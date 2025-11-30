"""Service for managing decision trees."""
import json
import streamlit as st
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from models.decision_tree import DecisionResult, Question, DecisionNode
from utils.config import Config
from utils.validators import validate_radio_selection, safe_int_extract, sanitize_input
from utils.cache import cache


class DecisionTreeService:
    """Service for executing decision tree logic."""
    
    def __init__(self):
        """Initialize the service."""
        self.trees: Dict[str, Dict] = {}
        self._load_trees()
    
    def _load_trees(self) -> None:
        """Load decision trees from JSON files."""
        logic_dir = Config.LOGIC_DIR
        for json_file in logic_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    tree_data = json.load(f)
                    tree_name = tree_data.get('tree_name', json_file.stem)
                    self.trees[tree_name] = tree_data
            except (json.JSONDecodeError, IOError) as e:
                st.error(f"Error loading tree from {json_file}: {e}")
    
    def get_available_trees(self) -> List[str]:
        """
        Get list of available decision trees.
        
        Returns:
            List of tree names
        """
        return list(self.trees.keys())
    
    def execute_tree(
        self, 
        tree_name: str, 
        answers: Dict[str, Any]
    ) -> DecisionResult:
        """
        Execute a decision tree with given answers.
        
        Args:
            tree_name: Name of the tree to execute
            answers: Dictionary of question IDs to answers
            
        Returns:
            DecisionResult object
        """
        if tree_name not in self.trees:
            return DecisionResult(
                decision=None,
                explanation=f"Tree '{tree_name}' not found.",
                path=[]
            )
        
        # For now, use hardcoded logic for existing trees
        # This will be replaced with generic JSON engine
        if tree_name == "Incident Reporting":
            return self._execute_incident_reporting(answers)
        elif tree_name == "Vendor Risk Tiering":
            return self._execute_vendor_classification(answers)
        elif tree_name == "DPIA Requirement":
            return self._execute_dpia(answers)
        
        return DecisionResult(decision=None, explanation="Tree not implemented.", path=[])
    
    def _execute_incident_reporting(self, answers: Dict[str, Any]) -> DecisionResult:
        """Execute incident reporting tree logic."""
        path = []
        q1 = answers.get("ir_q1", "Select...")
        path.append(f"Q1 → {q1}")
        
        if q1 == "Select...":
            return DecisionResult(None, None, path)
        
        if q1 == "No":
            return DecisionResult(
                "ACCEPT",
                "The vendor does not process personal or sensitive data on your behalf. "
                "Strict incident notification requirements are not triggered. You can still "
                "include a generic incident notification clause as good practice.",
                path,
                DecisionType.ACCEPT
            )
        
        q2 = answers.get("ir_q2", "Select...")
        path.append(f"Q2 → {q2}")
        
        if q2 == "Select...":
            return DecisionResult(None, None, path)
        
        if q2 == "No":
            return DecisionResult(
                "ACCEPT_WITH_MITIGATION",
                "There is no explicit regulatory or upstream contractual incident notification "
                "timeframe, but the vendor processes personal or sensitive data. You should "
                "define a reasonable notification time window in the contract for governance "
                "and monitoring purposes.",
                path,
                DecisionType.ACCEPT_WITH_MITIGATION
            )
        
        q3 = answers.get("ir_q3", "Select...")
        path.append(f"Q3 → {q3}")
        
        if q3 == "Select...":
            return DecisionResult(None, None, path)
        
        # Safe extraction with error handling
        required_hours = safe_int_extract(q3, 24)
        
        q4 = answers.get("ir_q4", "Select...")
        path.append(f"Q4 → {q4}")
        
        if q4 == "Select...":
            return DecisionResult(None, None, path)
        
        if q4 == "Yes":
            return DecisionResult(
                "ACCEPT",
                f"The vendor agrees to a {required_hours}-hour notification window, which "
                "aligns with your internal standard and regulatory expectations. This supports "
                "timely internal escalation and external reporting where required.",
                path,
                DecisionType.ACCEPT
            )
        
        q5 = answers.get("ir_q5", "Select...")
        path.append(f"Q5 → {q5}")
        
        if q5 == "Select...":
            return DecisionResult(None, None, path)
        
        if q5 == "Yes":
            return DecisionResult(
                "ACCEPT_WITH_MITIGATION",
                "The vendor cannot meet your preferred incident notification timeframe, but "
                "you can introduce compensating controls such as enhanced monitoring and "
                "prioritised escalation. The risk is reduced but should be documented and "
                "periodically reviewed.",
                path,
                DecisionType.ACCEPT_WITH_MITIGATION
            )
        
        return DecisionResult(
            "REJECT",
            "The vendor cannot meet your required notification timeframe and you cannot put "
            "effective compensating controls in place. The residual risk remains too high, "
            "so you should consider alternative vendors or a different solution.",
            path,
            DecisionType.REJECT
        )
    
    def _execute_vendor_classification(self, answers: Dict[str, Any]) -> DecisionResult:
        """Execute vendor classification tree logic."""
        path = []
        q1 = answers.get("vc_q1", "Select...")
        path.append(f"Q1 → {q1}")
        
        if q1 == "Select...":
            return DecisionResult(None, None, path)
        
        q2 = answers.get("vc_q2", "Select...")
        path.append(f"Q2 → {q2}")
        
        if q2 == "Select...":
            return DecisionResult(None, None, path)
        
        q3 = answers.get("vc_q3", "Select...")
        path.append(f"Q3 → {q3}")
        
        if q3 == "Select...":
            return DecisionResult(None, None, path)
        
        # Scoring logic
        score = 0
        
        if q1 == "No data":
            score += 0
        elif q1 == "Personal data":
            score += 2
        elif q1 == "Special category / highly sensitive data":
            score += 4
        
        if q2 == "Small (few records, low volume)":
            score += 1
        elif q2 == "Medium":
            score += 2
        elif q2 == "Large (high volume / continuous)":
            score += 3
        
        if q3 == "Yes":
            score += 2
        
        # Map score to risk level
        if score <= 2:
            level = "LOW"
            explanation = (
                "The vendor has limited exposure to personal or sensitive data and does not "
                "present significant integration risk. Standard due diligence and basic "
                "controls should be sufficient."
            )
        elif 3 <= score <= 5:
            level = "MEDIUM"
            explanation = (
                "The vendor processes personal data or has moderate integration with your "
                "environment. A more detailed security and privacy review is appropriate, and "
                "contractual controls should be clearly defined."
            )
        elif 6 <= score <= 7:
            level = "HIGH"
            explanation = (
                "The vendor processes a meaningful volume of personal or sensitive data and/or "
                "connects to core systems. Enhanced due diligence, stronger controls, and "
                "ongoing monitoring are recommended."
            )
        else:
            level = "CRITICAL"
            explanation = (
                "The vendor processes highly sensitive or special category data at scale and/or "
                "is tightly integrated with critical systems. Treat this as a critical vendor: "
                "require comprehensive assessment, senior sign-off, and continuous monitoring."
            )
        
        return DecisionResult(
            f"RISK TIER: {level}",
            explanation,
            path,
            DecisionType.RISK_TIER,
            {"score": score, "level": level}
        )
    
    def _execute_dpia(self, answers: Dict[str, Any]) -> DecisionResult:
        """Execute DPIA requirement tree logic."""
        path = []
        q1 = answers.get("dp_q1", "Select...")
        path.append(f"Q1 → {q1}")
        
        if q1 == "Select...":
            return DecisionResult(None, None, path)
        
        q2 = answers.get("dp_q2", "Select...")
        path.append(f"Q2 → {q2}")
        
        if q2 == "Select...":
            return DecisionResult(None, None, path)
        
        q3 = answers.get("dp_q3", "Select...")
        path.append(f"Q3 → {q3}")
        
        if q3 == "Select...":
            return DecisionResult(None, None, path)
        
        yes_count = sum(1 for ans in [q1, q2, q3] if ans == "Yes")
        
        if yes_count == 0:
            return DecisionResult(
                "DPIA NOT REQUIRED (LIKELY)",
                "None of the high-risk indicators are triggered. A full DPIA is unlikely to be "
                "mandatory, but you should document this assessment and keep it under review "
                "if the scope changes.",
                path,
                DecisionType.DPIA_NOT_REQUIRED
            )
        elif yes_count == 1:
            return DecisionResult(
                "DPIA RECOMMENDED",
                "At least one high-risk characteristic is present. A DPIA may not be strictly "
                "mandatory in all jurisdictions, but completing one is recommended to document "
                "risk analysis and controls.",
                path,
                DecisionType.DPIA_RECOMMENDED
            )
        else:
            return DecisionResult(
                "DPIA REQUIRED",
                "Multiple high-risk characteristics are present. A DPIA should be treated as "
                "mandatory to assess and document privacy risks and mitigating controls before "
                "proceeding.",
                path,
                DecisionType.DPIA_REQUIRED
            )

