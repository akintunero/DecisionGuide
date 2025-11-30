"""Decision tree data models."""
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum


class DecisionType(str, Enum):
    """Types of decisions."""
    ACCEPT = "ACCEPT"
    ACCEPT_WITH_MITIGATION = "ACCEPT_WITH_MITIGATION"
    REJECT = "REJECT"
    RISK_TIER = "RISK_TIER"
    DPIA_REQUIRED = "DPIA_REQUIRED"
    DPIA_RECOMMENDED = "DPIA_RECOMMENDED"
    DPIA_NOT_REQUIRED = "DPIA_NOT_REQUIRED"


@dataclass
class DecisionResult:
    """Result of a decision tree evaluation."""
    decision: Optional[str]
    explanation: Optional[str]
    path: List[str]
    decision_type: Optional[DecisionType] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize metadata if not provided."""
        if self.metadata is None:
            self.metadata = {}


@dataclass
class Question:
    """Represents a question in a decision tree."""
    id: str
    text: str
    options: List[str]
    question_type: str = "radio"  # radio, selectbox, etc.
    required: bool = True
    help_text: Optional[str] = None


@dataclass
class DecisionNode:
    """Represents a node in a decision tree."""
    id: str
    condition: Optional[str] = None
    decision: Optional[str] = None
    explanation: Optional[str] = None
    next_nodes: Dict[str, str] = None  # Maps answer -> next node ID
    
    def __post_init__(self):
        """Initialize next_nodes if not provided."""
        if self.next_nodes is None:
            self.next_nodes = {}

