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

    return {
        "score": score,
        "matching": matching,
        "missing": missing
    }