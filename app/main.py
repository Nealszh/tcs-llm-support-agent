from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os

from agent.graph import build_graph
from agent.schema import UserInput, TriageResult

load_dotenv()

app = FastAPI(title="TCS Support Triage & Resolution Agent", version="1.0.0")
graph = build_graph()


@app.get("/health")
def health():
    return {"status": "ok", "env": os.getenv("APP_ENV", "unknown")}


@app.post("/triage", response_model=TriageResult)
def triage(payload: UserInput):
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="message is empty")
    out = graph.invoke({"user_message": payload.message})
    return out["result_json"]
