import httpx
from typing import List
from app.models.schemas import PlaceInfo
from app.utils.logger import setup_logger
from app.utils.cache import places_cache

logger = setup_logger(__name__)


class PlacesClient:
    def __init__(self, base_url: str = "https://overpass-api.de/api/interpreter"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=45.0)
    
    def _build_overpass_query(self, latitude: float, longitude: float, radius: int = 25000, limit: int = 30) -> str:
        query = f"""[out:json][timeout:30];
(
  // Tourism attractions - highest priority
  node["tourism"~"attraction|museum|gallery|zoo|theme_park|viewpoint|information|artwork"](around:{radius},{latitude},{longitude});
  way["tourism"~"attraction|museum|gallery|zoo|theme_park|viewpoint|information|artwork"](around:{radius},{latitude},{longitude});
  relation["tourism"~"attraction|museum|gallery|zoo|theme_park|viewpoint|information|artwork"](around:{radius},{latitude},{longitude});
  
  // Historic sites
  node["historic"](around:{radius},{latitude},{longitude});
  way["historic"](around:{radius},{latitude},{longitude});
  relation["historic"](around:{radius},{latitude},{longitude});
  
  // Leisure/Parks
  node["leisure"~"park|garden|nature_reserve|stadium|sports_centre"](around:{radius},{latitude},{longitude});
  way["leisure"~"park|garden|nature_reserve|stadium|sports_centre"](around:{radius},{latitude},{longitude});
  relation["leisure"~"park|garden|nature_reserve|stadium|sports_centre"](around:{radius},{latitude},{longitude});
  
  // Religious places
  node["amenity"~"place_of_worship"](around:{radius},{latitude},{longitude});
  way["amenity"~"place_of_worship"](around:{radius},{latitude},{longitude});
  relation["amenity"~"place_of_worship"](around:{radius},{latitude},{longitude});
);
out center {limit};"""
        return query
    
    async def get_tourist_places(self, latitude: float, longitude: float, place_name: str, limit: int = 5) -> List[PlaceInfo]:
        # Check cache first (1 hour TTL)
        cache_key = f"places:{latitude}:{longitude}:{limit}"
        cached_result = places_cache.get(cache_key)
        if cached_result is not None:
            logger.debug(f"Using cached places data for {place_name}")
            return cached_result
        
        try:
            logger.info(f"Fetching places near coordinates ({latitude}, {longitude}) for '{place_name}'")
            query = self._build_overpass_query(latitude, longitude, limit=30)
            response = await self.client.post(self.base_url, content=query, headers={"Content-Type": "text/plain"})
            
            if response.status_code != 200:
                logger.error(f"Places API error: HTTP {response.status_code} - {response.text[:200]}")
                return []
            
            data = response.json()
            
            if "remark" in data and "error" in data.get("remark", "").lower():
                logger.error(f"Places API error: {data.get('remark')}")
                return []
            
            elements = data.get("elements", [])
            
            if not elements:
                logger.warning(f"No places found near ({latitude}, {longitude}) for '{place_name}'")
                return []
            
            places = []
            seen_names = set()
            
            for element in elements:
                if len(places) >= limit:
                    break
                    
                tags = element.get("tags", {})
                name = tags.get("name")
                
                if not name:
                    continue
                
                name_lower = name.lower().strip()
                if name_lower in seen_names:
                    continue
                
                element_lat = element.get("lat") or (element.get("center", {}).get("lat") if "center" in element else None)
                element_lon = element.get("lon") or (element.get("center", {}).get("lon") if "center" in element else None)
                
                if element_lat and element_lon:
                    import math
                    distance = math.sqrt((element_lat - latitude)**2 + (element_lon - longitude)**2) * 111  
                    if distance > 30:  
                        logger.debug(f"Place '{name}' is {distance:.1f}km away from requested location, skipping")
                        continue
                
                seen_names.add(name_lower)
                place_type = (
                    tags.get("tourism") or 
                    tags.get("historic") or 
                    tags.get("leisure") or 
                    tags.get("amenity") or 
                    tags.get("place") or
                    "attraction"
                )
                if place_type and isinstance(place_type, str):
                    place_type = place_type.replace("_", " ").title()
                
                places.append(PlaceInfo(name=name, type=place_type, description=tags.get("description")))
                logger.debug(f"Added place {len(places)}/{limit}: {name} ({place_type})")
            
            logger.info(f"Found {len(places)} places for '{place_name}' (requested {limit})")
            
            # Cache the result for 1 hour (3600 seconds)
            places_cache.set(cache_key, places, ttl_seconds=3600)
            logger.debug(f"Cached places data for {place_name}")
            
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

