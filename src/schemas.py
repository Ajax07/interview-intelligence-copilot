from pydantic import BaseModel, Field
from typing import List

class Conflict(BaseModel):
    topic: str = Field(description="Skill or behavior where interviewers disagreed")
    interviewer_a_view: str = Field(description="First interviewer's stance with citation")
    interviewer_b_view: str = Field(description="Second interviewer's stance with citation")
    severity: str = Field(description="High, Medium, or Low impact")

class DebriefSynthesis(BaseModel):
    red_flags: List[str] = Field(description="Critical risks or behavioral concerns detected")
    conflicts: List[Conflict] = Field(description="Contradictions between debriefs")
    key_evidence: dict[str, str] = Field(description="Extracted skill evidence mapped to quotes")
    next_step: str = Field(description="MUST always be exactly: 'Human Hiring Manager Review'")