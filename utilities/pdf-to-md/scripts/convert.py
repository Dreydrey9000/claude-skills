#!/usr/bin/env python3
"""
PDF to Markdown Batch Converter
================================
Converts PDF files to clean markdown using pymupdf4llm.
Works on single files or entire folders (recursive).

Usage:
    python convert.py /path/to/folder              # Convert all PDFs in folder
    python convert.py /path/to/file.pdf             # Convert single PDF
    python convert.py /path/to/folder --output /out # Custom output directory
    python convert.py /path/to/folder --flat        # No subfolder structure
    python convert.py /path/to/folder --include-foreign  # Include non-English files
"""

import argparse
import shutil
import sys
from pathlib import Path

try:
    import pymupdf4llm
except ImportError:
    print("ERROR: pymupdf4llm not installed.")
    print("Fix: python3 -m venv /tmp/pdf-converter && /tmp/pdf-converter/bin/pip install pymupdf4llm")
    sys.exit(1)

# Language prefixes to skip by default (common in translated document sets)
FOREIGN_PREFIXES = ("DE ", "NL ", "FR ", "IT ", "ES ", "PT ", "ZH ", "JA ", "KO ",
                    "DE-", "NL-", "FR-", "IT-", "ES-", "PT-", "ZH-", "JA-", "KO-")

FOREIGN_FOLDER_MARKERS = ("DE_", "DE-", "DE ", "NL_", "NL-", "NL ", "FR_", "FR-", "FR ",
                          "IT_", "IT-", "IT ", "ES_", "ES-", "ES ", "PT_", "PT-", "PT ",
                          "ZH_", "ZH-", "ZH ", "JA_", "JA-", "JA ", "KO_", "KO-", "KO ")


def is_foreign(filepath: Path, include_foreign: bool) -> bool:
    """Check if a file appears to be a non-English translation."""
    if include_foreign:
        return False
    # Check filename
    if filepath.name.startswith(FOREIGN_PREFIXES):
        return True
    # Check parent folder names
    for part in filepath.parts:
        if any(part.startswith(m) for m in FOREIGN_FOLDER_MARKERS):
            return True
    return False


def convert_pdf(pdf_path: Path, out_path: Path) -> tuple[bool, int, str]:
    """Convert a single PDF to markdown. Returns (success, line_count, error_msg)."""
    try:
        md = pymupdf4llm.to_markdown(str(pdf_path))
        lines = md.count("\n")
        if lines == 0 or len(md.strip()) == 0:
            return False, 0, "empty (visual-only PDF, no extractable text)"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(md, encoding="utf-8")
        return True, lines, ""
    except Exception as e:
        return False, 0, str(e)


def main():
    parser = argparse.ArgumentParser(description="Convert PDFs to Markdown")
    parser.add_argument("input", help="PDF file or folder containing PDFs")
    parser.add_argument("--output", "-o", help="Output directory (default: markdown/ subfolder)")
    parser.add_argument("--flat", action="store_true", help="Don't preserve folder structure")
    parser.add_argument("--include-foreign", action="store_true",
                        help="Include non-English files (DE/NL/FR/IT/etc.)")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()

    if not input_path.exists():
        print(f"ERROR: {input_path} does not exist")
        sys.exit(1)

    # Single file mode
    if input_path.is_file() and input_path.suffix.lower() == ".pdf":
        out_dir = Path(args.output) if args.output else input_path.parent / "markdown"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / input_path.with_suffix(".md").name

        print(f"Converting: {input_path.name}")
        success, lines, err = convert_pdf(input_path, out_file)

        if success:
            print(f"  OK ({lines} lines) -> {out_file}")
        else:
            print(f"  FAILED: {err}")
            # Move to cant-markdown
            cant = out_dir / "cant-markdown"
            cant.mkdir(exist_ok=True)
            shutil.copy2(input_path, cant / input_path.name)
            print(f"  Original PDF copied to: {cant / input_path.name}")
        return

    # Folder mode
    if not input_path.is_dir():
        print(f"ERROR: {input_path} is not a PDF file or directory")
        sys.exit(1)

    out_dir = Path(args.output) if args.output else input_path / "markdown"
    out_dir.mkdir(parents=True, exist_ok=True)
    cant_dir = out_dir / "cant-markdown"

    # Collect PDFs
    all_pdfs = sorted(input_path.rglob("*.pdf"))
    # Filter out PDFs already in our output directory
    all_pdfs = [p for p in all_pdfs if "markdown" not in str(p.relative_to(input_path)).split("/")]

    # Filter foreign language files
    pdfs = [p for p in all_pdfs if not is_foreign(p, args.include_foreign)]
    skipped = len(all_pdfs) - len(pdfs)

    print(f"Found {len(pdfs)} PDFs to convert", end="")
    if skipped > 0:
        print(f" (skipped {skipped} non-English files)", end="")
    print(f"\nOutput: {out_dir}\n")

    if not pdfs:
        print("No PDFs found to convert.")
        return

    converted = 0
    failed = 0
    empty = 0

    for i, pdf in enumerate(pdfs, 1):
        rel = pdf.relative_to(input_path)
        print(f"[{i}/{len(pdfs)}] {rel}...", end=" ", flush=True)

        # Determine output path
        if args.flat:
            out_file = out_dir / pdf.with_suffix(".md").name
        else:
            out_file = out_dir / rel.with_suffix(".md")

        success, lines, err = convert_pdf(pdf, out_file)

        if success:
            print(f"OK ({lines} lines)")
            converted += 1
        elif lines == 0 and "empty" in err:
            print(f"EMPTY - {err}")
            empty += 1
            # Copy original to cant-markdown
            cant_dir.mkdir(exist_ok=True)
            shutil.copy2(pdf, cant_dir / pdf.name)
            # Remove empty .md if it was created
            if out_file.exists():
                out_file.unlink()
        else:
            print(f"ERROR - {err}")
            failed += 1

    # Summary
    print(f"\n{'='*50}")
    print(f"RESULTS:")
    print(f"  Converted:  {converted}/{len(pdfs)}")
    if empty > 0:
        print(f"  Empty/Visual: {empty} (originals in cant-markdown/)")
    if failed > 0:
        print(f"  Failed:     {failed}")
    if skipped > 0:
        print(f"  Skipped:    {skipped} (non-English)")
    print(f"\nMarkdown files: {out_dir}")
    if empty > 0:
        print(f"Unconvertible: {cant_dir}")


if __name__ == "__main__":
    main()
