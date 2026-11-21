"""
Error-handling, edge-case, and security tests for ResearchGate AI.
"""
from __future__ import annotations

import io
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.research_service import ResearchAnalysisService
from app.dependencies import research_service_dep

client = TestClient(app)


def test_malformed_gemini_json():
    svc = ResearchAnalysisService.__new__(ResearchAnalysisService)
    with pytest.raises(ValueError, match="invalid response format|Could not parse"):
        svc._parse_json("Not a json response")


def test_missing_keys_gemini_json():
    svc = ResearchAnalysisService.__new__(ResearchAnalysisService)
    with pytest.raises(ValueError, match="did not match the required research|missing required fields"):
        svc._validate_result({"summary": "incomplete json"})


def test_strip_markdown_fences():
    svc = ResearchAnalysisService.__new__(ResearchAnalysisService)
    fenced = """```json
    {
        "summary": "Valid summary",
        "objectives": ["Goal 1"],
        "findings": ["Result 1"],
        "keywords": ["tag1", "tag2"],
        "questions": ["Next step 1"]
    }
    ```"""
    parsed = svc._parse_json(fenced)
    assert parsed["summary"] == "Valid summary"
    assert len(parsed["objectives"]) == 1


def test_oversized_file_upload():
    huge_bytes = b"0" * (11 * 1024 * 1024)
    files = {"file": ("huge.txt", io.BytesIO(huge_bytes), "text/plain")}
    response = client.post("/api/v1/research/extract-text", files=files)
    assert response.status_code == 422
    assert "exceeds the 10 MB size limit" in response.json()["detail"]


def test_invalid_extension():
    files = {"file": ("script.sh", io.BytesIO(b"echo hello"), "application/x-sh")}
    response = client.post("/api/v1/research/extract-text", files=files)
    assert response.status_code == 422
    assert "Unsupported file type" in response.json()["detail"]


def test_frontend_api_client_unreachable_backend():
    import sys
    from pathlib import Path
    frontend_dir = Path(__file__).resolve().parent.parent.parent / "frontend"
    if str(frontend_dir) not in sys.path:
        sys.path.insert(0, str(frontend_dir))

    from services.api_client import ResearchAPIClient, APIError

    dead_client = ResearchAPIClient(base_url="http://127.0.0.1:54321/api/v1", timeout=1.0)
    with pytest.raises(APIError, match="Unable to connect|unreachable|Cannot connect|timed out"):
        dead_client.health_check()


def test_simulated_gemini_rate_limit_and_network_error():
    class FailingService(ResearchAnalysisService):
        def __init__(self):
            pass

        def analyse(self, text: str):
            raise RuntimeError("Failed to reach the Gemini API. Please check your network connection and API key.")

    app.dependency_overrides[research_service_dep] = lambda: FailingService()
    try:
        response = client.post(
            "/api/v1/research/analyze",
            json={"text": "This is a sufficiently long mock abstract to pass initial length validation."}
        )
        assert response.status_code == 503
        assert "Failed to reach the Gemini API" in response.json()["detail"]
        assert "traceback" not in response.text.lower()
    finally:
        app.dependency_overrides.clear()


def test_valid_pdf_extraction():
    pdf_data = b"""%PDF-1.4
1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj
2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj
3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj
4 0 obj << /Length 55 >> stream
BT
/F1 12 Tf
72 712 Td
(Valid scientific paper content extracted from PDF.) Tj
ET
endstream endobj
5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj
xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000244 00000 n 
0000000351 00000 n 
trailer << /Size 6 /Root 1 0 R >>
startxref
428
%%EOF"""
    files = {"file": ("paper.pdf", io.BytesIO(pdf_data), "application/pdf")}
    response = client.post("/api/v1/research/extract-text", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["file_type"] == "pdf"
    assert "Valid scientific paper content" in data["text"]


def test_scanned_or_blank_pdf_rejection():
    from pypdf import PdfWriter
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    buf = io.BytesIO()
    writer.write(buf)
    files = {"file": ("blank.pdf", io.BytesIO(buf.getvalue()), "application/pdf")}
    response = client.post("/api/v1/research/extract-text", files=files)
    assert response.status_code == 422
    assert "No readable text could be extracted" in response.json()["detail"]


def test_empty_gemini_response_error():
    svc = ResearchAnalysisService.__new__(ResearchAnalysisService)
    with pytest.raises(ValueError, match="empty response|invalid response format|Could not parse"):
        svc._parse_json("")


def test_pydantic_validation_error_on_invalid_schema():
    svc = ResearchAnalysisService.__new__(ResearchAnalysisService)
    bad_data = {
        "summary": "Some summary",
        "objectives": [],  # fails min_length=1
        "findings": ["finding 1"],
        "keywords": ["kw1"],
        "questions": ["q1"],
    }
    with pytest.raises(ValueError, match="did not match the required research|Response validation failed"):
        svc._validate_result(bad_data)
