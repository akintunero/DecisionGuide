"""Input validation utilities."""
from typing import Any, List, Optional


def validate_radio_selection(value: Any, valid_options: List[str]) -> bool:
    """
    Validate that a radio button selection is valid.
    
    Args:
        value: The selected value
        valid_options: List of valid option strings
        
    Returns:
        True if valid, False otherwise
    """
    if value is None:
        return False
    return str(value) in valid_options


def validate_not_empty(value: Any) -> bool:
    """
    Validate that a value is not empty or None.
    
    Args:
        value: Value to validate
        
    Returns:
        True if not empty, False otherwise
    """
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip() != "" and value != "Select..."
    return True


def safe_int_extract(text: str, default: int = 0) -> int:
    """
    Safely extract integer from text (e.g., "24 hours" -> 24).
    
    Args:
        text: Text containing a number
        default: Default value if extraction fails
        
    Returns:
        Extracted integer or default value
    """
    if not text or not isinstance(text, str):
        return default
    
    try:
        # Extract first number from text
        parts = text.split()
        if parts:
            first_part = parts[0]
            return int(first_part)
    except (ValueError, AttributeError):
        pass
    
    return default


def sanitize_input(value: Any) -> str:
    """
    Sanitize user input to prevent injection attacks.
    
    Args:
        value: Input value to sanitize
        
    Returns:
        Sanitized string
    """
    if value is None:
        return ""
    
    text = str(value)
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '{', '}', '\\', '/']
    for char in dangerous_chars:
        text = text.replace(char, '')
    
    return text.strip()

