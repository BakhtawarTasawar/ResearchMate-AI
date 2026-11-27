# ResearchMate AI
### AI-Powered Scientific Research Assistant

ResearchMate AI is a web-based scientific research assistant developed for the **STEM2Connect AI Hackathon 2026**.

We built ResearchMate AI to make scientific literature easier to understand and review. It takes research papers and abstracts and organizes their key information into five structured dimensions, helping students and researchers identify the main ideas, objectives, findings, and potential directions for further research.

The application combines Google Gemini, FastAPI, Streamlit, and PostgreSQL to provide an accessible research analysis workflow.

## Live Demo

- **Application:** [ResearchMate AI](https://researchmate-ai-project.streamlit.app/)
- **GitHub Repository:** [ResearchMate-AI](https://github.com/BakhtawarTasawar/ResearchMate-AI)

## The Problem

Scientific papers often contain dense technical language, complex methodologies, statistical results, and detailed conclusions. Reviewing multiple papers can take considerable time, especially when we need to identify the most relevant information before moving forward with our research.

We developed ResearchMate AI to simplify this initial review process.

Rather than returning a general conversational response, the application organizes the submitted research into five consistent sections. This gives users a clearer starting point for understanding a paper and deciding which parts deserve closer attention.

## What We Built

ResearchMate AI provides the following functionality:

- **Research Text Analysis:** Submit scientific abstracts or research text directly through the application.
- **PDF and TXT Uploads:** Upload research documents for server-side text extraction.
- **Structured AI Analysis:** Generate five research dimensions using Google Gemini.
- **User Authentication:** Register, log in, and access protected research functionality.
- **Input Validation:** Validate submitted content, supported file formats, and file size.
- **API-Based Architecture:** Keep frontend functionality separate from backend processing.
- **Structured Responses:** Validate AI-generated output using Pydantic schemas.

## Five Research Dimensions

Each submitted paper is analyzed across five sections:

| # | Dimension | Description |
|---|---|---|
| 1 | **Simple Summary** | A plain-language explanation of the research problem, methodology, and conclusion. |
| 2 | **Research Objectives** | The main hypotheses, research questions, and objectives of the study. |
| 3 | **Key Findings** | Important results, empirical observations, statistical outcomes, and comparisons. |
| 4 | **Important Keywords** | 4–10 relevant scientific concepts and technical terms. |
| 5 | **Future Research Questions** | Unresolved questions, study limitations, and possible directions for further research. |

The generated analysis is intended to support the reading process, not replace the original research paper or independent academic evaluation.

## How It Works

1. **Registration and Login:** Users create an account or sign in to access the research workspace.
2. **Submit Research:** Users paste an abstract or upload a PDF/TXT document.
3. **Text Extraction:** The backend extracts readable content from uploaded documents.
4. **Validation:** The submitted content is checked for supported formats and input requirements.
5. **AI Processing:** The backend sends the research content to Google Gemini using structured prompts.
6. **Response Validation:** The generated response is checked against predefined Pydantic schemas.
7. **Results:** The frontend displays the analysis across the five research dimensions.

## Technical Architecture

We use a decoupled architecture in which the frontend and backend have separate responsibilities.

- **Frontend:** Streamlit manages the user interface, navigation, authentication state, file submission, and results presentation.
- **Backend:** FastAPI handles authentication, API requests, input validation, document extraction, database access, and AI processing.
- **Database:** PostgreSQL stores user account information. SQLAlchemy manages database interactions, while Alembic handles migrations.
- **AI Integration:** Google Gemini generates structured research analysis through the Google GenAI SDK.

### Project Structure

```text
ResearchMate-AI/
│
├── frontend/
│   ├── app.py
│   ├── pages/
│   │   ├── auth.py
│   │   ├── home.py
│   │   ├── analyze.py
│   │   └── about.py
│   ├── components/
│   │   └── ui.py
│   ├── services/
│   │   └── api_client.py
│   ├── utils/
│   │   ├── session.py
│   │   └── icons.py
│   ├── styles/
│   │   └── styles.css
│   ├── assets/
│   ├── config/
│   │   └── settings.py
│   └── requirements.txt
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── auth.py
│   │   │       ├── health.py
│   │   │       └── research.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── logging.py
│   │   │   └── security.py
│   │   ├── db/
│   │   │   ├── database.py
│   │   │   └── models.py
│   │   ├── dependencies/
│   │   ├── schemas/
│   │   │   └── research.py
│   │   └── services/
│   │       ├── gemini_client.py
│   │       ├── prompts.py
│   │       ├── research_service.py
│   │       └── extraction_service.py
│   ├── migrations/
│   ├── tests/
│   └── requirements.txt
│
├── .streamlit/
├── docker-compose.yml
├── .env.example
└── README.md
```

### Core Components

**Frontend — Streamlit**

Provides the user-facing application, authentication workflows, page navigation, file uploads, and research result presentation. It communicates with the backend through HTTP requests.

**Backend — FastAPI**

Provides versioned REST API endpoints for authentication, health checks, document extraction, and research analysis. It also manages database sessions and coordinates AI processing.

**AI Processing — Google Gemini**

We integrated `gemini-3.5-flash-lite` through the `google-genai` SDK. Structured prompts guide the model to return the five research dimensions in a consistent format. The Gemini API key is kept on the backend.

**Document Extraction — pypdf**

Uploaded PDF documents are processed server-side using `pypdf`. The extraction service handles multi-page documents and validates encrypted, empty, or image-only PDFs. TXT files are decoded using UTF-8 with a Latin-1 fallback.

**Authentication and Security**

User passwords are hashed using Argon2 through `pwdlib`. JWT access tokens are handled using PyJWT. Protected API requests require valid authentication, and frontend API client instances are maintained in Streamlit session state.

**Response Validation — Pydantic**

AI responses are validated against the `AnalysisResult` schema using Pydantic v2. The backend also handles accidental Markdown code fences before parsing generated JSON.

## Technology Stack

| Area | Technology |
|---|---|
| Language | Python |
| Frontend | Streamlit |
| HTTP Client | HTTPX |
| Backend | FastAPI, Uvicorn |
| AI Model | Google Gemini (`gemini-3.5-flash-lite`) |
| AI SDK | Google GenAI |
| Document Processing | pypdf |
| Validation | Pydantic v2 |
| Database | PostgreSQL |
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic |
| Authentication | PyJWT, pwdlib (Argon2) |
| Containerization | Docker, Docker Compose |
| Testing | Pytest |

## Getting Started

### Prerequisites

- Python 3.10 or higher
- PostgreSQL or Docker with Docker Compose
- Google Gemini API key from [Google AI Studio](https://aistudio.google.com/)
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/BakhtawarTasawar/ResearchMate-AI.git
cd ResearchMate-AI
```

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create the environment file:

```bash
cp .env.example .env
```

Configure the required variables in `backend/.env`:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.5-flash-lite
FRONTEND_URL=http://localhost:8501

DATABASE_URL=your_postgresql_connection_string
JWT_SECRET_KEY=your_long_random_secret
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the backend:

```bash
uvicorn app.main:app --reload --port 8000
```

The backend will be available at:

- Health check: http://localhost:8000/api/v1/health
- Swagger documentation: http://localhost:8000/docs

### 3. Frontend Setup

Open another terminal from the repository root:

```bash
cd frontend
```

Create the environment file:

```bash
cp .env.example .env
```

Configure the backend URL:

```env
BACKEND_API_URL=http://localhost:8000/api/v1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run Streamlit:

```bash
streamlit run app.py
```

Open the application at:

http://localhost:8501

### 4. Docker Setup

We also provide a Docker Compose configuration to run the PostgreSQL database, FastAPI backend, and Streamlit frontend as separate services.

From the repository root:

```bash
docker compose up --build
```

To stop the services:

```bash
docker compose down
```

The PostgreSQL data is stored in a persistent Docker volume.

**Security:** Real API keys, database passwords, JWT secrets, and production credentials must be configured through environment variables. They should never be committed to the repository.

## API Documentation

All API endpoints use the `/api/v1` prefix.

Protected endpoints require a valid Bearer access token obtained through the login endpoint.

| Endpoint | Method | Authentication | Description |
|---|---|---|---|
| `/api/v1/health` | GET | No | Checks backend availability. |
| `/api/v1/auth/register` | POST | No | Creates a new user account. |
| `/api/v1/auth/login` | POST | No | Authenticates a user and returns an access token. |
| `/api/v1/auth/me` | GET | Yes | Returns the authenticated user's profile. |
| `/api/v1/research/extract-text` | POST | Yes | Extracts text from PDF or TXT uploads. |
| `/api/v1/research/analyze` | POST | Yes | Analyzes submitted scientific text. |

### Research Analysis Example

**Endpoint:** `POST /api/v1/research/analyze`

Request:

```json
{
  "text": "Scientific paper abstract or research text..."
}
```

The endpoint accepts research text between 50 and 100,000 characters.

Example response:

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

## Testing

Backend tests are located in `backend/tests/`.

Run the test suite with:

```bash
cd backend
pytest tests/ -v
```

## Challenges We Addressed

### PDF Text Extraction

PDF files vary in layout, encoding, and structure. Some are encrypted or contain scanned images instead of selectable text. We implemented server-side extraction with `pypdf` and validation to handle documents that do not contain readable text.

### Authentication Across User Sessions

Streamlit serves multiple user sessions through the same application process. A shared HTTP client could cause authentication state to overlap between users. We scoped API client instances to individual Streamlit sessions and resolve Bearer tokens from the active session.

### External AI Service Errors

Gemini requests can fail because of temporary service interruptions, network issues, or rate limits. We implemented retry handling for transient failures, with up to three attempts and increasing delays between retries. Permanent errors, such as authentication and permission failures, are not repeatedly retried.

### Consistent AI Responses

Language models can return unexpected formatting, including JSON wrapped in Markdown code fences. We handle this formatting and validate the resulting data against predefined Pydantic schemas before returning it to the frontend.

## Current Limitations

- **Gemini API Dependency:** Research analysis requires an internet connection and depends on Google Gemini availability and quota limits.
- **Input Length:** Submitted research text must contain between 50 and 100,000 characters.
- **File Size:** Uploaded documents are limited to 10 MB.
- **Scanned PDFs:** OCR is not currently implemented, so image-only PDFs cannot be processed as readable text.
- **Source Quality:** The quality of generated analysis depends on the clarity and completeness of the submitted research content.

## Project Information

**Project:** ResearchMate AI  
**Hackathon:** STEM2Connect AI Hackathon 2026  
**Live Application:** https://researchmate-ai-project.streamlit.app/  
**Repository:** https://github.com/BakhtawarTasawar/ResearchMate-AI

We developed ResearchMate AI to make the initial review of scientific literature more organized and accessible. By combining document extraction, authentication, API-based backend processing, and generative AI, we brought these capabilities together in one focused research workflow.

**Developed for the STEM2Connect AI Hackathon 2026.**
