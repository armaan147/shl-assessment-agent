from fastapi import FastAPI
from app.schemas import (ChatRequest, ChatResponse)
from agent.extractor import (extract_requirements)
from agent.planner import (build_search_queries)
from agent.multi_retriever import (multi_retrieve)
from agent.reranker import (rerank)
from agent.formatter import (format_recommendations)
from agent.decision import decide_action
from agent.catalog import find_assessment
from agent.comparator import compare_assessments

app = FastAPI()

@app.get("/health")
def health():
    return {
        "status": "ok"
    }

@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest):

    messages = [
        m.model_dump()
        for m in request.messages
    ]

    requirements = extract_requirements(
        messages
    )

    latest_message = messages[-1]["content"]

    action = decide_action(
    latest_message,
    requirements
)


    if action == "REFUSE":
        return {
            "reply":
            "I can only assist with SHL assessment recommendations and assessment comparisons.",
            "recommendations": [],
            "end_of_conversation": False
        }


    if action == "CLARIFY":

        return {
            "reply":
            "What role are you hiring for?",
            "recommendations": [],
            "end_of_conversation": False
        }


    if action == "COMPARE":
        names = requirements.get(
            "assessment_names",
            []
        )
        if len(names) < 2:
            return {
                "reply":
                "Please specify two assessments to compare.",
                "recommendations": [],
                "end_of_conversation": False
            }
        a = find_assessment(names[0])
        b = find_assessment(names[1])
        if a is None or b is None:
            return {
                "reply":
                "I couldn't find one or both assessments in the catalog.",
                "recommendations": [],
                "end_of_conversation": False
            }
        comparison = compare_assessments(
            a,
            b
        )
        return {
            "reply": comparison,
            "recommendations": [],
            "end_of_conversation": False
        }


    queries = build_search_queries(
        requirements
    )
    candidates = multi_retrieve(
        queries
    )
    shortlist = rerank(
        requirements,
        candidates
    )
    return {
        "reply":
        "Here are the recommended assessments.",

        "recommendations":
        format_recommendations(
            shortlist
        ),

        "end_of_conversation":
        False
    }