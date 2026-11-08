from pydantic import BaseModel, Field
from typing import Literal

class EvidenceResponse(BaseModel):
    observable_action: str
    incident_status: Literal["supported","contradicted","insufficient_evidence"]
    abstain: bool
    asserted_claims: list[str] = Field(default_factory=list)
    evidence_timestamps: list[float] = Field(default_factory=list)
    explanation: str
