# Forgeskill — LLM-Powered Resume–Job Matching System

Forgeskill compares a candidate's resume with a job description and shows how well they match. It extracts text from a PDF resume, identifies skills using structured Groq API prompts, calculates a match score, and generates a skill-gap analysis with learning recommendations.

## Features

- **PDF resume parsing:** extracts text from uploaded resumes
- **Skill extraction:** structured Groq API prompts identify technical and soft skills
- **Job matching:** compares resume skills against a job description and returns a match score
- **Skill-gap analysis:** lists missing skills with tips on how to learn them
- **Serverless-ready backend:** FastAPI app wrapped with Mangum for AWS Lambda + API Gateway
- **React frontend:** upload a resume, paste a job description, view results

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React (Vite) |
| Backend | Python, FastAPI |
| AI / LLM | Groq API (structured JSON prompts) |
| Cloud | AWS Lambda, API Gateway (via Mangum) |
| PDF parsing | pypdf |

## Architecture

```
React Frontend
      │  (upload resume + job description)
      ▼
AWS API Gateway
      │
      ▼
AWS Lambda (FastAPI + Mangum)
      │
      ├── PDF Text Extraction (pypdf)
      ├── Skill Extraction (Groq API)
      └── Match Score + Skill-Gap Analysis (Groq API)
      │
      ▼
JSON response → React UI
```

## Project Structure

```
Forgeskill/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI app + routes
│   │   ├── services/
│   │   │   ├── pdf_parser.py  # Resume text extraction
│   │   │   ├── llm_client.py  # Groq API client
│   │   │   └── matcher.py     # Skill extraction, match score, gap analysis
│   │   └── prompts/
│   │       └── templates.py   # Structured prompt templates
│   ├── handler.py             # AWS Lambda entry point (Mangum)
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- A Groq API key (https://console.groq.com)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # then add your GROQ_API_KEY
uvicorn app.main:app --reload
```

Interactive API docs: `http://localhost:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. Set `VITE_API_URL` in `frontend/.env` if your API is not on `http://localhost:8000`.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Health check |
| POST | `/api/upload-resume` | Upload a PDF resume (`file`) and get extracted skills |
| POST | `/api/match` | Upload a PDF resume (`file`) + `job_description` and get match score and skill gaps |

Example:

```bash
curl -X POST http://localhost:8000/api/match \
  -F "file=@resume.pdf" \
  -F "job_description=Looking for a Python developer with FastAPI, AWS and Docker experience"
```

## Deployment (AWS Lambda)

1. Install dependencies into a package folder: `pip install -r requirements.txt -t package/`
2. Copy `app/` and `handler.py` into `package/` and zip its contents.
3. Create a Lambda function (Python 3.11) with handler `handler.handler` and upload the zip.
4. Add `GROQ_API_KEY` as a Lambda environment variable.
5. Create an API Gateway HTTP API that proxies all routes to the Lambda.
6. Set `VITE_API_URL` in the frontend to the API Gateway URL and deploy the frontend (S3, Netlify, or Vercel).

## Future Improvements

- Support DOCX resumes
- Rank multiple job descriptions at once
- Save match history per user
- Suggest specific courses for missing skills

## Author

**Mohana Sundaram B**  
GitHub: [Mohansundar25](https://github.com/Mohansundar25)
