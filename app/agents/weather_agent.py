# Weather Agent - Child Agent 1
from typing import Optional
from app.models.schemas import WeatherResponse
from app.clients.geocoding_client import GeocodingClient
from app.clients.weather_client import WeatherClient
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class WeatherAgent:
    def __init__(self, geocoding_client: GeocodingClient, weather_client: WeatherClient):
        self.geocoding_client = geocoding_client
        self.weather_client = weather_client
    
    async def get_weather_info(self, place_name: str) -> Optional[WeatherResponse]:
        # Get coordinates first, then weather
        location = await self.geocoding_client.get_coordinates(place_name)
        if not location:
            return None
        
        weather = await self.weather_client.get_weather(location.latitude, location.longitude, place_name)
        return weather

