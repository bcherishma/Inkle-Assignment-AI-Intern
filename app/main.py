# FastAPI application for Tourism AI Multi-Agent System
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

from app.models.schemas import TourismRequest, TourismResponse
from app.clients.geocoding_client import GeocodingClient
from app.clients.weather_client import WeatherClient
from app.clients.places_client import PlacesClient
from app.agents.weather_agent import WeatherAgent
from app.agents.places_agent import PlacesAgent
from app.agents.parent_agent import TourismAIAgent
from app.utils.logger import setup_logger

# Load environment variables
load_dotenv()

logger = setup_logger(__name__)


class Settings(BaseSettings):
    nominatim_base_url: str = os.getenv("NOMINATIM_BASE_URL", "https://nominatim.openstreetmap.org/search")
    open_meteo_base_url: str = os.getenv("OPEN_METEO_BASE_URL", "https://api.open-meteo.com/v1/forecast")
    overpass_base_url: str = os.getenv("OVERPASS_BASE_URL", "https://overpass-api.de/api/interpreter")
    user_agent: str = os.getenv("USER_AGENT", "TourismAI/1.0")
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    class Config:
        env_file = ".env"


# Global clients and agents
geocoding_client: GeocodingClient = None
weather_client: WeatherClient = None
places_client: PlacesClient = None
weather_agent: WeatherAgent = None
places_agent: PlacesAgent = None
tourism_agent: TourismAIAgent = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup and shutdown
    global geocoding_client, weather_client, places_client
    global weather_agent, places_agent, tourism_agent
    
    settings = Settings()
    
    logger.info("Starting Tourism AI Multi-Agent System...")
    
    # Initialize clients
    geocoding_client = GeocodingClient(
        base_url=settings.nominatim_base_url,
        user_agent=settings.user_agent
    )
    weather_client = WeatherClient(base_url=settings.open_meteo_base_url)
    places_client = PlacesClient(base_url=settings.overpass_base_url)
    
    # Initialize agents
    weather_agent = WeatherAgent(geocoding_client, weather_client)
    places_agent = PlacesAgent(geocoding_client, places_client)
    tourism_agent = TourismAIAgent(weather_agent, places_agent)
    
    logger.info("Tourism AI Multi-Agent System started successfully!")
    
    yield
    
    # Cleanup
    logger.info("Shutting down Tourism AI Multi-Agent System...")
    await geocoding_client.close()
    await weather_client.close()
    await places_client.close()
    logger.info("Shutdown complete.")


# Create FastAPI app
app = FastAPI(
    title="Tourism AI Multi-Agent System",
    description="A multi-agent system for tourism information using weather and places APIs",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files for UI
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
logger.info(f"Static directory: {static_dir}, exists: {os.path.exists(static_dir)}")

if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    logger.info("Static files mounted at /static")

@app.get("/ui")
async def serve_ui():
    ui_path = os.path.join(static_dir, "index.html")
    logger.info(f"Serving UI from: {ui_path}, exists: {os.path.exists(ui_path)}")
    if os.path.exists(ui_path):
        return FileResponse(ui_path, media_type="text/html")
    return {"message": "UI not found", "path": ui_path}

@app.get("/")
async def root():
    ui_path = os.path.join(static_dir, "index.html")
    if os.path.exists(ui_path):
        return FileResponse(ui_path, media_type="text/html")
    return {
        "message": "Tourism AI Multi-Agent System API",
        "version": "1.0.0",
        "ui": "/ui",
        "api_docs": "/docs",
        "static_dir": static_dir,
        "index_exists": os.path.exists(ui_path)
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "tourism-ai-system"}


@app.post("/query", response_model=TourismResponse)
async def query_tourism(request: TourismRequest):
    # Main endpoint for tourism queries
    try:
        logger.info(f"Received query: {request.query}")
        
        if not tourism_agent:
            logger.error("Tourism agent not initialized")
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        response = await tourism_agent.process_query(
            query=request.query,
            place_name=request.place
        )
        
        logger.info(f"Query processed successfully for: {response.place_name}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    settings = Settings()
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )

