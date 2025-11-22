"""
Caching utility for API responses to improve performance and reduce API calls.
Implements time-based caching with configurable TTL (Time To Live).
"""
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from functools import wraps
import hashlib
import json
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class ResponseCache:
    """Simple in-memory cache with TTL (Time To Live) support"""
    
    def __init__(self, default_ttl_seconds: int = 3600):
        """
        Initialize cache with default TTL
        
        Args:
            default_ttl_seconds: Default cache expiration time in seconds (default: 1 hour)
        """
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl_seconds
    
    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate cache key from arguments"""
        key_data = json.dumps({
            'args': args,
            'kwargs': sorted(kwargs.items())
        }, sort_keys=True)
        key_hash = hashlib.md5(key_data.encode()).hexdigest()
        return f"{prefix}:{key_hash}"
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache if not expired
        
        Args:
            key: Cache key
            
        Returns:
            Cached value if exists and not expired, None otherwise
        """
        if key not in self.cache:
            return None
        
        entry = self.cache[key]
        expires_at = entry.get('expires_at')
        
        if expires_at and datetime.now() > expires_at:
            del self.cache[key]
            logger.debug(f"Cache expired for key: {key}")
            return None
        
        logger.debug(f"Cache hit for key: {key}")
        return entry.get('value')
    
    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        """
        Store value in cache with TTL
        
        Args:
            key: Cache key
            value: Value to cache
            ttl_seconds: Time to live in seconds (uses default if None)
        """
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl
        expires_at = datetime.now() + timedelta(seconds=ttl)
        
        self.cache[key] = {
            'value': value,
            'expires_at': expires_at,
            'created_at': datetime.now()
        }
        
        logger.debug(f"Cached value for key: {key} (TTL: {ttl}s)")
    
    def clear(self) -> None:
        """Clear all cache entries"""
        self.cache.clear()
        logger.info("Cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        now = datetime.now()
        active_entries = sum(
            1 for entry in self.cache.values()
            if not entry.get('expires_at') or entry['expires_at'] > now
        )
        
        return {
            'total_entries': len(self.cache),
            'active_entries': active_entries,
            'expired_entries': len(self.cache) - active_entries
        }


weather_cache = ResponseCache(default_ttl_seconds=3600)  
places_cache = ResponseCache(default_ttl_seconds=3600)  


def cached(prefix: str, ttl_seconds: int = 3600):
    """
    Decorator for caching function results
    
    Args:
        prefix: Cache key prefix
        ttl_seconds: Time to live in seconds
        
    Example:
        @cached("weather", ttl_seconds=3600)
        async def get_weather(lat, lon):
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache = weather_cache if "weather" in prefix.lower() else places_cache
            
            cache_key = cache._generate_key(prefix, *args, **kwargs)
            
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            result = await func(*args, **kwargs)
            cache.set(cache_key, result, ttl_seconds)
            
            return result
        
        return wrapper
    return decorator

