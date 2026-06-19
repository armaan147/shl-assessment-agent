import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)
model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def compare_assessments(
    assessment_a,
    assessment_b
):
    prompt = f"""
You are an SHL assessment expert.
Compare these assessments.
Assessment A:
Name:
{assessment_a['name']}
Categories:
{assessment_a['categories']}
Job Levels:
{assessment_a['job_levels']}
Description:
{assessment_a['description']}
--------------------------------

Assessment B:
Name:
{assessment_b['name']}
Categories:
{assessment_b['categories']}
Job Levels:
{assessment_b['job_levels']}
Description:
{assessment_b['description']}
--------------------------------

Provide:
1. Purpose
2. Key differences
3. When to use A
4. When to use B

Keep it concise.
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("COMPARATOR ERROR:", e)
        return (
            "Comparison service temporarily unavailable. "
            "Please try again later."
        )