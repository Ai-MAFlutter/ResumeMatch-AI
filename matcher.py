import re

SKILLS = [
    "Python",
    "FastAPI",
    "Flask",
    "Django",
    "SQL",
    "Git",
    "Docker",
    "REST API",
    "Machine Learning",
    "Pandas",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "Flutter",
    "Dart",
    "Provider",
    "Bloc"
]


def extract_skills(text):

    found = []

    text = text.lower()

    for skill in SKILLS:
        if skill.lower() in text:
            found.append(skill)

    return sorted(set(found))


def compare_skills(resume_text, job_text):

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)

    matching = sorted(set(resume_skills) & set(job_skills))
    missing = sorted(set(job_skills) - set(resume_skills))

    if len(job_skills) == 0:
        score = 0
    else:
        score = round(len(matching) / len(job_skills) * 100)

        # Skill Category Scores

    skill_scores = {

        "Python": 0,

        "AI": 0,

        "RAG": 0,

        "Backend": 0,

        "Data": 0,

        "Flutter": 0

    }


    for skill in matching:

        skill_lower = skill.lower()


        if "python" in skill_lower:
            skill_scores["Python"] = 90


        elif "ai" in skill_lower or "machine learning" in skill_lower:
            skill_scores["AI"] = 85


        elif "rag" in skill_lower or "llm" in skill_lower:
            skill_scores["RAG"] = 85


        elif "fastapi" in skill_lower or "django" in skill_lower:
            skill_scores["Backend"] = 80


        elif "pandas" in skill_lower or "numpy" in skill_lower:
            skill_scores["Data"] = 75


        elif "flutter" in skill_lower or "dart" in skill_lower:
            skill_scores["Flutter"] = 80



    return {

        "score": score,

        "matching": matching,

        "missing": missing,

        "skill_scores": skill_scores

    }