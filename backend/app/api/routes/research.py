"""
API routes for research analysis and document extraction.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.core.config import get_settings
from app.core.logging import get_logger
from app.dependencies import extraction_service_dep, research_service_dep
from app.schemas import (
    AnalyzeResponse,
    AnalyzeTextRequest,
    ExtractTextResponse,
)
from app.services.extraction_service import DocumentExtractionService
from app.services.research_service import ResearchAnalysisService

logger = get_logger(__name__)
router = APIRouter(prefix="/research", tags=["Research"])


# ---------------------------------------------------------------------------
# POST /research/analyze  — analyse plain text
# ---------------------------------------------------------------------------

@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    summary="Analyse research text",
    description=(
        "Accepts a scientific abstract or paper text and returns five structured "
        "research insight dimensions powered by Google Gemini."
    ),
)
def analyze_text(
    body: AnalyzeTextRequest,
    service: ResearchAnalysisService = Depends(research_service_dep),
) -> AnalyzeResponse:
    settings = get_settings()
    logger.info("POST /research/analyze  chars=%d", len(body.text))

    try:
        result = service.analyse(body.text)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc))
    except Exception as exc:
        logger.exception("Unexpected error during analysis")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again.",
        )

    words = len(body.text.split())
    return AnalyzeResponse(
        success=True,
        model_used=settings.GEMINI_MODEL,
        char_count=len(body.text),
        word_count=words,
        result=result,
    )


# ---------------------------------------------------------------------------
# POST /research/extract-text  — extract text from PDF / TXT upload
# ---------------------------------------------------------------------------

@router.post(
    "/extract-text",
    response_model=ExtractTextResponse,
    summary="Extract text from uploaded document",
    description="Upload a PDF or TXT file and receive its extracted plain text.",
)
async def extract_text(
    file: UploadFile = File(..., description="PDF or TXT file to extract text from."),
    service: DocumentExtractionService = Depends(extraction_service_dep),
) -> ExtractTextResponse:
    logger.info(
        "POST /research/extract-text  filename=%s content_type=%s",
        file.filename,
        file.content_type,
    )

    content_bytes = await file.read()

    try:
        text = service.extract(
            filename=file.filename or "upload",
            content_bytes=content_bytes,
            content_type=file.content_type,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

    ext = (file.filename or "").rsplit(".", 1)[-1].lower() if "." in (file.filename or "") else "unknown"

    return ExtractTextResponse(
        success=True,
        filename=file.filename or "upload",
        file_type=ext,
        char_count=len(text),
        word_count=len(text.split()),
        text=text,
    )
