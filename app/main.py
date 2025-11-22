# FastAPI application for Tourism AI Multi-Agent System
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.config import Settings
from app.models.schemas import TourismRequest, TourismResponse
from app.clients.geocoding_client import GeocodingClient
from app.clients.weather_client import WeatherClient
from app.clients.places_client import PlacesClient
from app.agents.weather_agent import WeatherAgent
from app.agents.places_agent import PlacesAgent
from app.agents.parent_agent import TourismAIAgent
from app.utils.logger import setup_logger
from app.database import init_db, close_db
from app.repositories.history_repository import HistoryRepository

# Load environment variables
load_dotenv()

# Initialize settings
settings = Settings()

# Setup logger
logger = setup_logger(__name__, level=settings.log_level)


# Global clients and agents
geocoding_client: GeocodingClient = None
weather_client: WeatherClient = None
places_client: PlacesClient = None
weather_agent: WeatherAgent = None
places_agent: PlacesAgent = None
tourism_agent: TourismAIAgent = None
history_repository: HistoryRepository = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup and shutdown
    global geocoding_client, weather_client, places_client
    global weather_agent, places_agent, tourism_agent, history_repository
    
    logger.info(f"Starting {settings.app_name} v{settings.app_version}...")
    
    # Initialize database schema
    await init_db(settings)
    
    # Initialize repository (Repository Pattern)
    # Extract database path from settings
    db_path = settings.database_url
    if db_path.startswith("sqlite+aiosqlite:///"):
        db_path = db_path.replace("sqlite+aiosqlite:///", "")
    elif db_path.startswith("sqlite:///"):
        db_path = db_path.replace("sqlite:///", "")
    history_repository = HistoryRepository(db_path)
    
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
    await close_db()
    logger.info("Shutdown complete.")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
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

@app.get("/")
async def root():
    return {
        "message": "Tourism AI Multi-Agent System API",
        "version": settings.app_version,
        "endpoints": {
            "/query": "POST - Query tourism information",
            "/health": "GET - Health check",
            "/history": "GET - Get recent query history",
            "/history/stats": "GET - Get query statistics",
            "/history/place/{place_name}": "GET - Get history for a specific place",
            "/docs": "GET - API documentation (Swagger UI)",
            "/redoc": "GET - API documentation (ReDoc)"
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "tourism-ai-system"}


@app.get("/history")
async def get_query_history(limit: int = 10, days: int = None):
    """Get recent query history"""
    try:
        if not history_repository:
            raise HTTPException(status_code=503, detail="Repository not initialized")
        
        history = await history_repository.get_recent(limit=limit, days=days)
        return {
            "success": True,
            "count": len(history),
            "history": history
        }
    except Exception as e:
        logger.error(f"Error fetching query history: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching history: {str(e)}")


@app.get("/history/stats")
async def get_query_stats():
    """Get query statistics"""
    try:
        if not history_repository:
            raise HTTPException(status_code=503, detail="Repository not initialized")
        
        stats = await history_repository.get_stats()
        return {"success": True, "stats": stats}
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")


@app.get("/history/place/{place_name}")
async def get_place_history(place_name: str, limit: int = 5):
    """Get query history for a specific place"""
    try:
        if not history_repository:
            raise HTTPException(status_code=503, detail="Repository not initialized")
        
        history = await history_repository.get_by_place(place_name=place_name, limit=limit)
        return {
            "success": True,
            "place_name": place_name,
            "count": len(history),
            "history": history
        }
    except Exception as e:
        logger.error(f"Error fetching place history: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching place history: {str(e)}")


@app.post("/query", response_model=TourismResponse)
async def query_tourism(request: TourismRequest, http_request: Request):
    """Main endpoint for tourism queries"""
    try:
        logger.info(f"Received query: {request.query}")
        
        if not tourism_agent:
            logger.error("Tourism agent not initialized")
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        # Get user IP for tracking
        user_ip = http_request.client.host if http_request.client else None
        
        # Process query
        response = await tourism_agent.process_query(
            query=request.query,
            place_name=request.place
        )
        
        # Store query history using Repository Pattern
        if history_repository:
            try:
                await history_repository.save_interaction(
                    query=request.query,
                    place_name=response.place_name,
                    user_ip=user_ip,
                    has_weather=response.weather is not None,
                    has_places=response.places is not None and len(response.places) > 0,
                    weather_temp=response.weather.temperature if response.weather else None,
                    weather_rain_prob=response.weather.rain_probability if response.weather else None,
                    places_count=len(response.places) if response.places else 0,
                    error=response.error,
                    success=response.success
                )
            except Exception as db_error:
                logger.warning(f"Failed to save query history: {db_error}")
                # Don't fail the request if history saving fails
        
        logger.info(f"Query processed successfully for: {response.place_name}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
        log_level=settings.log_level.lower()
    )

