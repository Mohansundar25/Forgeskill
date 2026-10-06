from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.services.llm_client import extract_skills
from app.services.matcher import match_skills
from app.services.pdf_parser import extract_text

app = FastAPI(title='Forgeskill API', version='1.0.0')
app.add_middleware(
    CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*']
)


class MatchRequest(BaseModel):
    resume_skills: list[str]
    job_description: str


async def _read_pdf(file: UploadFile) -> str:
    if not (file.filename or '').lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail='Only PDF files are supported')
    text = extract_text(await file.read())
    if not text.strip():
        raise HTTPException(status_code=422, detail='Could not extract text from the PDF')
    return text


@app.get('/api/health')
def health():
    return {'status': 'ok'}


@app.post('/api/upload-resume')
async def upload_resume(file: UploadFile = File(...)):
    text = await _read_pdf(file)
    return {'skills': extract_skills(text)}


@app.post('/api/match')
def match(req: MatchRequest):
    if not req.job_description.strip():
        raise HTTPException(status_code=400, detail='Job description is required')
    return match_skills(req.resume_skills, req.job_description)


@app.post('/api/analyze')
async def analyze(file: UploadFile = File(...), job_description: str = Form(...)):
    """One-shot endpoint: PDF resume + job description -> AI skills, score and gap analysis."""
    text = await _read_pdf(file)
    resume_skills = extract_skills(text)
    return {'resume_skills': resume_skills, **match_skills(resume_skills, job_description)}
