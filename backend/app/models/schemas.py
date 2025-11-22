"""Pydantic models for request/response"""

from pydantic import BaseModel, Field
from typing import Optional, List
from app.models.base import BaseResponse


class LocationResponse(BaseModel):
    """Location coordinates response"""
    latitude: float
    longitude: float
    display_name: str
    place_id: int


class WeatherResponse(BaseModel):
    """Weather information response"""
    temperature: float = Field(..., description="Current temperature in Celsius")
    rain_probability: float = Field(..., description="Probability of rain in percentage")
    place_name: str


class PlaceInfo(BaseModel):
    """Tourist place information"""
    name: str
    type: Optional[str] = None
    description: Optional[str] = None


class PlacesResponse(BaseModel):
    """Tourist places response"""
    places: List[PlaceInfo]
    place_name: str


class TourismRequest(BaseModel):
    """Tourism query request"""
    query: str = Field(..., description="User query about a place")
    place: Optional[str] = Field(None, description="Optional explicit place name")


class TourismResponse(BaseResponse):
    """Complete tourism response"""
    place_name: str
    weather: Optional[WeatherResponse] = None
    places: Optional[List[PlaceInfo]] = None
    error: Optional[str] = None

