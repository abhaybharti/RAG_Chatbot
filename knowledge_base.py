"""Load Markdown files and retrieve sections while retaining source metadata."""
from pathlib import Path
import re
import math

TOKEN_RE = re.compile(r"[a-z0-9]+", re.IGNORECASE)
STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "could",
    "did", "do", "does", "for", "from", "how", "i", "in", "is", "it",
    "me", "of", "on", "or", "please", "should", "tell", "that", "the",
    "their", "this", "to", "was", "what", "when", "where", "which",
    "who", "why", "will", "with", "would", "you", "your"
}

def tokenize(text):
    return [t.lower() for t in TOKEN_RE.findall(text) if t.lower() not in STOP_WORDS]

def parse_markdown(text, filename):
    """Split Markdown into heading-based sections. Content before the first heading is 'Introduction'."""
    sections = []
    heading_stack = []
    current_lines = []
    current_start = 1
    current_heading = "Introduction"

    def save(end_line):
        content = "\n".join(current_lines).strip()
        if content:
            sections.append({
                "id": f"S{len(sections) + 1}",
                "file": filename,
                "section": " → ".join(heading_stack) if heading_stack else current_heading,
                "content": content,
                "start_line": current_start,
                "end_line": end_line,
            })

    lines = text.splitlines()
    for line_number, line in enumerate(lines, start=1):
        match = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line)
        if match:
            save(line_number - 1)
            level = len(match.group(1))
            title = match.group(2).strip()
            heading_stack = heading_stack[:level - 1]
            heading_stack.append(title)
            current_heading = title
            current_lines = []
            current_start = line_number
        else:
            current_lines.append(line)

    save(len(lines))
    return sections

def load_documents(directory="docs"):
    """Read every .md file recursively from directory, sorted for reproducible source IDs."""
    root = Path(directory)
    if not root.exists():
        raise FileNotFoundError(f"Documents directory does not exist: {root.resolve()}")

    all_sections = []
    for path in sorted(root.rglob("*.md")):
        if not path.is_file():
            continue
        relative_name = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        all_sections.extend(parse_markdown(text, relative_name))
    # Ensure IDs are unique across files.
    for index, section in enumerate(all_sections, start=1):
        section["id"] = f"S{index}"
    return all_sections

def retrieve_sections(question, sections, top_k=5, min_score=0.12):
    """
    Simple local keyword retrieval. It costs no embedding/API calls.
    Scores are heuristic, not calibrated probabilities; tune using your own questions.
    """
    query_terms = set(tokenize(question))
    if not query_terms:
        return []

    scored = []
    for section in sections:
        content_terms = set(tokenize(section["section"] + " " + section["content"]))
        overlap = query_terms & content_terms
        if not overlap:
            continue
        # Penalize weak matches and slightly reward multiple matching terms.
        score = len(overlap) / math.sqrt(max(1, len(query_terms)))
        score += 0.15 if any(term in tokenize(section["section"]) for term in query_terms) else 0
        if score >= min_score:
            scored.append((score, section))

    scored.sort(key=lambda item: (-item[0], item[1]["file"], item[1]["start_line"]))
    return [dict(section, retrieval_score=round(score, 3)) for score, section in scored[:top_k]]
