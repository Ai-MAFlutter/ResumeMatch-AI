from openai import OpenAI
import os
from dotenv import load_dotenv

from matcher import compare_skills


load_dotenv()


client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)



INSTRUCTIONS = """
You are an AI Resume Assistant.

Answer ONLY using the provided resume context.

If the answer is not found in the resume,
reply with:

I don't know.
"""



PROMPT_TEMPLATE = """
Question:
{question}

Resume:
{context}
"""



MATCH_PROMPT_TEMPLATE = """
You are an expert AI Resume Reviewer.

Your task is to compare the candidate's resume with the job description.

Resume:
{resume}

Job Description:
{job}

Question:
{question}

Analyze the resume carefully.

Return your answer using exactly this format:

Resume Match Score: <0-100>

Matching Skills:
- ...
- ...
- ...

Missing Skills:
- ...
- ...
- ...

Recommendations:
- ...
- ...
- ...

Important Rules:
- Base your analysis only on the provided resume and job description.
- If a required skill is missing, list it under Missing Skills.
- Do NOT answer with "I don't know".
- Always provide a complete analysis.
"""



ANALYSIS_PROMPT = """
You are a professional AI Career Advisor.

Based on the following resume analysis, write a professional report.

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


Keep the report professional and concise.
"""



def build_context(search_results):

    context = ""

    for result in search_results:
        context += result["content"]
        context += "\n\n"

    return context




def build_prompt(question, search_results):

    context = build_context(search_results)

    return PROMPT_TEMPLATE.format(
        question=question,
        context=context
    )




def llm(prompt, model="llama-3.3-70b-versatile"):

    messages = [
        {
            "role": "system",
            "content": INSTRUCTIONS
        },
        {
            "role": "user",
            "content": prompt
        }
    ]


    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )


    return response.choices[0].message.content





def ask_resume(question, index):

    search_results = index.search(
        question,
        num_results=3
    )


    prompt = build_prompt(
        question,
        search_results
    )


    return llm(prompt)






def build_match_prompt(question, resume_context, job_description):

    return MATCH_PROMPT_TEMPLATE.format(
        resume=resume_context,
        job=job_description,
        question=question
    )






def compare_resume(question, resume_text, job_description):

    prompt = build_match_prompt(
        question,
        resume_text,
        job_description
    )


    return llm(prompt)






def analyze_resume(resume_text, job_description):

    # حساب الـ score والمهارات
    result = compare_skills(
        resume_text,
        job_description
    )


    # إنشاء تقرير AI
    prompt = ANALYSIS_PROMPT.format(
        score=result["score"],
        matching="\n".join(result["matching"]),
        missing="\n".join(result["missing"]),
        job=job_description
    )


    report = llm(prompt)



    # نرجع كل البيانات للواجهة
    return {
        "score": result["score"],
        "matching": result["matching"],
        "missing": result["missing"],
        "report": report
    }