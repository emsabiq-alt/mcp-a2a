"""
MCP-A2A Protocol Specification
=============================
Defines the communication contracts between Tool-Augmented Agents.
Instead of raw unstructured text, MCP-A2A enforces schema-validated Evidence Handover.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional
from enum import Enum
import json
import time
import hashlib

class MessageType(str, Enum):
    HANDSHAKE = "handshake"
    TASK_DELEGATION = "task_delegation"
    EVIDENCE_HANDOVER = "evidence_handover"
    VERIFICATION_REQUEST = "verification_request"
    VERIFICATION_RESULT = "verification_result"
    COMPLETION = "completion"
    ERROR = "error"

@dataclass
class ToolExecutionRecord:
    tool_name: str
    arguments: Dict[str, Any]
    output: Any
    timestamp: float = field(default_factory=time.time)
    execution_hash: str = ""

    def __post_init__(self):
        if not self.execution_hash:
            raw = f"{self.tool_name}:{json.dumps(self.arguments, sort_keys=True)}:{str(self.output)}"
            self.execution_hash = hashlib.sha256(raw.encode()).hexdigest()[:16]

@dataclass
class EvidenceEnvelope:
    """
    Contract for data transferred across agent boundaries.
    Ensures Agent B receives verifiable facts grounded in Agent A's MCP executions,
    not raw hallucinations.
    """
    task_id: str
    producer_agent: str
    consumer_agent: str
    evidence_type: str
    claims: Dict[str, Any]
    backing_tool_records: List[ToolExecutionRecord]
    created_at: float = field(default_factory=time.time)

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EvidenceEnvelope":
        records = [ToolExecutionRecord(**r) for r in data.get("backing_tool_records", [])]
        return cls(
            task_id=data["task_id"],
            producer_agent=data["producer_agent"],
            consumer_agent=data["consumer_agent"],
            evidence_type=data["evidence_type"],
            claims=data["claims"],
            backing_tool_records=records,
            created_at=data.get("created_at", time.time())
        )
