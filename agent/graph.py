from typing import TypedDict, Any, Dict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import os
import json

from agent.prompts import SYSTEM, ROUTER, TRIAGE_AND_DRAFT
from agent.tools import extract_signals
from agent.schema import TriageResult


class AgentState(TypedDict, total=False):
    user_message: str
    signals: Dict[str, Any]
    route: Dict[str, Any]
    result_json: Dict[str, Any]


def _get_llm() -> ChatOpenAI:
    # Provider abstraction (可扩展到 Azure/Vertex；此处提交最小可用 OpenAI 版本)
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    return ChatOpenAI(model=model, temperature=0.2)


def node_signals(state: AgentState) -> AgentState:
    state["signals"] = extract_signals(state["user_message"])
    return state


def node_route(state: AgentState) -> AgentState:
    llm = _get_llm()
    msg = [
        SystemMessage(content=SYSTEM),
        HumanMessage(
            content=ROUTER
            + "\n\nUser message:\n"
            + state["user_message"]
            + "\n\nSignals:\n"
            + json.dumps(state["signals"])
        ),
    ]
    raw = llm.invoke(msg).content
    try:
        state["route"] = json.loads(raw)
    except Exception:
        state["route"] = {"next_action": "ask", "reason": "Router output not valid JSON; fallback to ask."}
    return state


def node_draft(state: AgentState) -> AgentState:
    llm = _get_llm()
    msg = [
        SystemMessage(content=SYSTEM),
        HumanMessage(
            content=TRIAGE_AND_DRAFT
            + "\n\nUser message:\n"
            + state["user_message"]
            + "\n\nSignals:\n"
            + json.dumps(state["signals"])
        ),
    ]
    raw = llm.invoke(msg).content
    try:
        data = json.loads(raw)
        validated = TriageResult(**data).model_dump()
        state["result_json"] = validated
    except Exception as e:
        state["result_json"] = {
            "category": "Unknown",
            "priority": "P2",
            "title": "Unable to parse LLM output",
            "summary": "The agent could not produce valid structured JSON.",
            "clarifying_questions": ["Can you share the exact error message and steps to reproduce?"],
            "suggested_steps": [],
            "escalation_reason": None,
            "assumptions": [f"Parsing/validation error: {str(e)}"],
        }
    return state


def node_ask(state: AgentState) -> AgentState:
    # "ask" is represented by returning clarifying questions in the structured result.
    return node_draft(state)


def node_escalate(state: AgentState) -> AgentState:
    return node_draft(state)


def build_graph():
    g = StateGraph(AgentState)
    g.add_node("detect_signals", node_signals)
    g.add_node("route", node_route)
    g.add_node("draft", node_draft)
    g.add_node("ask", node_ask)
    g.add_node("escalate", node_escalate)

    g.set_entry_point("detect_signals")
    g.add_edge("detect_signals", "route")

    def _chooser(state: AgentState) -> str:
        action = (state.get("route") or {}).get("next_action", "ask")
        if action not in {"ask", "resolve", "escalate"}:
            return "ask"
        return "draft" if action == "resolve" else action

    g.add_conditional_edges(
        "route",
        _chooser,
        {"draft": "draft", "ask": "ask", "escalate": "escalate"},
    )

    g.add_edge("draft", END)
    g.add_edge("ask", END)
    g.add_edge("escalate", END)
    return g.compile()

