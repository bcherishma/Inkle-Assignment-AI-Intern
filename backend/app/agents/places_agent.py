from typing import List
from app.models.schemas import PlaceInfo
from app.clients.geocoding_client import GeocodingClient
from app.clients.places_client import PlacesClient


class PlacesAgent:
    def __init__(self, geocoding_client: GeocodingClient, places_client: PlacesClient):
        self.geocoding_client = geocoding_client
        self.places_client = places_client
    
    async def get_tourist_places(self, place_name: str, limit: int = 5) -> List[PlaceInfo]:
        location = await self.geocoding_client.get_coordinates(place_name)
        if not location:
            return []
        
        # Validate that the location matches the requested place
        display_name_lower = location.display_name.lower()
        place_name_lower = place_name.lower()
        
        if place_name_lower not in display_name_lower:
            parts = display_name_lower.split(',')
            city_match = any(place_name_lower in part.strip() or part.strip() in place_name_lower for part in parts[:2])
            if not city_match:
                from app.utils.logger import setup_logger
                logger = setup_logger(__name__)
                logger.warning(f"Geocoded location '{location.display_name}' may not match requested place '{place_name}'")
        
        places = await self.places_client.get_tourist_places(location.latitude, location.longitude, place_name, limit=limit)
        return places

