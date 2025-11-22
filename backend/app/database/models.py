from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class QueryHistory(Base):
    """Query history model"""
    __tablename__ = "query_history"
    
    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text, nullable=False, index=True)
    place_name = Column(String(255), nullable=True, index=True)
    user_ip = Column(String(50), nullable=True)
    
    has_weather = Column(Integer, default=0)  
    has_places = Column(Integer, default=0)  
    weather_temp = Column(Float, nullable=True)
    weather_rain_prob = Column(Float, nullable=True)
    places_count = Column(Integer, default=0)
    
    error = Column(String(100), nullable=True)
    success = Column(Integer, default=1)  
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "query": self.query,
            "place_name": self.place_name,
            "has_weather": bool(self.has_weather),
            "has_places": bool(self.has_places),
            "weather_temp": self.weather_temp,
            "weather_rain_prob": self.weather_rain_prob,
            "places_count": self.places_count,
            "error": self.error,
            "success": bool(self.success),
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
