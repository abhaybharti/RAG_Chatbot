# Markdown Knowledge Agent (Terminal)
A terminal chatbot that reads Markdown files, retrieved relevant sections and asks Google Gemini model to answer using those sections only.

The app reads all `.md` files recursively. It prints a note if it finds a number other than 10. Replace the sample files with your own documents before relying on answers.


## Features
- Reads every `*.md` file under `docs/` including subfolders
- Split markdown into heading-based section
- Keeps the filename and heading path with each section
- Print source filename and section headings for supported answers
- Returns a clear "not found" response with retrieval finds no keyword overlap or the model reports insufficient evidence
- Includes offline unit tests for Markdown parsing and retrieval

## Action Item:
- Add code to read *.doc/pdf/ppt/html/json/csv/.txt files
- Add 10 files for each file type
- How to do cleanup & what clean up is needed
- Design a RAG architecture for above two document (covering how document ingestion happens, at what frequency), How query time retrieval can be reduced
- How to add vector database, what problem does it serve
- How chunking is happening in current project
