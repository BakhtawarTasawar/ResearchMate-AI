"""
Frontend configuration — API base URL and application constants.
"""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Load frontend .env if present
_env_path = Path(__file__).parent.parent / ".env"
if _env_path.exists():
    load_dotenv(_env_path)

# ---------------------------------------------------------------------------
# Backend
# ---------------------------------------------------------------------------
BACKEND_API_URL: str = os.getenv("BACKEND_API_URL", "http://localhost:8000/api/v1")

# ---------------------------------------------------------------------------
# App metadata
# ---------------------------------------------------------------------------
APP_TITLE = "ResearchGate AI"
APP_SUBTITLE = "Scientific Research Assistant"
APP_VERSION = "2.0"

# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------
PAGE_HOME = "Home"
PAGE_ANALYZE = "Analyze Paper"
PAGE_ABOUT = "About"
PAGE_AUTH = "Account"
PAGES = [PAGE_HOME, PAGE_ANALYZE, PAGE_ABOUT, PAGE_AUTH]

# ---------------------------------------------------------------------------
# Assets
# ---------------------------------------------------------------------------
ASSETS_DIR = Path(__file__).parent / "assets"
STYLES_DIR = Path(__file__).parent / "styles"
FAVICON_PATH = ASSETS_DIR / "favicon.svg"

# ---------------------------------------------------------------------------
# Sample abstract (CRISPR — preserved from original)
# ---------------------------------------------------------------------------
SAMPLE_ABSTRACT = (
    "CRISPR-Cas9 technology has emerged as a transformative tool for targeted "
    "genome engineering, offering unprecedented precision in modifying genomic "
    "sequences. However, off-target mutations and variable editing efficiencies "
    "remain significant bottlenecks for therapeutic applications in human "
    "pluripotent stem cells (hPSCs). In this study, we developed an engineered "
    "high-fidelity Cas9 variant (eCas9-HF) combined with chemically modified "
    "single guide RNAs (sgRNAs) to address these limitations. We evaluated "
    "cleavage specificity and targeted insertion efficiency across 14 loci "
    "associated with monogenic neurodegenerative disorders. Our results "
    "demonstrated a 7.4-fold reduction in detectable off-target cleavage events "
    "while retaining over 88% on-target editing efficiency compared to wild-type "
    "SpCas9. Furthermore, whole-genome sequencing of treated hPSC clones confirmed "
    "long-term genomic integrity and pluripotency marker retention. These findings "
    "provide a robust methodology for high-precision therapeutic gene editing and "
    "establish a foundation for safe cellular replacement therapies."
)
