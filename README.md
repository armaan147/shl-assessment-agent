---
title: SHL Assessment Agent
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# SHL Assessment Recommendation Agent
## Overview
This project is an AI-powered conversational assessment recommendation system built for the SHL AI Intern Take-Home Assignment.
The system helps hiring managers identify relevant SHL assessments through natural language conversations. It supports clarification, recommendation, refinement, comparison, and refusal behaviors while ensuring recommendations are restricted to the SHL assessment catalog.
---

## Features
* Conversational assessment recommendation
* Assessment comparison
* Clarification for vague queries
* Multi-turn conversation support
* Off-topic query refusal
* Semantic retrieval using FAISS
* LLM-based requirement extraction
* LLM-based reranking
---

## Architecture
User Query
↓
Requirement Extraction (Gemini 2.5 Flash)
↓
Decision Engine
↓
Query Planning
↓
Multi-Query Retrieval (FAISS + BGE Embeddings)
↓
Reciprocal Rank Fusion (RRF)
↓
Gemini Reranker
↓
Final Recommendations
---

## Technologies Used
* FastAPI
* Google Gemini 2.5 Flash
* Sentence Transformers (BAAI/bge-small-en-v1.5)
* FAISS
* Python
---

## Setup
Install dependencies:
```bash
pip install -r requirements.txt
```

Create environment variables:
```bash
cp .env.example .env
```

Add your Gemini API key:
```env
GEMINI_API_KEY=your_api_key_here
```
---

## Run
```bash
uvicorn app.main:app --reload
```
---

## API Endpoints
### Health Check
GET /health
Response:

```json
{
  "status": "ok"
}
```

### Chat
POST /chat
Example Request:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hiring a Java developer with 4 years experience"
    }
  ]
}
```

Example Response:

```json
{
  "reply": "Here are the recommended assessments.",
  "recommendations": [
    {
      "name": "Java Frameworks (New)",
      "url": "https://www.shl.com/..."
    }
  ],
  "end_of_conversation": false
}
```
---

## Project Structure
app/
* FastAPI application and schemas
agent/
* Extraction, planning, reranking, comparison, and recommendation logic
retrieval/
* Semantic retrieval layer
data/
* Normalized SHL catalog
indexes/
* FAISS vector index
---

## Future Improvements
* Migration to the newer Google GenAI SDK
* Caching of repeated requests
* Hybrid retrieval (dense + keyword)
* Frontend UI
* Additional evaluation benchmarks
