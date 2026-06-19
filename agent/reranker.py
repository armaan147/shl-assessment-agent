import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def rerank(requirements, candidates):
    try:
        candidate_text = ""
        for idx, c in enumerate(candidates):
            candidate_text += f"""
ID: {c['id']}
NAME: {c['name']}
CATEGORY: {', '.join(c['categories'])}
DESCRIPTION: {c['description'][:400]}
---
"""
        prompt = f"""
You are an SHL assessment recommendation expert.
Hiring Requirements:

{json.dumps(requirements, indent=2)}

Available Assessments:

{candidate_text}

Select the BEST 5 assessments.
Rules:
1. Prefer a balanced assessment package.
2. Include technical skills assessments if relevant.
3. Include cognitive ability assessments if relevant.
4. Include personality assessments when communication, collaboration, leadership, or stakeholder interaction is important.
5. Return EXACTLY 5 assessment IDs.
6. Only use IDs from the provided list.
7. Avoid selecting multiple assessments that measure nearly identical technical skills.
8. Prefer diversity across categories.
9. Select at most 2 assessments from Knowledge & Skills.
10. Include Personality & Behavior when stakeholder interaction is important.
11. Include Ability & Aptitude when assessing professional roles.
12. Include Simulations when available and relevant.

Return ONLY valid JSON.

Schema:
{{
    "selected_ids": []
}}
"""

        response = model.generate_content(prompt)

        text = response.text.strip()

        print("\n=== GEMINI RAW RESPONSE ===\n")
        print(text)
        print("\n===========================\n")

        text = text.replace("```json", "")
        text = text.replace("```", "")

        result = json.loads(text)

        selected_ids = {
            str(x)
            for x in result["selected_ids"]
        }

        final = []

        for c in candidates:

            if c["id"] in selected_ids:
                final.append(c)

        if len(final) > 0:
            return final

        return candidates[:5]

    except Exception as e:

        print("\n=== RERANKER ERROR ===")
        print(e)
        print("======================\n")

        return candidates[:5]