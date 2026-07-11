from openai import OpenAI
import os
from dotenv import load_dotenv

from matcher import compare_skills


# =====================================================
# LOAD ENV
# =====================================================

load_dotenv()


# =====================================================
# GROQ CLIENT
# =====================================================

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


# =====================================================
# AI INSTRUCTIONS
# =====================================================

INSTRUCTIONS = """
You are ResumeMatch AI, an expert resume assistant.

Your job is to answer questions about the uploaded resume.

Rules:

- Use the provided resume context as the main source.
- Answer professionally and clearly.
- If the answer is partially available, explain what is available.
- Do not invent skills, projects, or experience.
- If the information does not exist, say:
  "This information is not available in the uploaded resume."

Never answer only with:
"I don't know."
"""


# =====================================================
# PROMPTS
# =====================================================

PROMPT_TEMPLATE = """
Resume Context:

{context}


User Question:

{question}


Answer based only on the resume context.
"""


PROMPT_TEMPLATE = """
Resume Context:

{context}


Job Description:

{job}


User Question:

{question}


Answer based on the resume and job description.
Give specific recommendations.
"""


ANALYSIS_PROMPT = """
You are a professional AI Career Advisor.

Create a professional resume evaluation report.


Resume Match Score:

{score}%


Matching Skills:

{matching}


Missing Skills:

{missing}


Job Description:

{job}



Return:

## Overall Evaluation

## Strengths

## Missing Skills

## Learning Roadmap

## Final Recommendation


Keep the report concise and professional.
"""


# =====================================================
# BUILD CONTEXT
# =====================================================

def build_context(search_results):

    if not search_results:

        return "No resume information was found."


    context = ""


    for i, result in enumerate(search_results, start=1):

        context += f"""
Resume Section {i}:

{result.get("content","")}

"""


    return context



# =====================================================
# BUILD QUESTION PROMPT
# =====================================================

def build_prompt(question, search_results, job_description):

    context = build_context(search_results)


    return PROMPT_TEMPLATE.format(
    question=question,
    context=context,
    job=job_description
)


# =====================================================
# LLM CALL
# =====================================================

def llm(
    prompt,
    model="llama-3.3-70b-versatile"
):

    messages = [

        {
            "role":"system",
            "content":INSTRUCTIONS
        },

        {
            "role":"user",
            "content":prompt
        }

    ]


    response = client.chat.completions.create(

        model=model,

        messages=messages,

        temperature=0

    )


    return response.choices[0].message.content
# =====================================================
# ASK RESUME
# =====================================================

def ask_resume(question, index, job_description=""):
    search_results = index.search(

        question,

        num_results=5

    )


    prompt = build_prompt(
    question,
    search_results,
    job_description
)

    return llm(prompt)



# =====================================================
# BUILD MATCH PROMPT
# =====================================================

def build_match_prompt(

    question,

    resume_context,

    job_description

):

    return MATCH_PROMPT_TEMPLATE.format(

        resume=resume_context,

        job=job_description,

        question=question

    )



# =====================================================
# COMPARE RESUME WITH JOB
# =====================================================

def compare_resume(

    question,

    resume_text,

    job_description

):

    prompt = build_match_prompt(

        question,

        resume_text,

        job_description

    )


    return llm(prompt)



# =====================================================
# ANALYZE RESUME
# =====================================================

def analyze_resume(

    resume_text,

    job_description

):


    # Calculate ATS score and skills

    result = compare_skills(

        resume_text,

        job_description

    )


    # Generate AI report

    prompt = ANALYSIS_PROMPT.format(

        score=result["score"],

        matching="\n".join(

            result["matching"]

        ),

        missing="\n".join(

            result["missing"]

        ),

        job=job_description

    )


    report = llm(prompt)



    return {

    "score": result["score"],

    "matching": result["matching"],

    "missing": result["missing"],

    "skill_scores": result["skill_scores"],

    "report": report

}