from app.prompts.templates import GAP_ANALYSIS_SYSTEM, SKILL_EXTRACTION_SYSTEM
from app.services.llm_client import chat_json


def _normalize(skill: str) -> str:
    return skill.strip().lower()


def extract_skills(text: str, source: str = "resume") -> list[str]:
    """Use the LLM to extract a de-duplicated list of skills from text."""
    result = chat_json(SKILL_EXTRACTION_SYSTEM.format(source=source), text[:12000])
    skills = result.get("technical_skills", []) + result.get("soft_skills", [])
    seen, unique = set(), []
    for skill in skills:
        key = _normalize(skill)
        if key and key not in seen:
            seen.add(key)
            unique.append(skill.strip())
    return unique


def compute_match(resume_skills: list[str], job_skills: list[str]) -> dict:
    """Compare skill lists and compute a match percentage."""
    resume_keys = {_normalize(s) for s in resume_skills}
    matched = [s for s in job_skills if _normalize(s) in resume_keys]
    missing = [s for s in job_skills if _normalize(s) not in resume_keys]
    score = round(len(matched) / len(job_skills) * 100, 1) if job_skills else 0.0
    return {"match_score": score, "matched_skills": matched, "missing_skills": missing}


def analyze(resume_text: str, job_description: str) -> dict:
    """Full pipeline: extract skills, compute match, and generate gap analysis."""
    resume_skills = extract_skills(resume_text, "resume")
    job_skills = extract_skills(job_description, "job description")
    match = compute_match(resume_skills, job_skills)

    gap = {"recommendations": [], "summary": "Great fit - no major skill gaps found."}
    if match["missing_skills"]:
        gap = chat_json(
            GAP_ANALYSIS_SYSTEM,
            f"Existing skills: {', '.join(resume_skills)}\n"
            f"Missing skills: {', '.join(match['missing_skills'])}",
        )

    return {
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        **match,
        "recommendations": gap.get("recommendations", []),
        "summary": gap.get("summary", ""),
    }
