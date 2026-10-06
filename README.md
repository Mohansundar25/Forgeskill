# Forgeskill — AI-Powered Resume–Job Matching System

Forgeskill uses **Large Language Models (LLMs)** to compare a candidate's resume with a job description. It extracts text from a PDF resume, uses AI to identify skills, calculates a match score, and generates a personalised **AI skill-gap analysis** with learning recommendations.

## 🤖 How AI Is Used

### In the product

| AI feature | What it does |
|---|---|
| **LLM skill extraction** | Structured Groq API prompts pull technical skills out of unstructured resume and job-description text and normalise them to canonical names (e.g. `JS` → `JavaScript`) |
| **AI gap analysis** | The LLM reviews matched vs. missing skills and writes a short fit assessment |
| **AI learning recommendations** | For each important missing skill, the LLM explains why it matters and how to learn it |
| **JSON-mode prompting** | Prompts force structured JSON output so AI responses are reliable to parse and display |

### In development

This project was built with **AI-assisted development**. AI coding agents were used to speed up implementation, debugging and refactoring, while I owned the architecture, prompt design, code review, API integration and cloud deployment.

## Features

- Upload a PDF resume and paste any job description
- AI extracts skills from both documents
- Match score (%) with matched and missing skills
- AI-written fit summary and learning plan for missing skills
- FastAPI backend that runs locally or serverless on AWS Lambda (via Mangum)
- React (Vite) frontend

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite |
| Backend | Python, FastAPI |
| AI / LLM | Groq API (Llama 3.3 70B), structured JSON prompts |
| PDF parsing | pypdf |
| Cloud | AWS Lambda, API Gateway, Mangum |

## Architecture

```
React Frontend
      │  (PDF resume + job description)
      ▼
AWS API Gateway
      │
      ▼
AWS Lambda (FastAPI + Mangum)
      │
      ├── PDF text extraction (pypdf)
      ├── 🤖 LLM skill extraction (Groq)
      ├── Match score calculation
      └── 🤖 LLM gap analysis + recommendations (Groq)
      │
      ▼
JSON response → React UI
```

## Project Structure

```
Forgeskill/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app + routes
│   │   ├── prompts.py           # AI prompt templates
│   │   └── services/
│   │       ├── pdf_parser.py    # Resume text extraction
│   │       ├── llm_client.py    # Groq LLM client + skill extraction
│   │       └── matcher.py       # Match score + AI gap analysis
│   ├── handler.py               # AWS Lambda handler (Mangum)
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/ (App.jsx, main.jsx, styles.css)
│   ├── index.html
│   └── package.json
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- A free Groq API key from https://console.groq.com

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # then add your GROQ_API_KEY
uvicorn app.main:app --reload
```

Interactive API docs: http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/analyze` | Upload a PDF + job description → AI skills, match score, gap analysis |
| POST | `/api/upload-resume` | Upload a PDF resume → AI-extracted skills |
| POST | `/api/match` | Compare a skill list with a job description |
| GET | `/api/health` | Health check |

## Deploying to AWS Lambda

1. Install dependencies into a folder: `pip install -r requirements.txt -t package/`
2. Copy `app/` and `handler.py` into `package/` and zip it.
3. Create a Lambda function (Python 3.11), upload the zip, set the handler to `handler.handler`.
4. Add `GROQ_API_KEY` as a Lambda environment variable.
5. Create an API Gateway HTTP API pointing to the function.
6. Set `VITE_API_URL` in the frontend to the API Gateway URL.

## Future Improvements

- AI-generated tailored resume bullet points for a specific job
- Rank multiple job descriptions against one resume
- DOCX resume support
- Embedding-based semantic skill matching

## Author

**Mohana Sundaram B** · GitHub: [Mohansundar25](https://github.com/Mohansundar25)
