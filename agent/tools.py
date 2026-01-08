from typing import Dict, Any
import re

def extract_signals(text: str) -> Dict[str, Any]:
    """Lightweight heuristic signals (启发式信号) to help the agent."""
    lower = text.lower()
    signals = {
        "mentions_error": bool(re.search(r"\berror\b|\bexception\b|\b500\b|\b403\b|\b404\b", lower)),
        "mentions_slow": "slow" in lower or "latency" in lower or "timeout" in lower,
        "mentions_access": "permission" in lower or "access" in lower or "unauthorized" in lower or "forbidden" in lower,
        "mentions_payment": "billing" in lower or "payment" in lower or "invoice" in lower,
        "mentions_security": "password" in lower or "token" in lower or "leak" in lower or "breach" in lower,
    }
    return signals
