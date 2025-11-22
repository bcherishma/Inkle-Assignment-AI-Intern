"""Run script for the Tourism AI Multi-Agent System"""

import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    # Railway uses PORT env var, fallback to API_PORT or 8000
    port = int(os.getenv("PORT", os.getenv("API_PORT", "8000")))
    log_level = os.getenv("LOG_LEVEL", "INFO").lower()
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=False,  # Disable reload in production (Railway)
        log_level=log_level
    )

