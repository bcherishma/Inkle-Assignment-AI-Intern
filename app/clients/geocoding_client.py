import httpx
from typing import Optional
from app.models.schemas import LocationResponse
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class GeocodingClient:
    def __init__(self, base_url: str = "https://nominatim.openstreetmap.org/search", user_agent: str = "TourismAI/1.0"):
        self.base_url = base_url
        self.user_agent = user_agent
        self.client = httpx.AsyncClient(timeout=10.0, headers={"User-Agent": self.user_agent})
    
    async def get_coordinates(self, place_name: str) -> Optional[LocationResponse]:
        # We get the latitude/longitude for a place name
        try:
            params = {"q": place_name, "format": "json", "limit": 1, "addressdetails": 1}
            response = await self.client.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                return None
            
            location = data[0]
            return LocationResponse(
                latitude=float(location["lat"]),
                longitude=float(location["lon"]),
                display_name=location.get("display_name", place_name),
                place_id=int(location.get("place_id", 0))
            )
        except Exception as e:
            logger.error(f"Error getting coordinates: {e}")
            return None
    
    async def close(self):
        await self.client.aclose()

