from retrieval.retriever import retrieve

def multi_retrieve(
    queries,
    k=20):

    fused = {}
    for query in queries:
        items = retrieve(
            query,
            k=k
        )
        for rank, item in enumerate(items, start=1):
            score = 1 / (60 + rank)
            if item["id"] not in fused:
                fused[item["id"]] = {
                    "item": item,
                    "score": 0
                }
            fused[item["id"]]["score"] += score
    results = sorted(
        fused.values(),
        key=lambda x: x["score"],
        reverse=True
    )
    return [
        x["item"]
        for x in results
    ]