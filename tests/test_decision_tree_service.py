"""Tests for decision tree service."""
import pytest
from services.decision_tree_service import DecisionTreeService
from models.decision_tree import DecisionType


class TestDecisionTreeService:
    """Test decision tree service."""
    
    @pytest.fixture
    def service(self):
        """Create service instance."""
        return DecisionTreeService()
    
    def test_get_available_trees(self, service):
        """Test getting available trees."""
        trees = service.get_available_trees()
        assert isinstance(trees, list)
    
    def test_incident_reporting_no_data(self, service):
        """Test incident reporting with no data processing."""
        answers = {"ir_q1": "No"}
        result = service.execute_tree("Incident Reporting", answers)
        assert result.decision == "ACCEPT"
        assert result.decision_type == DecisionType.ACCEPT
        assert result.explanation is not None
    
    def test_incident_reporting_full_flow(self, service):
        """Test full incident reporting flow."""
        answers = {
            "ir_q1": "Yes",
            "ir_q2": "Yes",
            "ir_q3": "24 hours",
            "ir_q4": "Yes"
        }
        result = service.execute_tree("Incident Reporting", answers)
        assert result.decision == "ACCEPT"
        assert "24-hour" in result.explanation or "24" in result.explanation
    
    def test_vendor_classification_low_risk(self, service):
        """Test vendor classification with low risk."""
        answers = {
            "vc_q1": "No data",
            "vc_q2": "Small (few records, low volume)",
            "vc_q3": "No"
        }
        result = service.execute_tree("Vendor Risk Tiering", answers)
        assert "LOW" in result.decision
        assert result.metadata is not None
        assert result.metadata.get("level") == "LOW"
    
    def test_dpia_not_required(self, service):
        """Test DPIA not required scenario."""
        answers = {
            "dp_q1": "No",
            "dp_q2": "No",
            "dp_q3": "No"
        }
        result = service.execute_tree("DPIA Requirement", answers)
        assert "NOT REQUIRED" in result.decision
        assert result.decision_type == DecisionType.DPIA_NOT_REQUIRED
    
    def test_dpia_required(self, service):
        """Test DPIA required scenario."""
        answers = {
            "dp_q1": "Yes",
            "dp_q2": "Yes",
            "dp_q3": "Yes"
        }
        result = service.execute_tree("DPIA Requirement", answers)
        assert "REQUIRED" in result.decision
        assert result.decision_type == DecisionType.DPIA_REQUIRED

