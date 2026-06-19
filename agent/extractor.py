import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY") )

model = genai.GenerativeModel("gemini-2.5-flash")

def extract_requirements(messages):
    conversation = "\n".join(
        [
            f"{m['role']}: {m['content']}"
            for m in messages
        ]
    )

    prompt = f"""
You are an information extraction system.
Extract hiring requirements from the conversation.
Return ONLY valid JSON.

Important Rules:
1. Use the FULL conversation history.
2. If a later message adds constraints, keep previously extracted role, skills and seniority.
3. Only set compare_request=true when the user explicitly asks to compare assessments.
4. Only populate assessment_names when compare_request=true.
5. If role or hiring target was identified earlier in the conversation, enough_information should remain true.
6. Do not invent assessment names.
7. Do not invent skills.
8. Return JSON only.
9. When a later message modifies requirements, preserve previously extracted skills unless the user explicitly changes them.
10. For technical roles, infer core skills from the role if they were identified earlier in the conversation.

Allowed seniority values:
- Entry-Level
- Graduate
- Mid-Professional
- Professional Individual Contributor
- Supervisor
- Front Line Manager
- Manager
- Director
- Executive
- General Population

Map experience to seniority:
0-1 years -> Entry-Level
2-5 years -> Mid-Professional
6-10 years -> Manager
10+ years -> Director or Executive

Schema:
{{
  "role": "",
  "seniority": "",
  "skills": [],
  "needs_personality": false,
  "stakeholder_interaction": false,
  "enough_information": false,
  "compare_request": false,
  "assessment_names": [],
  "off_topic": false
}}

Conversation:
{conversation}
"""
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        text = text.replace("```json", "")
        text = text.replace("```", "")
        return json.loads(text)

    except Exception as e:
        print("EXTRACTOR ERROR:", e)
        return {
            "role": "",
            "seniority": "",
            "skills": [],
            "needs_personality": False,
            "stakeholder_interaction": False,
            "enough_information": False,
            "compare_request": False,
            "assessment_names": [],
            "off_topic": False
        }
    