# Support Triage & Resolution Agent (LLM-driven)

## Overview
This project implements a production-oriented AI agent that triages support requests and produces a structured ticket draft with recommended resolution steps.  
The **control flow is determined by an LLM** using a routing prompt (ask/resolve/escalate), then the agent generates a structured JSON response.

## Key Features
- **LLM-driven routing** (ask vs resolve vs escalate)
- **Structured output** validated with Pydantic
- **FastAPI** backend with `/triage` endpoint
- **Docker** support for deployment
- **GitHub Actions** CI to run tests automatically

## Tech Stack
- Python, FastAPI
- LangGraph + LangChain
- OpenAI model via `langchain-openai` (pluggable provider design)

## How to Run (Local)
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
