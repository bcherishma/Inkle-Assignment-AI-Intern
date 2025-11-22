import re
from typing import Optional, Tuple
from app.models.schemas import TourismResponse, WeatherResponse, PlaceInfo
from app.agents.weather_agent import WeatherAgent
from app.agents.places_agent import PlacesAgent
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class TourismAIAgent:
    
    def __init__(
        self,
        weather_agent: WeatherAgent,
        places_agent: PlacesAgent
    ):
        self.weather_agent = weather_agent
        self.places_agent = places_agent
    
    def _extract_place_name(self, query: str) -> Optional[str]:
        # Extract place name from query - handles various natural language patterns
        query_clean = query.strip()
        
        # Common words to skip
        skip_words = {'the', 'and', 'or', 'can', 'what', 'where', 'how', 'when', 'why', 'is', 'are', 'will', 'want', 'to', 'in', 'at', 'for', 'my', 'i', 'me', 'we', 'our', 'a', 'an'}
        skip_words_upper = {w.capitalize() for w in skip_words} | {'The', 'And', 'Or', 'Can', 'What', 'Where', 'How', 'When', 'Why', 'I', 'My', 'Me', 'We', 'Our'}
        
        # Pattern 1: "going to [Place]" or "traveling to [Place]" or "visiting [Place]"
        patterns = [
            r'(?:going\s+to|traveling\s+to|travelling\s+to|travel\s+to|visit|visiting|visits|want\s+to\s+visit|plan\s+to\s+visit)\s+([A-Z][a-zA-Z\s]{2,}?)(?:,|\s+let|\s+what|\s+temperature|\s+places|\s+and|\s+)',
            r'(?:in|at)\s+([A-Z][a-zA-Z]{2,}(?:\s+[A-Z][a-zA-Z]{2,})*?)(?:\s*,|\s+let|\s+what|\s+temperature|\s+places|\s+the|\s+is|\s+are|\s*\?|$)',
            r'to\s+([A-Z][a-zA-Z]{2,}(?:\s+[A-Z][a-zA-Z]{2,})*?)(?:\s*,|\s+let|\s+what|\s+temperature|\s+places|\s+)',
            r'(?:place|city|location)\s+(?:is|called|named|in)\s+([A-Z][a-zA-Z]{2,}(?:\s+[A-Z][a-zA-Z]{2,})*?)(?:\s*,|\s+|$)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, query_clean, re.IGNORECASE)
            for match in matches:
                place = match.group(1).strip().rstrip('.,!?;:')
                # Clean up common prefixes/suffixes
                place = re.sub(r'^(the|a|an)\s+', '', place, flags=re.IGNORECASE)
                if place and len(place) > 2 and place.lower() not in skip_words:
                    # Remove trailing common words
                    words = place.split()
                    filtered = []
                    for w in words:
                        if w.lower() not in skip_words and w.rstrip('.,!?') not in skip_words_upper:
                            filtered.append(w.rstrip('.,!?'))
                    if filtered:
                        return ' '.join(filtered)
        
        # Split into sentences and look for capitalized words
        sentences = re.split(r'[.!?]\s+', query_clean)
        for sentence in sentences:
            words = sentence.split()
            capitalized_places = []
            for i, word in enumerate(words):
                cleaned = word.rstrip('.,!?;:')
                # Check if it's a capitalized word and not a common word
                if cleaned and cleaned[0].isupper() and len(cleaned) > 2:
                    if cleaned not in skip_words_upper:
                        capitalized_places.append(cleaned)
                        # Look ahead for additional capitalized words (multi-word places)
                        j = i + 1
                        while j < len(words) and j < i + 3:  # Max 3 words
                            next_word = words[j].rstrip('.,!?;:')
                            if next_word and next_word[0].isupper() and next_word not in skip_words_upper:
                                capitalized_places.append(next_word)
                                j += 1
                            else:
                                break
                        if capitalized_places:
                            result = ' '.join(capitalized_places)
                            # Double check it's not just common words
                            if result.lower() not in skip_words and len(result) > 2:
                                return result
                        capitalized_places = []
        
        # Pattern 3: Last resort - find any capitalized words that look like places
        words = query_clean.split()
        candidates = []
        for word in words:
            cleaned = word.rstrip('.,!?;:')
            if cleaned and cleaned[0].isupper() and len(cleaned) > 2 and cleaned not in skip_words_upper:
                candidates.append(cleaned)
        
        if candidates:
            # Take first few candidates, but skip if they're at the very start (likely sentence start)
            # If query starts with capitalized word, it might just be sentence capitalization
            if len(candidates) > 1 or (len(candidates) == 1 and not query_clean[0].isupper()):
                return ' '.join(candidates[:3])
        
        return None
    
    def _parse_intent(self, query: str) -> Tuple[bool, bool]:
        # Check what user wants - weather, places, or both (flexible natural language)
        query_lower = query.lower()
        
        # Weather keywords - more comprehensive
        weather_keywords = [
            'temperature', 'temp', 'weather', 'rain', 'rainfall', 'precipitation',
            'how hot', 'how cold', 'forecast', 'climate', 'sunny', 'cloudy',
            'snow', 'wind', 'humidity', 'degrees', 'celsius', 'fahrenheit',
            'chance of rain', 'will it rain', 'is it raining'
        ]
        wants_weather = any(keyword in query_lower for keyword in weather_keywords)
        
        places_keywords = [
            'places', 'place', 'visit', 'visiting', 'visits', 'attractions', 
            'attraction', 'see', 'tourist', 'tourism', 'sightseeing', 
            'monuments', 'monument', 'museums', 'museum', 'landmarks',
            'things to do', 'what to see', 'where to go', 'where to visit',
            'sights', 'parks', 'temples', 'palaces', 'beaches', 'locations',
            'recommendations', 'suggestions', 'must see', 'top places'
        ]
        wants_places = any(keyword in query_lower for keyword in places_keywords)
        
        # Context-based detection (if no explicit keywords)
        if not wants_weather and not wants_places:
            # Phrases that suggest planning/trip planning = places
            trip_keywords = ['plan', 'planning', 'trip', 'going', 'visit', 'travel', 'traveling', 'vacation']
            if any(keyword in query_lower for keyword in trip_keywords):
                wants_places = True
            # Phrases asking about the place itself
            elif any(phrase in query_lower for phrase in ['what can', 'what should', 'what are', 'where can', 'show me']):
                wants_places = True
        
        # If explicitly asking about both or using "and"
        if 'and' in query_lower or 'both' in query_lower or 'also' in query_lower:
            if wants_weather or wants_places:
                # If one intent is clear, check if other might be intended
                if 'temperature' in query_lower or 'weather' in query_lower:
                    wants_weather = True
                if 'places' in query_lower or 'visit' in query_lower or 'attractions' in query_lower:
                    wants_places = True
        
        return wants_weather, wants_places
    
    async def process_query(self, query: str, place_name: Optional[str] = None) -> TourismResponse:
        # Main function to process user query
        try:
            logger.info(f"TourismAIAgent: Processing query: {query}")
            
            # Extract place name if not provided
            if not place_name:
                place_name = self._extract_place_name(query)
            
            if not place_name:
                return TourismResponse(
                    success=False,
                    place_name="",
                    message="I couldn't identify the place name from your query. Please specify a place.",
                    error="PLACE_NOT_FOUND"
                )
            
            # Parse intent
            wants_weather, wants_places = self._parse_intent(query)
            
            # If no specific intent, default to places
            if not wants_weather and not wants_places:
                wants_places = True
            
            logger.info(f"TourismAIAgent: Place={place_name}, Weather={wants_weather}, Places={wants_places}")
            
            # Orchestrate child agents
            weather_result = None
            places_result = []
            
            if wants_weather:
                weather_result = await self.weather_agent.get_weather_info(place_name)
                if not weather_result:
                    return TourismResponse(
                        success=False,
                        place_name=place_name,
                        message=f"I don't know if this place exists: {place_name}. Could you check the spelling?",
                        error="PLACE_NOT_FOUND"
                    )
            
            if wants_places:
                places_result = await self.places_agent.get_tourist_places(place_name, limit=5)
                if not places_result:
                    # Check if place was found by trying weather agent
                    location_check = await self.weather_agent.get_weather_info(place_name)
                    if not location_check:
                        return TourismResponse(
                            success=False,
                            place_name=place_name,
                            message=f"I don't know if this place exists: {place_name}. Could you check the spelling?",
                            error="PLACE_NOT_FOUND"
                        )
                    # Place exists but no tourist attractions found (might be API timeout or no data)
                    # Still return weather if available, but mention places couldn't be fetched
                    if weather_result:
                        return TourismResponse(
                            success=True,
                            place_name=place_name,
                            weather=weather_result,
                            places=[],
                            message=f"In {place_name} it's currently {weather_result.temperature:.0f}°C with a chance of {weather_result.rain_probability:.0f}% to rain. I couldn't fetch tourist attractions at the moment (the places API might be slow or unavailable)."
                        )
                    return TourismResponse(
                        success=True,
                        place_name=place_name,
                        weather=weather_result,
                        places=[],
                        message=f"In {place_name} I couldn't find any tourist attractions nearby, or the places API is currently unavailable."
                    )
            
            # Build response message
            message_parts = []
            
            if weather_result:
                message_parts.append(
                    f"In {place_name} it's currently {weather_result.temperature:.0f}°C "
                    f"with a chance of {weather_result.rain_probability:.0f}% to rain."
                )
            
            if places_result:
                if message_parts:
                    message_parts.append("And these are the places you can go:")
                else:
                    message_parts.append(f"In {place_name} these are the places you can go,")
                
                place_names = [place.name for place in places_result]
                # Add places as separate lines in message
                message_parts.append("\n\n" + "\n".join(place_names))
            
            message = " ".join(message_parts) if message_parts else f"Information about {place_name}."
            
            return TourismResponse(
                success=True,
                place_name=place_name,
                weather=weather_result,
                places=places_result,
                message=message
            )
            
        except Exception as e:
            logger.error(f"TourismAIAgent: Unexpected error - {e}")
            return TourismResponse(
                success=False,
                place_name=place_name or "",
                message="An error occurred while processing your request. Please try again.",
                error=str(e)
            )

