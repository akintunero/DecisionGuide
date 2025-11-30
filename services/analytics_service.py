"""Analytics service for tracking usage statistics."""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from collections import defaultdict
from utils.config import Config


class AnalyticsService:
    """Service for tracking and analyzing usage statistics."""
    
    def __init__(self):
        """Initialize analytics service."""
        self.analytics_file = Config.DATA_DIR / "analytics.json"
        self._ensure_analytics_file()
    
    def _ensure_analytics_file(self) -> None:
        """Ensure analytics file exists."""
        if not self.analytics_file.exists():
            self._save_analytics({
                "total_decisions": 0,
                "tree_usage": {},
                "decision_counts": defaultdict(int),
                "first_use": datetime.now().isoformat(),
                "last_use": datetime.now().isoformat()
            })
    
    def _load_analytics(self) -> Dict[str, Any]:
        """Load analytics from file."""
        try:
            if self.analytics_file.exists():
                with open(self.analytics_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Convert decision_counts back to defaultdict
                    if "decision_counts" in data:
                        data["decision_counts"] = defaultdict(int, data["decision_counts"])
                    return data
        except (json.JSONDecodeError, IOError):
            pass
        return {
            "total_decisions": 0,
            "tree_usage": {},
            "decision_counts": defaultdict(int),
            "first_use": datetime.now().isoformat(),
            "last_use": datetime.now().isoformat()
        }
    
    def _save_analytics(self, analytics: Dict[str, Any]) -> None:
        """Save analytics to file."""
        try:
            # Convert defaultdict to regular dict for JSON serialization
            data = dict(analytics)
            if "decision_counts" in data and isinstance(data["decision_counts"], defaultdict):
                data["decision_counts"] = dict(data["decision_counts"])
            
            with open(self.analytics_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving analytics: {e}")
    
    def track_decision(
        self,
        tree_name: str,
        decision: str
    ) -> None:
        """
        Track a decision for analytics.
        
        Args:
            tree_name: Name of the decision tree used
            decision: Decision outcome
        """
        if not Config.ENABLE_ANALYTICS:
            return
        
        analytics = self._load_analytics()
        
        analytics["total_decisions"] += 1
        analytics["last_use"] = datetime.now().isoformat()
        
        # Track tree usage
        if tree_name not in analytics["tree_usage"]:
            analytics["tree_usage"][tree_name] = 0
        analytics["tree_usage"][tree_name] += 1
        
        # Track decision outcomes
        analytics["decision_counts"][decision] += 1
        
        self._save_analytics(analytics)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get usage statistics.
        
        Returns:
            Dictionary of statistics
        """
        if not Config.ENABLE_ANALYTICS:
            return {}
        
        analytics = self._load_analytics()
        
        # Convert defaultdict to dict for display
        decision_counts = dict(analytics["decision_counts"]) if isinstance(
            analytics["decision_counts"], defaultdict
        ) else analytics["decision_counts"]
        
        return {
            "total_decisions": analytics.get("total_decisions", 0),
            "tree_usage": analytics.get("tree_usage", {}),
            "decision_counts": decision_counts,
            "first_use": analytics.get("first_use"),
            "last_use": analytics.get("last_use")
        }

