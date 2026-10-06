import json

from app.prompts import GAP_ANALYSIS_PROMPT
from app.services.llm_client import ask_json, extract_skills


def _norm(skill: str) -> str:
    return skill.strip().lower()


def match_skills(resume_skills: list[str], job_description: str) -> dict:
    """Compare resume skills with the job's skills and ask the LLM for a gap analysis."""
    job_skills = extract_skills(job_description)
    have = {_norm(s) for s in resume_skills}

    matched = [s for s in job_skills if _norm(s) in have]
    missing = [s for s in job_skills if _norm(s) not in have]
    score = round(100 * len(matched) / len(job_skills)) if job_skills else 0

    analysis = ask_json(
        GAP_ANALYSIS_PROMPT,
        json.dumps({'job_skills': job_skills, 'matched': matched, 'missing': missing}),
    )

    return {
        'match_score': score,
        'job_skills': job_skills,
        'matched_skills': matched,
        'missing_skills': missing,
        'summary': analysis.get('summary', ''),
        'recommendations': analysis.get('recommendations', []),
    }
