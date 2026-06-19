from agent.planner import build_search_queries
from agent.multi_retriever import multi_retrieve
from agent.reranker import rerank

def recommend(requirements):
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
    return shortlist