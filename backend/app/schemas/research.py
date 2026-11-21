"""
Pydantic schemas for research analysis request/response validation.
"""
from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field, field_validator


# ---------------------------------------------------------------------------
# Request schemas
# ---------------------------------------------------------------------------

class AnalyzeTextRequest(BaseModel):
    """Body for POST /research/analyze when sending plain text."""

    text: str = Field(
        ...,
        min_length=50,
        max_length=100_000,
        description="Raw scientific abstract or paper text to analyse.",
    )

    @field_validator("text")
    @classmethod
    def strip_text(cls, v: str) -> str:
        return v.strip()


# ---------------------------------------------------------------------------
# Response schemas
# ---------------------------------------------------------------------------

class AnalysisResult(BaseModel):
    """
    Structured output from Gemini analysis — the five research dimensions.
    All fields are validated to ensure they are non-empty lists or strings.
    """

    summary: str = Field(
        ...,
        description="Plain-language 2–3 sentence synthesis of the study.",
    )
    objectives: List[str] = Field(
        ...,
        min_length=1,
        description="Research questions and aims extracted from the abstract.",
    )
    findings: List[str] = Field(
        ...,
        min_length=1,
        description="Key empirical results, metrics, and discoveries.",
    )
    keywords: List[str] = Field(
        ...,
        min_length=1,
        description="4–10 high-salience scientific terms from the text.",
    )
    questions: List[str] = Field(
        ...,
        min_length=1,
        description="Suggested future research directions based on this study.",
    )


class AnalyzeResponse(BaseModel):
    """Full response envelope from /research/analyze."""

    success: bool = True
    model_used: str
    char_count: int
    word_count: int
    result: AnalysisResult


class ExtractTextResponse(BaseModel):
    """Response from /research/extract-text (file upload endpoint)."""

    success: bool = True
    filename: str
    file_type: str
    char_count: int
    word_count: int
    text: str


class HealthResponse(BaseModel):
    """Response from GET /health."""

    status: str = "ok"
    version: str
    gemini_model: str


class ErrorResponse(BaseModel):
    """Standard error envelope returned on 4xx / 5xx."""

    success: bool = False
    error: str
    detail: str | None = None
