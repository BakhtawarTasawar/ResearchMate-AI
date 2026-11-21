"""
Document extraction service.
Handles PDF and TXT file bytes → plain text, with thorough validation.
"""
from __future__ import annotations

import io

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)

_ALLOWED_MIME: set[str] = {
    "application/pdf",
    "text/plain",
}
_ALLOWED_EXTENSIONS: set[str] = {".pdf", ".txt"}


class DocumentExtractionService:
    """Extracts plain text from uploaded PDF or TXT files."""

    def __init__(self) -> None:
        self._settings = get_settings()

    def extract(
        self,
        filename: str,
        content_bytes: bytes,
        content_type: str | None = None,
    ) -> str:
        """
        Extract text from file bytes.
        Returns the extracted plain text string.
        Raises ValueError for invalid/unsupported/empty content.
        """
        lower_name = filename.lower()
        ext = "." + lower_name.rsplit(".", 1)[-1] if "." in lower_name else ""

        if ext not in _ALLOWED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type '{ext}'. "
                "Please upload a PDF (.pdf) or plain text (.txt) file."
            )

        if len(content_bytes) > self._settings.MAX_UPLOAD_BYTES:
            mb = self._settings.MAX_UPLOAD_BYTES // (1024 * 1024)
            raise ValueError(f"File exceeds the {mb} MB size limit.")

        if ext == ".pdf":
            return self._extract_pdf(content_bytes)
        else:
            return self._extract_txt(content_bytes)

    # ------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_pdf(content_bytes: bytes) -> str:
        """Extract text from PDF bytes using pypdf."""
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise RuntimeError("pypdf is not installed in the backend environment.") from exc

        reader = PdfReader(io.BytesIO(content_bytes))

        if reader.is_encrypted:
            raise ValueError(
                "This PDF is password-protected. Please upload an unlocked PDF."
            )

        pages: list[str] = []
        for page in reader.pages:
            page_text = page.extract_text() or ""
            stripped = page_text.strip()
            if stripped:
                pages.append(stripped)

        text = "\n\n".join(pages).strip()

        if not text:
            raise ValueError(
                "No readable text could be extracted from this PDF. "
                "It may be a scanned image-only document. "
                "OCR support is not currently available."
            )

        logger.info("PDF extracted: %d pages → %d characters", len(reader.pages), len(text))
        return text

    @staticmethod
    def _extract_txt(content_bytes: bytes) -> str:
        """Decode TXT bytes, trying UTF-8 then latin-1 fallback."""
        try:
            text = content_bytes.decode("utf-8").strip()
        except UnicodeDecodeError:
            text = content_bytes.decode("latin-1", errors="replace").strip()

        if not text:
            raise ValueError("The uploaded TXT file is empty.")

        logger.info("TXT extracted: %d characters", len(text))
        return text


_service: DocumentExtractionService | None = None


def get_extraction_service() -> DocumentExtractionService:
    global _service
    if _service is None:
        _service = DocumentExtractionService()
    return _service
