"""Tests for validation utilities."""
import pytest
from utils.validators import (
    validate_radio_selection,
    validate_not_empty,
    safe_int_extract,
    sanitize_input
)


class TestValidators:
    """Test validation functions."""
    
    def test_validate_radio_selection_valid(self):
        """Test valid radio selection."""
        assert validate_radio_selection("Yes", ["Yes", "No", "Select..."]) is True
        assert validate_radio_selection("No", ["Yes", "No", "Select..."]) is True
    
    def test_validate_radio_selection_invalid(self):
        """Test invalid radio selection."""
        assert validate_radio_selection("Maybe", ["Yes", "No"]) is False
        assert validate_radio_selection(None, ["Yes", "No"]) is False
    
    def test_validate_not_empty(self):
        """Test not empty validation."""
        assert validate_not_empty("test") is True
        assert validate_not_empty("") is False
        assert validate_not_empty("Select...") is False
        assert validate_not_empty(None) is False
    
    def test_safe_int_extract(self):
        """Test safe integer extraction."""
        assert safe_int_extract("24 hours") == 24
        assert safe_int_extract("48 hours") == 48
        assert safe_int_extract("72") == 72
        assert safe_int_extract("invalid") == 0
        assert safe_int_extract("") == 0
        assert safe_int_extract(None) == 0
        assert safe_int_extract("24 hours", default=10) == 24
    
    def test_sanitize_input(self):
        """Test input sanitization."""
        assert sanitize_input("test") == "test"
        assert sanitize_input("test<script>") == "testscript"
        assert sanitize_input("  test  ") == "test"
        assert sanitize_input(None) == ""

