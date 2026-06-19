import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = None
index = None
docs = None


def load_resources():
    global model, index, docs

    if docs is None:
        with open(
            "data/normalized_catalog.json",
            "r",
            encoding="utf-8"
        ) as f:
            docs = json.load(f)

    if model is None:
        model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )

    if index is None:

        texts = []

        for doc in docs:

            text = f"""
            {doc['name']}
            {doc['description']}
            {' '.join(doc['categories'])}
            {' '.join(doc['job_levels'])}
            """

            texts.append(text)

        embeddings = model.encode(
            texts,
            normalize_embeddings=True
        )

        embeddings = np.array(
            embeddings,
            dtype=np.float32
        )

        dimension = embeddings.shape[1]

        index_obj = faiss.IndexFlatIP(
            dimension
        )

        index_obj.add(
            embeddings
        )

        index = index_obj


def retrieve(query, k=10):

    load_resources()

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )

    query_embedding = np.array(
        query_embedding,
        dtype=np.float32
    )

    scores, indices = index.search(
        query_embedding,
        k
    )

    results = []

    for score, idx in zip(
        scores[0],
        indices[0]
    ):
        item = docs[idx].copy()
        item["retrieval_score"] = float(score)
        results.append(item)

    return results