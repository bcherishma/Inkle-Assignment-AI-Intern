import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration settings"""
    
    # API URLs
    nominatim_base_url: str = os.getenv(
        "NOMINATIM_BASE_URL", 
        "https://nominatim.openstreetmap.org/search"
    )
    open_meteo_base_url: str = os.getenv(
        "OPEN_METEO_BASE_URL", 
        "https://api.open-meteo.com/v1/forecast"
    )
    overpass_base_url: str = os.getenv(
        "OVERPASS_BASE_URL", 
        "https://overpass-api.de/api/interpreter"
    )
    
    # API Configuration
    user_agent: str = os.getenv("USER_AGENT", "TourismAI/1.0")
    
    # Server Configuration
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    # Render/Railway use PORT env var, fallback to API_PORT or 8000
    api_port: int = int(os.getenv("PORT", os.getenv("API_PORT", "8000")))
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Database Configuration
    database_url: str = os.getenv(
        "DATABASE_URL",
        "sqlite+aiosqlite:///./tourism_ai.db"
    )
    database_echo: bool = os.getenv("DATABASE_ECHO", "False").lower() == "true"
    
    # Application Info
    app_name: str = "Tourism AI Multi-Agent System"
    app_version: str = "1.0.0"
    app_description: str = "A multi-agent system for tourism information using weather and places APIs"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

