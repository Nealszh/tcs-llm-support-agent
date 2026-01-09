# Support Triage & Resolution Agent (LLM-driven)

## Overview
This project implements a production-oriented AI agent that triages support requests and produces a structured support ticket draft with recommended resolution steps.

The **control flow is determined by a Large Language Model (LLM)** using a routing prompt (`ask` / `resolve` / `escalate`). Based on the routing decision, the agent generates a structured JSON response suitable for downstream ticketing or automation systems.

The system is designed with **production readiness** in mind, including schema validation, API contracts, CI automation, and containerization support.

---

## Key Features
- **LLM-driven routing** (ask vs resolve vs escalate)
- **Structured output** validated using Pydantic schemas
- **FastAPI** backend with a `/triage` endpoint
- **Docker** support for containerized deployment
- **GitHub Actions CI** to automatically run tests on each push

---

## Tech Stack
- Python, FastAPI
- LangGraph + LangChain
- OpenAI model via `langchain-openai` (pluggable provider design)
- Pydantic for schema validation
- Pytest for automated testing

---

## Assumptions & Design Decisions
- The agent is designed as a **contract-level system**: CI tests validate API behavior and response structure rather than LLM output quality.
- External LLM calls are **lazy-initialized** and excluded from CI to avoid credential dependency.
- Routing decisions (`ask` / `resolve` / `escalate`) are delegated to the LLM via a structured prompt.
- The system assumes **one user message per triage request** for simplicity.
- The LLM provider is **pluggable** and can be replaced without modifying the core application logic.

---

## API Contract

### POST `/triage`
Request body:
```json
{
  "message": "My VPN is not working"
}
```
---

## How to Run (Local)

This project can be run locally for development or evaluation purposes.

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a .env file based on the provided example:
```
cp .env.example .env
```

### 3. Start the API server
```
uvicorn app.main:app --reload
```

### 4. Open API documentation

Once the server is running, open the following URL in your browser:
http://127.0.0.1:8000/docs

## Running Tests
pytest -q

