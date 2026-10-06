import os

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, File, Form, HTTPException, UploadFile  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402

from app.services.matcher import analyze, extract_skills  # noqa: E402
from app.services.pdf_parser import extract_text_from_pdf  # noqa: E402

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

app = FastAPI(title="Forgeskill API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)


async def _read_resume(file: UploadFile) -> str:
    if not (file.filename or "").lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")
    data = await file.read()
    if len(data) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File is larger than 5 MB.")
    try:
        return extract_text_from_pdf(data)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    text = await _read_resume(file)
    try:
        skills = extract_skills(text, "resume")
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"LLM error: {exc}")
    return {"filename": file.filename, "characters": len(text), "skills": skills}


@app.post("/api/match")
async def match(file: UploadFile = File(...), job_description: str = Form(...)):
    if len(job_description.strip()) < 20:
        raise HTTPException(status_code=400, detail="Job description is too short.")
    text = await _read_resume(file)
    try:
        return analyze(text, job_description)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"LLM error: {exc}")
