"""Caching utilities for performance optimization."""
from functools import lru_cache
from typing import Any, Callable, Dict, Optional, Tuple
import time
from utils.config import Config


class SimpleCache:
    """Simple in-memory cache with TTL."""
    
    def __init__(self, ttl: int = None):
        """
        Initialize cache.
        
        Args:
            ttl: Time to live in seconds (defaults to Config.CACHE_TTL)
        """
        self.ttl = ttl or Config.CACHE_TTL
        self._cache: Dict[str, Tuple[Any, float]] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache if not expired.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if expired/not found
        """
        if key not in self._cache:
            return None
        
        value, timestamp = self._cache[key]
        if time.time() - timestamp > self.ttl:
            del self._cache[key]
            return None
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        self._cache[key] = (value, time.time())
    
    def clear(self) -> None:
        """Clear all cached values."""
        self._cache.clear()


# Global cache instance
cache = SimpleCache()

