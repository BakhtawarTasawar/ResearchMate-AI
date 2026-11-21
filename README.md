# ResearchGate AI — Scientific Research Assistant

> **Production-grade AI research workspace** deconstructing scientific abstracts and papers into five structured analytical dimensions using Google Gemini and FastAPI.

---

## 1. Architectural Overview

ResearchGate AI uses a **two-tier decoupled architecture**:

```
ResearchMate-AI/
│
├── frontend/                     # Streamlit Client Application
│   ├── app.py                    # Entry point & routing
│   ├── pages/
│   │   ├── home.py               # Overview & workflow pillars
│   │   ├── analyze.py            # Upload, editor, live analysis workspace
│   │   └── about.py              # Mission, architecture & roadmap
│   ├── components/
│   │   └── ui.py                 # Reusable cards, badges, hero, sidebar, footer
│   ├── services/
│   │   └── api_client.py         # HTTP client communicating with FastAPI
│   ├── utils/
│   │   ├── session.py            # Typed Streamlit session-state manager
│   │   └── icons.py              # Lucide-style SVG outline icon system
│   ├── styles/
│   │   └── styles.css            # Custom CSS (3D paper depth, tokens, responsive)
│   ├── assets/
│   │   └── favicon.svg           # Application favicon
│   ├── config.py / config/       # Frontend configuration & settings
│   └── requirements.txt
│
├── backend/                      # FastAPI Microservice & AI Engine
│   ├── app/
│   │   ├── main.py               # FastAPI app, lifespan, CORS, error handlers
│   │   ├── api/
│   │   │   └── routes/           # /health, /research/analyze, /research/extract-text
│   │   ├── core/
│   │   │   ├── config.py         # Settings & environment validation
│   │   │   └── logging.py        # Centralised logger
│   │   ├── schemas/
│   │   │   └── research.py       # Pydantic request / response schemas
│   │   ├── services/
│   │   │   ├── gemini_client.py  # Google GenAI client initialisation
│   │   │   ├── prompts.py        # Isolated scientific prompt templates
│   │   │   ├── research_service.py # Analysis, JSON sanitisation, schema validation
│   │   │   └── extraction_service.py # PDF / TXT parsing with pypdf
│   │   └── dependencies/         # Dependency injection providers
│   ├── tests/
│   │   └── test_api.py           # Pytest test suite (health, validation, mocks)
│   ├── .env.example
│   └── requirements.txt
│
├── .streamlit/
│   └── config.toml               # Streamlit theme & server options
├── .env.example                  # Root environment template
├── .gitignore
└── README.md
```

### Key Architectural Decisions

1. **Strict Credential Isolation**: The Gemini API key (`GEMINI_API_KEY`) lives solely in `backend/.env`. The Streamlit frontend only communicates with FastAPI over HTTP and never has direct access to Gemini credentials.
2. **Pydantic Contract Validation**: Requests and Gemini responses are strictly validated against schemas in `backend/app/schemas/research.py`.
3. **Robust Document Extraction**: PDF documents are parsed server-side using `pypdf` with encrypted-file detection and empty-page validation. TXT documents support UTF-8 and Latin-1 encodings.
4. **Resilient JSON Parsing**: Accidental markdown code fences (` ```json `) emitted by LLMs are sanitized before JSON deserialization.

---

## 2. Five Structured Research Dimensions

ResearchGate AI deconstructs scientific text into five accessible pillars:

| # | Dimension | Purpose | Accent Color |
|---|---|---|---|
| **1** | **Simple Summary** | Plain-language 2–3 sentence synthesis of problem, methodology & conclusion | Blue (`#1D4ED8`) |
| **2** | **Research Objectives** | Core hypotheses, primary research questions, and specific aims | Teal (`#0C6B5E`) |
| **3** | **Key Findings** | Empirical metrics, percentage changes, statistical significance, comparative results | Violet (`#5B21B6`) |
| **4** | **Important Keywords** | 4–10 concept tags, scientific ontology, and technical terminology | Amber (`#92400E`) |
| **5** | **Future Questions** | Open questions, study limitations, and forward-looking hypotheses | Rose (`#9D174D`) |

---

## 3. Quick Start Guide

### Prerequisites
- Python 3.10+
- Google Gemini API key ([Google AI Studio](https://aistudio.google.com/))

---

### Step 1: Clone & Set Up Backend

```bash
cd backend

# Create .env from example
cp .env.example .env
# Edit .env and paste your GEMINI_API_KEY:
# GEMINI_API_KEY=your_key_here
# GEMINI_MODEL=gemini-3.5-flash-lite

# Install backend dependencies
pip install -r requirements.txt

# Run the FastAPI server (starts on http://localhost:8000)
uvicorn app.main:app --reload --port 8000
```

Verify backend health at: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)  
Interactive API Documentation (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Step 2: Set Up & Run Frontend

Open a new terminal window:

```bash
cd frontend

# (Optional) Create frontend .env if backend runs on a non-default port
cp .env.example .env
# Default: BACKEND_API_URL=http://localhost:8000/api/v1

# Install frontend dependencies
pip install -r requirements.txt

# Start Streamlit application (starts on http://localhost:8501)
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 4. Running the Test Suite

Run backend unit and integration tests with `pytest`:

```bash
cd backend
pytest tests/ -v
```

Tests cover:
- Health check endpoint (`GET /api/v1/health`)
- Request validation (empty payloads, too-short text)
- Document extraction (valid TXT, unsupported extensions, empty files)
- Schema-validated mocked analysis pipeline

---

## 5. API Reference

### `GET /api/v1/health`
Checks backend and returns runtime version and configured Gemini model.

### `POST /api/v1/research/analyze`
**Body:**
```json
{
  "text": "Your scientific paper abstract or text (50 - 100,000 characters)..."
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "model_used": "gemini-3.5-flash-lite",
  "char_count": 850,
  "word_count": 125,
  "result": {
    "summary": "...",
    "objectives": ["..."],
    "findings": ["..."],
    "keywords": ["..."],
    "questions": ["..."]
  }
}
```

### `POST /api/v1/research/extract-text`
Multipart form upload of a `.pdf` or `.txt` file (max 10 MB).  
Returns extracted text and word/character counts.

---

## 6. Design System

- **Parchment Surface**: Neutral warm-slate background (`#F7F6F3`) avoiding stark clinical white or dark mode fatigue.
- **Physical Depth**: Subtle multi-layer ambient box-shadows (`var(--shadow-sm)`, `var(--shadow-hover)`) and soft 3D borders.
- **No AI Slop**: Clean scientific typography, semantic badges, and Lucide SVG outline icons — zero floating gradient blobs, chatbot robots, or generic emoji.
- **Responsive Layout**: Breakpoints tuned for 1440px, 1024px, 768px, and 480px viewports.

---

## 7. License

Built for the **STEM2Connect AI Hackathon**.
