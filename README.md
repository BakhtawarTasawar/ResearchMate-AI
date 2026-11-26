# ResearchMate AI — AI-Powered Scientific Research Assistant

**ResearchMate AI** is a web-based scientific research assistant built for the **STEM2Connect AI Hackathon 2026**. It helps students, researchers, and academics quickly understand dense scientific papers and abstracts by transforming them into five structured research dimensions using Google Gemini, FastAPI, and Streamlit.

---

## Table of Contents

- [Live Demo and Repository](#live-demo-and-repository)
- [Project Overview](#project-overview)
- [Five Structured Research Dimensions](#five-structured-research-dimensions)
- [Technical Architecture](#technical-architecture)
- [Technology Stack](#technology-stack)
- [Installation and Local Setup](#installation-and-local-setup)
- [API Documentation](#api-documentation)
- [Running Tests](#running-tests)
- [Challenges and Solutions](#challenges-and-solutions)
- [Limitations](#limitations)
- [License](#license)

---

## Live Demo and Repository

- **Live Application:** [https://researchmate-ai-project.streamlit.app/](https://researchmate-ai-project.streamlit.app/)
- **GitHub Repository:** [https://github.com/BakhtawarTasawar/ResearchMate-AI](https://github.com/BakhtawarTasawar/ResearchMate-AI)

### How to Test the Application

1. Open the live application link above.
2. Create an account on the **Register** tab or sign in with existing credentials.
3. Navigate to **Analyze Paper**.
4. Paste a scientific abstract or upload a `.pdf` or `.txt` research document (up to 10 MB).
5. Run the analysis to view the paper broken down into five structured research dimensions.

---

## Project Overview

Scientific literature is often dense, technical, and time-consuming to read. Researchers and students frequently need to review dozens of papers to determine whether a study's methodology, empirical findings, and open questions are relevant to their work.

**ResearchMate AI** addresses this problem by providing a structured workspace that:

- Accepts raw pasted text, plain-text (`.txt`) files, or multi-page `.pdf` documents.
- Extracts readable text server-side and validates input length.
- Generates a consistent, five-part analytical breakdown powered by Google Gemini.

**Intended Users:** University students, academic researchers, literature reviewers, and STEM professionals seeking faster comprehension of scientific papers.

---

## Five Structured Research Dimensions

ResearchMate AI deconstructs submitted scientific text into five consistent output sections:

| # | Dimension | Purpose | Accent Color |
|---|---|---|---|
| **1** | **Simple Summary** | Plain-language 2–3 sentence synthesis of the problem, methodology, and conclusion | Blue (`#1D4ED8`) |
| **2** | **Research Objectives** | Core hypotheses, primary research questions, and specific aims | Teal (`#0C6B5E`) |
| **3** | **Key Findings** | Empirical metrics, percentage changes, statistical significance, and comparative results | Violet (`#5B21B6`) |
| **4** | **Important Keywords** | 4–10 high-salience scientific concepts and technical terms | Amber (`#92400E`) |
| **5** | **Future Research Questions** | Open questions, study limitations, and forward-looking research directions | Rose (`#9D174D`) |

---

## Technical Architecture

ResearchMate AI uses a **two-tier decoupled architecture** separating the Streamlit user interface from the FastAPI backend and AI processing layer.

```text
ResearchMate-AI/
│
├── frontend/                       # Streamlit Client Application
│   ├── app.py                      # Entry point, auth gate, navbar & page routing
│   ├── pages/
│   │   ├── auth.py                 # Login & registration workflows
│   │   ├── home.py                 # Dashboard overview & workflow pillars
│   │   ├── analyze.py              # Text editor, file upload & analysis results view
│   │   └── about.py                # Project mission & architecture overview
│   ├── components/
│   │   └── ui.py                   # Reusable cards, badges, navbar & footer
│   ├── services/
│   │   └── api_client.py           # Session-scoped httpx client for FastAPI
│   ├── utils/
│   │   ├── session.py              # Typed Streamlit session-state manager
│   │   └── icons.py                # Lucide-style SVG outline icon system
│   ├── styles/
│   │   └── styles.css              # Custom CSS styling and responsive layout
│   ├── assets/
│   │   └── favicon.svg             # Application favicon
│   ├── config/
│   │   └── settings.py             # Frontend configuration & page constants
│   └── requirements.txt
│
├── backend/                        # FastAPI Service & AI Engine
│   ├── app/
│   │   ├── main.py                 # FastAPI app, lifespan, CORS & error handlers
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── auth.py         # /auth/register, /auth/login, /auth/me
│   │   │       ├── health.py       # /health
│   │   │       └── research.py     # /research/extract-text, /research/analyze
│   │   ├── core/
│   │   │   ├── config.py           # Settings & environment validation
│   │   │   ├── logging.py          # Centralised logger
│   │   │   └── security.py         # Argon2 password hashing & JWT utilities
│   │   ├── db/
│   │   │   ├── database.py         # SQLAlchemy engine & session management
│   │   │   └── models.py           # User database model
│   │   ├── dependencies/           # FastAPI dependency injection providers
│   │   ├── schemas/
│   │   │   └── research.py         # Pydantic request & response schemas
│   │   └── services/
│   │       ├── gemini_client.py    # Google GenAI client initialisation
│   │       ├── prompts.py          # Structured scientific prompt templates
│   │       ├── research_service.py # Gemini calls, retries, JSON & schema validation
│   │       └── extraction_service.py # PDF / TXT extraction via pypdf
│   ├── migrations/                 # Alembic database migrations
│   ├── tests/                      # Backend pytest suite
│   ├── .env.example
│   └── requirements.txt
│
├── .streamlit/
│   └── config.toml                 # Streamlit theme & server configuration
├── docker-compose.yml              # Multi-container PostgreSQL, backend & frontend setup
├── .env.example                    # Root environment template
└── README.md
```

### Component Responsibilities

- **Streamlit Frontend (`frontend/`):** Renders the user interface, enforces an authentication gate before displaying protected pages, manages per-user session state (`st.session_state`), and communicates with the backend exclusively via HTTP.
- **FastAPI Backend (`backend/`):** Handles user registration and login, validates file uploads and text payloads, manages database sessions, and orchestrates AI requests.
- **Google Gemini API (`gemini_client.py`, `research_service.py`):** Generates structured research analyses using `gemini-3.5-flash-lite` via the `google-genai` SDK. The `GEMINI_API_KEY` is stored strictly on the backend and never exposed to the frontend.
- **PDF & Text Extraction (`extraction_service.py`):** Parses uploaded `.pdf` files server-side using `pypdf` (supporting multi-page documents while rejecting encrypted or empty/image-only PDFs) and decodes `.txt` files using UTF-8 with a Latin-1 fallback.
- **Authentication & API Communication (`auth.py`, `security.py`, `api_client.py`):** Uses Argon2 password hashing (`pwdlib`) and Bearer JWT tokens (`PyJWT`). The frontend stores each user's API client in `st.session_state` to isolate authentication tokens per session.
- **Structured AI Response Validation (`schemas/research.py`, `research_service.py`):** Requests JSON output conforming to `AnalysisResult`, strips accidental Markdown code fences, and validates all five fields with Pydantic v2 before returning results.

---

## Technology Stack

| Role | Technology |
|---|---|
| **Programming Language** | Python 3.10+ |
| **Frontend** | Streamlit, `httpx`, `python-dotenv` |
| **Backend** | FastAPI, Uvicorn |
| **AI Model & SDK** | Google Gemini (`gemini-3.5-flash-lite`) via `google-genai` |
| **PDF Processing** | `pypdf` |
| **Data Validation** | Pydantic v2 |
| **Database & Migrations** | PostgreSQL (`psycopg`), SQLAlchemy 2.0, Alembic |
| **Authentication** | `PyJWT` (Bearer JWT), `pwdlib[argon2]` |
| **Deployment** | Streamlit Community Cloud (frontend), Docker / Docker Compose (containerized stack) |

---

## Installation and Local Setup

### Prerequisites

- Python 3.10 or higher
- PostgreSQL database (local instance or Docker)
- A Google Gemini API key from [Google AI Studio](https://aistudio.google.com/)

### 1. Clone the Repository

```bash
git clone https://github.com/BakhtawarTasawar/ResearchMate-AI.git
cd ResearchMate-AI
```

### 2. Backend Setup (`backend/`)

The Gemini API key, JWT secret, and database connection string are kept strictly server-side in `backend/.env` and are never exposed in frontend code.

```bash
cd backend
cp .env.example .env
```

Edit `backend/.env` and configure the required variables (do not commit `.env` or share real secrets):

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.5-flash-lite
FRONTEND_URL=http://localhost:8501

# Required by backend/app/db/database.py and backend/app/core/security.py
DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/researchmate
JWT_SECRET_KEY=replace_with_a_long_random_secret_string
```

Install dependencies, apply database migrations (if needed), and start the FastAPI server:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Verify the backend is running:
- Health check: `http://localhost:8000/api/v1/health`
- Interactive Swagger docs: `http://localhost:8000/docs`

### 3. Frontend Setup (`frontend/`)

Open a new terminal window from the repository root:

```bash
cd frontend
cp .env.example .env
```

By default, `frontend/.env` points to the local backend:

```env
BACKEND_API_URL=http://localhost:8000/api/v1
```

Install frontend dependencies and start Streamlit:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## API Documentation

All endpoints are prefixed with `/api/v1`. Protected endpoints require an `Authorization: Bearer <access_token>` header obtained from `/api/v1/auth/login`.

| Endpoint | Method | Auth Required | Purpose |
|---|---|---|---|
| `/api/v1/health` | `GET` | No | Returns backend status, API version, and configured Gemini model |
| `/api/v1/auth/register` | `POST` | No | Creates a new user account (`full_name`, `email`, `password`) |
| `/api/v1/auth/login` | `POST` | No | Authenticates user credentials and returns a Bearer JWT `access_token` |
| `/api/v1/auth/me` | `GET` | Yes | Returns the currently authenticated user's profile |
| `/api/v1/research/extract-text` | `POST` | Yes | Accepts a multipart `.pdf` or `.txt` upload (max 10 MB) and returns extracted text |
| `/api/v1/research/analyze` | `POST` | Yes | Analyzes 50–100,000 characters of scientific text and returns five structured dimensions |

### Example: `POST /api/v1/research/analyze`

**Request Body:**

```json
{
  "text": "Your scientific paper abstract or text (50 - 100,000 characters)..."
}
```

**Response (`200 OK`):**

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

---

## Running Tests

Backend tests are located in `backend/tests/` and can be run with `pytest` when installed in your backend environment:

```bash
cd backend
pytest tests/ -v
```

---

## Challenges and Solutions

- **PDF Text Extraction:** Uploaded PDFs vary widely in encoding and structure, and some files are encrypted or image-only. `DocumentExtractionService` uses `pypdf` to extract text across all pages, explicitly detects password-protected PDFs, and returns clear validation errors when no readable text is found.
- **Frontend–Backend Authentication:** In multi-user Streamlit deployments, a module-level singleton HTTP client can accidentally share or overwrite authentication tokens across sessions. `api_client.py` scopes `ResearchAPIClient` instances to `st.session_state` and resolves Bearer tokens from the active session.
- **Gemini API Availability & Transient Errors:** External LLM APIs occasionally return temporary `503` (high demand) or `429` (rate limit) errors. `ResearchAnalysisService` implements automatic retries (up to 3 total attempts with 2-second and 4-second exponential backoff) for transient SDK/network errors while failing immediately on permanent errors such as `401` or `403`.
- **Structured AI Response Handling:** Language models can occasionally wrap JSON output in Markdown code fences. The backend enforces `response_schema=AnalysisResult`, strips any code fences before `json.loads()`, and validates all required fields with Pydantic.

---

## Limitations

- **API Dependency:** Analysis requires an active internet connection and depends on Google Gemini API availability and quota limits.
- **Input & Extraction Quality:** Output accuracy depends on the clarity of the source paper and the quality of extracted text. Submitted text must be between 50 and 100,000 characters, and uploaded files are limited to 10 MB.
- **No OCR for Scanned PDFs:** Scanned, image-only PDFs do not contain selectable text and cannot be processed by `pypdf` because OCR is not currently implemented.

---

## License

Developed for the **STEM2Connect AI Hackathon 2026**.
