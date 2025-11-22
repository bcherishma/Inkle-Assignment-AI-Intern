# Places Agent - Child Agent 2
from typing import List
from app.models.schemas import PlaceInfo
from app.clients.geocoding_client import GeocodingClient
from app.clients.places_client import PlacesClient


class PlacesAgent:
    def __init__(self, geocoding_client: GeocodingClient, places_client: PlacesClient):
        self.geocoding_client = geocoding_client
        self.places_client = places_client
    
    async def get_tourist_places(self, place_name: str, limit: int = 5) -> List[PlaceInfo]:
        # Get coordinates first, then tourist places
        location = await self.geocoding_client.get_coordinates(place_name)
        if not location:
            return []
        
        places = await self.places_client.get_tourist_places(location.latitude, location.longitude, place_name, limit=limit)
        return places

