"""Terminal chatbot for answering questions from Markdown documents only."""
from dotenv import load_dotenv
from knowledge_base import load_documents, retrieve_sections
from answer import answer_question

load_dotenv()

DOCS_DIR = "docs"
TOP_K = 5

def main():
    sections = load_documents(DOCS_DIR)
    if not sections:
        print(f"No Markdown sections found in '{DOCS_DIR}'. Add .md files and try again.")
        return

    filenames = sorted({section["file"] for section in sections})
    print(f"Loaded {len(filenames)} Markdown file(s), {len(sections)} section(s).")
    if len(filenames) != 10:
        print(f"NOTE: Expected 10 Markdown files; found {len(filenames)}.")
    print("Ask questions based on the documents. Type 'exit' to quit.\n")

    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break
        if question.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break
        if not question:
            continue

        matches = retrieve_sections(question, sections, top_k=TOP_K)
        if not matches:
            print("\nAssistant: I couldn't find this information in the provided Markdown documents.\n")
            continue

        try:
            response = answer_question(question, matches)
            print(f"\nAssistant: {response['answer']}")
            if response["sources"]:
                print("\nSources:")
                for source in response["sources"]:
                    # Source IDs are validated against retrieved sections in answerer.py.
                    print(f"- {source['file']} — {source['section']}")
            print()
        except Exception as exc:
            print("\nAssistant: I couldn't generate an answer. Check your API key, connection, and model settings.")
            print(f"Technical detail: {exc}\n")

if __name__ == "__main__":
    main()
