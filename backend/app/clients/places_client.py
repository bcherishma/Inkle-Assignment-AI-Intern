import httpx
from typing import List
from app.models.schemas import PlaceInfo
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class PlacesClient:
    def __init__(self, base_url: str = "https://overpass-api.de/api/interpreter"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=45.0)
    
    def _build_overpass_query(self, latitude: float, longitude: float, radius: int = 8000, limit: int = 5) -> str:
        query = f"""[out:json][timeout:20];
(
  node["tourism"]["name"](around:{radius},{latitude},{longitude});
  way["tourism"]["name"](around:{radius},{latitude},{longitude});
  relation["tourism"]["name"](around:{radius},{latitude},{longitude});
);
out center {limit};"""
        return query
    
    async def get_tourist_places(self, latitude: float, longitude: float, place_name: str, limit: int = 5) -> List[PlaceInfo]:
        try:
            query = self._build_overpass_query(latitude, longitude, limit=limit)
            response = await self.client.post(self.base_url, content=query, headers={"Content-Type": "text/plain"})
            
            if response.status_code != 200:
                logger.error(f"Places API error: HTTP {response.status_code} - {response.text[:200]}")
                return []
            
            data = response.json()
            
            if "remark" in data and "error" in data.get("remark", "").lower():
                logger.error(f"Places API error: {data.get('remark')}")
                return []
            
            elements = data.get("elements", [])
            
            places = []
            seen_names = set()
            
            for element in elements:
                tags = element.get("tags", {})
                name = tags.get("name")
                
                if not name or name in seen_names:
                    continue
                
                seen_names.add(name)
                # We can get place type from the various tags
                place_type = (
                    tags.get("tourism") or 
                    tags.get("historic") or 
                    tags.get("leisure") or 
                    tags.get("amenity") or 
                    tags.get("place") or
                    "attraction"
                )
                
                places.append(PlaceInfo(name=name, type=place_type, description=tags.get("description")))
                
                if len(places) >= limit:
                    break
            
            return places
        except httpx.TimeoutException:
            logger.error(f"Places API timeout for {place_name}")
            return []
        except httpx.HTTPStatusError as e:
            logger.error(f"Places API HTTP error: {e.response.status_code} - {e.response.text[:200]}")
            return []
        except Exception as e:
            logger.error(f"Places API error: {type(e).__name__}: {str(e)}")
            return []
    
    async def close(self):
        await self.client.aclose()

