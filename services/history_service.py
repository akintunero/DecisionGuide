"""Service for managing decision history."""
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any
from models.decision_tree import DecisionResult
from utils.config import Config


class HistoryService:
    """Service for storing and retrieving decision history."""
    
    def __init__(self):
        """Initialize history service."""
        self.history_file = Config.DATA_DIR / "decision_history.json"
        self._ensure_history_file()
    
    def _ensure_history_file(self) -> None:
        """Ensure history file exists."""
        if not self.history_file.exists():
            self._save_history([])
    
    def _load_history(self) -> List[Dict[str, Any]]:
        """Load history from file."""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
        return []
    
    def _save_history(self, history: List[Dict[str, Any]]) -> None:
        """Save history to file."""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving history: {e}")
    
    def save_decision(
        self,
        tree_name: str,
        result: DecisionResult,
        answers: Dict[str, Any]
    ) -> None:
        """
        Save a decision to history.
        
        Args:
            tree_name: Name of the decision tree
            result: DecisionResult object
            answers: Dictionary of answers provided
        """
        if not Config.ENABLE_HISTORY:
            return
        
        history = self._load_history()
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "tree_name": tree_name,
            "decision": result.decision,
            "explanation": result.explanation,
            "path": result.path,
            "answers": answers,
            "metadata": result.metadata or {}
        }
        
        history.append(entry)
        
        # Keep only last 100 entries
        if len(history) > 100:
            history = history[-100:]
        
        self._save_history(history)
    
    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent decision history.
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of history entries, most recent first
        """
        if not Config.ENABLE_HISTORY:
            return []
        
        history = self._load_history()
        return list(reversed(history[-limit:]))
    
    def clear_history(self) -> None:
        """Clear all history."""
        self._save_history([])

