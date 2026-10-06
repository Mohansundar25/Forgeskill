from io import BytesIO

from pypdf import PdfReader


def extract_text(data: bytes) -> str:
    """Extract plain text from every page of a PDF file."""
    reader = PdfReader(BytesIO(data))
    return '\n'.join((page.extract_text() or '') for page in reader.pages)
