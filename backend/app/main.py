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
from app.database.connection import _get_db_path
from app.repositories.history_repository import HistoryRepository

load_dotenv()

settings = Settings()
logger = setup_logger(__name__, level=settings.log_level)

# Global dependency objects
geocoding_client: GeocodingClient = None
weather_client: WeatherClient = None
places_client: PlacesClient = None
weather_agent: WeatherAgent = None
places_agent: PlacesAgent = None
tourism_agent: TourismAIAgent = None
history_repository: HistoryRepository = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global geocoding_client, weather_client, places_client
    global weather_agent, places_agent, tourism_agent, history_repository

    logger.info(f"Starting {settings.app_name} v{settings.app_version}...")

    # Initialize SQLite database
    await init_db(settings)

    # Resolve DB path
    db_path = _get_db_path(settings)
    logger.info(f"Database path: {db_path}")
    history_repository = HistoryRepository(db_path)

    # Initialize API clients
    geocoding_client = GeocodingClient(
        base_url=settings.nominatim_base_url,
        user_agent=settings.user_agent
    )
    weather_client = WeatherClient(base_url=settings.open_meteo_base_url)
    places_client = PlacesClient(base_url=settings.overpass_base_url)

    # Agents
    weather_agent = WeatherAgent(geocoding_client, weather_client)
    places_agent = PlacesAgent(geocoding_client, places_client)
    tourism_agent = TourismAIAgent(weather_agent, places_agent)

    logger.info("Tourism AI Multi-Agent System started successfully!")

    yield

    # Shutdown gracefully
    logger.info("Shutting down Tourism AI Multi-Agent System...")
    await geocoding_client.close()
    await weather_client.close()
    await places_client.close()
    await close_db()
    logger.info("Shutdown complete.")

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # Local development
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",

        # Render Frontend (YOUR ACTUAL URL)
        "https://wanderwise-frontend-9zer.onrender.com",
    ],
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
            "/history": "GET - Recent query history",
            "/history/stats": "GET - Query statistics",
            "/history/place/{place_name}": "GET - History for a specific place",
            "/docs": "Swagger UI",
            "/redoc": "ReDoc UI"
        }
    }


@app.get("/health")
async def health_check():
    try:
        if tourism_agent is None:
            return {"status": "starting", "service": "tourism-ai-system"}
        return {"status": "healthy", "service": "tourism-ai-system", "version": settings.app_version}
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {"status": "unhealthy", "error": str(e)}


@app.get("/history")
async def get_query_history(limit: int = 10, days: int = None):
    try:
        if not history_repository:
            raise HTTPException(status_code=503, detail="Repository not initialized")

        history = await history_repository.get_recent(limit=limit, days=days)
        return {"success": True, "count": len(history), "history": history}
    except Exception as e:
        logger.error(f"Error fetching query history: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching history: {str(e)}")


@app.get("/history/stats")
async def get_query_stats():
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


@app.options("/query")
async def options_query():
    """Handle CORS preflight"""
    return {"message": "OK"}


@app.post("/query", response_model=TourismResponse)
async def query_tourism(request: TourismRequest, http_request: Request):
    try:
        logger.info(f"Received query: {request.query}")

        if not tourism_agent:
            raise HTTPException(status_code=503, detail="Service not initialized")

        user_ip = http_request.client.host if http_request.client else None

        response = await tourism_agent.process_query(
            query=request.query,
            place_name=request.place
        )

        # Save history
        if history_repository:
            try:
                history_id = await history_repository.save_interaction(
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
                logger.info(f"Saved query history with ID: {history_id}")
            except Exception as db_error:
                logger.error(f"Failed to save query history: {db_error}", exc_info=True)

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
