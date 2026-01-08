from pydantic import BaseModel, Field
from typing import List, Literal, Optional


Category = Literal["Bug", "Performance", "Access", "Billing", "FeatureRequest", "Security", "Unknown"]
Priority = Literal["P0", "P1", "P2", "P3"]


class UserInput(BaseModel):
    message: str = Field(..., description="User's support request text")


class TriageResult(BaseModel):
    category: Category
    priority: Priority
    title: str
    summary: str
    clarifying_questions: List[str] = []
    suggested_steps: List[str] = []
    escalation_reason: Optional[str] = None
    assumptions: List[str] = []
