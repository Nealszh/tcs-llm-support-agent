from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os

from agent.graph import build_graph
from agent.schema import UserInput, TriageResult

load_dotenv()

app = FastAPI(title="TCS Support Triage & Resolution Agent", version="1.0.0")

_graph = None

def get_graph():
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph


@app.get("/health")
def health():
    return {"status": "ok", "env": os.getenv("APP_ENV", "unknown")}


@app.post("/triage", response_model=TriageResult)
def triage(payload: UserInput):
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="message is empty")

    try:
        graph = get_graph()
        out = graph.invoke({"user_message": payload.message})
        return out["result_json"]
    except Exception:
        # In CI/test we may not have external credentials; return a controlled 500.
        raise HTTPException(status_code=500, detail="Triage failed")
