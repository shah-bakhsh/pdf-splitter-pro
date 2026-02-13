"""
PDF Processing Module — PDF reading, text extraction, and splitting.
"""

from pypdf import PdfReader, PdfWriter
import io
import re


def extract_page_texts(reader: PdfReader) -> list[str]:
    """Extract text from each page of the PDF."""
    return [page.extract_text() or "" for page in reader.pages]


def extract_full_text(page_texts: list[str]) -> str:
    """Combine all page texts into one string."""
    return "\n".join(page_texts)


def split_pdf_to_buffers(uploaded_file, chapters: list[dict]) -> list[dict]:
    """Split PDF into chapter byte buffers."""
    uploaded_file.seek(0)
    reader = PdfReader(uploaded_file)
    results = []

    for ch in chapters:
        writer = PdfWriter()
        for page_num in range(ch["start_page"] - 1, min(ch["end_page"], len(reader.pages))):
            writer.add_page(reader.pages[page_num])

        buf = io.BytesIO()
        writer.write(buf)

        results.append({
            "name": ch["name"],
            "start_page": ch["start_page"],
            "end_page": ch["end_page"],
            "file_name": f"{ch['name'].replace(' ', '_')}_pages_{ch['start_page']}_to_{ch['end_page']}.pdf",
            "data": buf.getvalue(),
        })

    return results


def get_chapter_texts(page_texts: list[str], chapters: list[dict]) -> list[str]:
    """Extract text for each chapter."""
    result = []
    for ch in chapters:
        text = "\n".join(page_texts[ch["start_page"] - 1 : ch["end_page"]])
        result.append(text)
    return result
