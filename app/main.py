# FastAPI application for Tourism AI Multi-Agent System
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
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


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup and shutdown
    global geocoding_client, weather_client, places_client
    global weather_agent, places_agent, tourism_agent
    
    logger.info(f"Starting {settings.app_name} v{settings.app_version}...")
    
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
            "/docs": "GET - API documentation (Swagger UI)",
            "/redoc": "GET - API documentation (ReDoc)"
        }
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
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
        log_level=settings.log_level.lower()
    )

