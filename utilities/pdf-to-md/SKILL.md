---
name: pdf-to-md
description: Batch convert PDF files to clean Markdown. Point it at a folder or single file and get readable markdown output. Handles books, reports, worksheets, slide decks — anything with extractable text. Visual-only PDFs (diagrams, templates with no text) get sorted into a "cant-markdown" folder automatically.
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
---

# PDF to Markdown Converter

## What This Does

Converts PDF files to clean, readable Markdown using `pymupdf4llm` — the best PDF-to-markdown library available. It preserves:
- Headers and structure
- Tables
- Lists and bullet points
- Bold/italic formatting
- Page breaks as horizontal rules

## How To Use

When the user asks to convert PDFs to markdown, follow this workflow:

### Step 1: Identify the target

The user will provide either:
- A **folder path** containing PDFs (converts all PDFs recursively)
- A **single PDF file path** (converts just that file)

### Step 2: Ensure pymupdf4llm is available

Run the converter script. It auto-creates a venv at `/tmp/pdf-converter` if one doesn't exist:

```bash
# Check if venv exists, create if not
if [ ! -f /tmp/pdf-converter/bin/python ]; then
  python3 -m venv /tmp/pdf-converter
  /tmp/pdf-converter/bin/pip install pymupdf4llm
fi
```

### Step 3: Run the conversion

For a **folder** of PDFs:
```bash
/tmp/pdf-converter/bin/python ~/.claude/skills/pdf-to-md/scripts/convert.py "/path/to/folder"
```

For a **single file**:
```bash
/tmp/pdf-converter/bin/python ~/.claude/skills/pdf-to-md/scripts/convert.py "/path/to/file.pdf"
```

### Step 4: Report results

The script outputs:
- How many PDFs were found
- Each file's conversion status (OK with line count, or ERROR)
- Any empty conversions get moved to `cant-markdown/` subfolder with the original PDF
- Final output location

### Options

The script accepts these optional flags:
- `--output /custom/path` — Save markdown files to a custom location (default: `markdown/` subfolder next to the input)
- `--flat` — Don't preserve folder structure, put all .md files in one directory
- `--include-foreign` — Include non-English files (by default, skips files starting with DE/NL/FR/IT/ES/PT/ZH/JA/KO prefixes)

### What Can't Be Converted

Some PDFs are purely visual — diagrams, canvas templates, scanned images without OCR. These produce empty markdown. The script automatically:
1. Detects empty output (0 lines)
2. Copies the original PDF to a `cant-markdown/` folder
3. Removes the empty .md file

Tell the user which files couldn't be converted and why (visual-only, no extractable text).

## Technical Details

- **Library**: `pymupdf4llm` (built on PyMuPDF/fitz)
- **Python**: Uses a temporary venv at `/tmp/pdf-converter` to avoid polluting system Python
- **Performance**: ~1-2 seconds per small PDF, 10-30 seconds for large books (200+ pages)
- **Output quality**: Better than most alternatives because pymupdf4llm is specifically designed for LLM-readable markdown output
