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
            clean_place = place_name.strip()
            
            # Common city-country mappings to improve accuracy
            city_hints = {
                "bangalore": "India",
                "mumbai": "India",
                "delhi": "India",
                "kolkata": "India",
                "chennai": "India",
                "hyderabad": "India",
                "pune": "India",
                "ahmedabad": "India",
                "jaipur": "India",
                "surat": "India",
                "lucknow": "India",
                "kanpur": "India",
                "nagpur": "India",
                "indore": "India",
                "thane": "India",
                "bhopal": "India",
                "visakhapatnam": "India",
                "patna": "India",
                "vadodara": "India",
                "paris": "France",
                "london": "United Kingdom",
                "new york": "United States",
                "tokyo": "Japan",
                "sydney": "Australia",
                "dubai": "United Arab Emirates",
            }
            
            place_lower = clean_place.lower()
            country_hint = None
            for city, country in city_hints.items():
                if city in place_lower:
                    country_hint = country
                    break
            
            query = clean_place
            if country_hint and country_hint.lower() not in place_lower:
                query = f"{clean_place}, {country_hint}"
            
            params = {
                "q": query, 
                "format": "json", 
                "limit": 5,  
                "addressdetails": 1,
                "namedetails": 1
            }
            response = await self.client.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                logger.warning(f"No results found for: {place_name}")
                return None
            
            place_lower = clean_place.lower()
            best_match = None
            best_score = 0
            
            for location in data:
                display_name = location.get("display_name", "").lower()
                name = location.get("name", "").lower()
                address = location.get("address", {})
                
                score = 0
                
                if place_lower == name or place_lower in name.split(",")[0]:
                    score += 30
                
                if place_lower in display_name:
                    score += 20
                
                if country_hint:
                    country_lower = country_hint.lower()
                    if country_lower in display_name:
                        score += 25  
                    else:
                        score -= 15  
                
                place_type = location.get("type", "")
                if place_type in ["city", "town", "administrative"]:
                    score += 10
                
                if display_name.startswith(place_lower):
                    score += 15
                
                if country_hint and address:
                    country_code = address.get("country_code", "").lower()
                    country_name = address.get("country", "").lower()
                    country_hint_lower = country_hint.lower()
                    if country_hint_lower in country_name or country_code in ["in", "us", "gb", "fr", "jp", "au", "ae"]:
                        if country_hint_lower == "india" and country_code == "in":
                            score += 20
                        elif country_hint_lower in country_name:
                            score += 20
                
                if score > best_score:
                    best_score = score
                    best_match = location
            
            if best_match and best_score < 0 and country_hint:
                logger.warning(f"Best match has low score ({best_score}), trying without country hint")
                params_no_hint = {
                    "q": clean_place,
                    "format": "json",
                    "limit": 5,
                    "addressdetails": 1,
                    "namedetails": 1
                }
                response = await self.client.get(self.base_url, params=params_no_hint)
                response.raise_for_status()
                data = response.json()
                
                for location in data:
                    display_name = location.get("display_name", "").lower()
                    address = location.get("address", {})
                    score = 0
                    if place_lower in display_name:
                        score += 20
                    if country_hint and country_hint.lower() in display_name:
                        score += 25
                    if address and address.get("country", "").lower() == country_hint.lower():
                        score += 20
                    if score > best_score:
                        best_score = score
                        best_match = location
            
            location = best_match if best_match else data[0]
            
            display_name = location.get("display_name", "").lower()
            name = location.get("name", "").lower()
            
            if place_lower not in display_name and place_lower not in name:
                logger.warning(f"Place name '{place_name}' not found in geocoding result: {display_name}")
            
            logger.info(f"Geocoding '{place_name}' -> {location.get('display_name', 'Unknown')} ({location.get('lat')}, {location.get('lon')})")
            
            return LocationResponse(
                latitude=float(location["lat"]),
                longitude=float(location["lon"]),
                display_name=location.get("display_name", place_name),
                place_id=int(location.get("place_id", 0))
            )
        except Exception as e:
            logger.error(f"Error getting coordinates for '{place_name}': {e}")
            return None
    
    async def close(self):
        await self.client.aclose()

