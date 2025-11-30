"""Configuration management for DecisionGuide."""
import os
from typing import Optional
from pathlib import Path


class Config:
    """Application configuration with environment variable support."""
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    LOGIC_DIR: Path = BASE_DIR / "logic"
    DATA_DIR: Path = BASE_DIR / "data"
    
    # App settings
    APP_TITLE: str = os.getenv("APP_TITLE", "DecisionGuide")
    APP_DESCRIPTION: str = os.getenv(
        "APP_DESCRIPTION",
        "A simple, logic-based assistant for governance and audit decisions."
    )
    
    # Feature flags
    ENABLE_PDF_EXPORT: bool = os.getenv("ENABLE_PDF_EXPORT", "true").lower() == "true"
    ENABLE_HISTORY: bool = os.getenv("ENABLE_HISTORY", "true").lower() == "true"
    ENABLE_ANALYTICS: bool = os.getenv("ENABLE_ANALYTICS", "false").lower() == "true"
    
    # Performance
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))  # 1 hour default
    
    # Security
    MAX_SESSION_DURATION: int = int(os.getenv("MAX_SESSION_DURATION", "7200"))  # 2 hours
    
    @classmethod
    def ensure_directories(cls) -> None:
        """Ensure required directories exist."""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.LOGIC_DIR.mkdir(exist_ok=True)


# Initialize directories
Config.ensure_directories()

