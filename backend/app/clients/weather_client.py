import httpx
from typing import Optional
from app.models.schemas import WeatherResponse
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class WeatherClient:
    def __init__(self, base_url: str = "https://api.open-meteo.com/v1/forecast"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=10.0)
    
    async def get_weather(self, latitude: float, longitude: float, place_name: str) -> Optional[WeatherResponse]:
        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,precipitation_probability",
                "forecast_days": 1
            }
            response = await self.client.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            current = data.get("current", {})
            
            temperature = current.get("temperature_2m", 0.0)
            rain_probability = current.get("precipitation_probability", 0.0)
            
            return WeatherResponse(
                temperature=temperature,
                rain_probability=rain_probability,
                place_name=place_name
            )
        except Exception as e:
            logger.error(f"Weather API error: {e}")
            return None
    
    async def close(self):
        await self.client.aclose()

