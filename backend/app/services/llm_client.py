import json
import os

from dotenv import load_dotenv
from groq import Groq

from app.prompts import SKILL_EXTRACTION_PROMPT

load_dotenv()

MODEL = os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')
_client = None


def get_client() -> Groq:
    global _client
    if _client is None:
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            raise RuntimeError('GROQ_API_KEY is not set')
        _client = Groq(api_key=api_key)
    return _client


def ask_json(system_prompt: str, user_content: str) -> dict:
    """Send a prompt to the LLM and parse its JSON response."""
    response = get_client().chat.completions.create(
        model=MODEL,
        temperature=0.1,
        response_format={'type': 'json_object'},
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_content},
        ],
    )
    return json.loads(response.choices[0].message.content)


def extract_skills(text: str) -> list[str]:
    """Use the LLM to extract a de-duplicated list of skills from free text."""
    data = ask_json(SKILL_EXTRACTION_PROMPT, text[:12000])
    seen, skills = set(), []
    for skill in data.get('skills', []):
        name = str(skill).strip()
        if name and name.lower() not in seen:
            seen.add(name.lower())
            skills.append(name)
    return skills
