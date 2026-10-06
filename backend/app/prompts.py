"""Prompt templates used by the AI features."""

SKILL_EXTRACTION_PROMPT = (
    'You are an expert technical recruiter. Extract the skills mentioned in the text. '
    'Respond ONLY with JSON in the form {"skills": ["..."]}. Rules: include programming languages, '
    'frameworks, libraries, cloud services, databases, tools and engineering practices; use canonical '
    'names (e.g. "JavaScript", "AWS Lambda", "PostgreSQL"); no duplicates; at most 40 skills.'
)

GAP_ANALYSIS_PROMPT = (
    'You are a career coach for software engineers. You receive the skills a job requires, the skills '
    'the candidate matches and the skills they are missing. Respond ONLY with JSON in the form '
    '{"summary": "2-3 sentence fit assessment", "recommendations": '
    '[{"skill": "...", "why": "why it matters for this job", "how_to_learn": "a concrete next step"}]}. '
    'Cover the most important missing skills first, at most 6 recommendations.'
)
