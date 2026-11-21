"""
Unit and integration tests for ResearchGate AI FastAPI backend.
"""
from __future__ import annotations

import io
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.research import AnalysisResult
from app.services.research_service import ResearchAnalysisService
from app.dependencies import research_service_dep

client = TestClient(app)


# ---------------------------------------------------------------------------
# Health endpoint test
# ---------------------------------------------------------------------------

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "gemini_model" in data


# ---------------------------------------------------------------------------
# Validation tests
# ---------------------------------------------------------------------------

def test_analyze_empty_body():
    response = client.post("/api/v1/research/analyze", json={})
    assert response.status_code == 422


def test_analyze_too_short_text():
    response = client.post("/api/v1/research/analyze", json={"text": "Short abstract"})
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# Document extraction tests
# ---------------------------------------------------------------------------

def test_extract_txt_success():
    content = b"This is a valid scientific research text for extraction testing."
    files = {"file": ("sample.txt", io.BytesIO(content), "text/plain")}
    response = client.post("/api/v1/research/extract-text", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["filename"] == "sample.txt"
    assert data["file_type"] == "txt"
    assert data["char_count"] == len(content)
    assert data["text"] == content.decode()


def test_extract_unsupported_extension():
    content = b"Binary or disallowed file content."
    files = {"file": ("sample.exe", io.BytesIO(content), "application/octet-stream")}
    response = client.post("/api/v1/research/extract-text", files=files)
    assert response.status_code == 422
    assert "Unsupported file type" in response.json()["detail"]


def test_extract_empty_txt():
    files = {"file": ("empty.txt", io.BytesIO(b"   "), "text/plain")}
    response = client.post("/api/v1/research/extract-text", files=files)
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# Mocked analysis test (ensures schema compliance without hitting Gemini quota)
# ---------------------------------------------------------------------------

class MockResearchService(ResearchAnalysisService):
    def __init__(self):
        pass

    def analyse(self, text: str) -> AnalysisResult:
        return AnalysisResult(
            summary="A mock plain-language summary for testing purposes.",
            objectives=["Objective 1: Evaluate model architecture."],
            findings=["Finding 1: 99.9% accuracy observed."],
            keywords=["mock", "test", "science", "evaluation"],
            questions=["What happens at scale?"]
        )


def test_analyze_mocked_success():
    app.dependency_overrides[research_service_dep] = lambda: MockResearchService()
    try:
        sample_text = (
            "This is a sufficiently long mock scientific abstract describing novel "
            "methods in artificial intelligence and deep neural network architectures."
        )
        response = client.post("/api/v1/research/analyze", json={"text": sample_text})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["result"]["summary"] == "A mock plain-language summary for testing purposes."
        assert len(data["result"]["objectives"]) == 1
        assert len(data["result"]["findings"]) == 1
        assert len(data["result"]["keywords"]) == 4
        assert len(data["result"]["questions"]) == 1
    finally:
        app.dependency_overrides.clear()
