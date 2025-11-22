"""Repository Pattern for Query History

We can swap to MongoDB/PostgreSQL by
changing only this file.
"""

import aiosqlite
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class HistoryRepository:
    """Repository for query history operations"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    async def save_interaction(
        self,
        query: str,
        place_name: Optional[str] = None,
        user_ip: Optional[str] = None,
        has_weather: bool = False,
        has_places: bool = False,
        weather_temp: Optional[float] = None,
        weather_rain_prob: Optional[float] = None,
        places_count: int = 0,
        error: Optional[str] = None,
        success: bool = True
    ) -> int:
        """Save a query interaction to the database"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """INSERT INTO query_history 
                   (query, place_name, user_ip, has_weather, has_places, 
                    weather_temp, weather_rain_prob, places_count, error, success, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    query,
                    place_name,
                    user_ip,
                    1 if has_weather else 0,
                    1 if has_places else 0,
                    weather_temp,
                    weather_rain_prob,
                    places_count,
                    error,
                    1 if success else 0,
                    datetime.utcnow().isoformat()
                )
            )
            await db.commit()
            cursor = await db.execute("SELECT last_insert_rowid()")
            row = await cursor.fetchone()
            return row[0] if row else None
    
    async def get_recent(
        self,
        limit: int = 10,
        days: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get recent query history"""
        async with aiosqlite.connect(self.db_path) as db:
            query = """SELECT * FROM query_history"""
            params = []
            
            if days:
                cutoff_date = (datetime.utcnow() - timedelta(days=days)).isoformat()
                query += " WHERE created_at >= ?"
                params.append(cutoff_date)
            
            query += " ORDER BY created_at DESC LIMIT ?"
            params.append(limit)
            
            cursor = await db.execute(query, params)
            rows = await cursor.fetchall()
            
            columns = [description[0] for description in cursor.description]
            
            results = []
            for row in rows:
                row_dict = dict(zip(columns, row))
                row_dict['has_weather'] = bool(row_dict.get('has_weather', 0))
                row_dict['has_places'] = bool(row_dict.get('has_places', 0))
                row_dict['success'] = bool(row_dict.get('success', 1))
                results.append(row_dict)
            
            return results
    
    async def get_by_place(
        self,
        place_name: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Get query history for a specific place"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """SELECT * FROM query_history 
                   WHERE place_name = ? 
                   ORDER BY created_at DESC 
                   LIMIT ?""",
                (place_name, limit)
            )
            rows = await cursor.fetchall()
            
            columns = [description[0] for description in cursor.description]
            results = []
            for row in rows:
                row_dict = dict(zip(columns, row))
                row_dict['has_weather'] = bool(row_dict.get('has_weather', 0))
                row_dict['has_places'] = bool(row_dict.get('has_places', 0))
                row_dict['success'] = bool(row_dict.get('success', 1))
                results.append(row_dict)
            
            return results
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get query statistics"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("SELECT COUNT(*) FROM query_history")
            total = (await cursor.fetchone())[0]
            
            cursor = await db.execute("SELECT COUNT(*) FROM query_history WHERE success = 1")
            successful = (await cursor.fetchone())[0]
            
            cursor = await db.execute("SELECT COUNT(DISTINCT place_name) FROM query_history WHERE place_name IS NOT NULL")
            unique_places = (await cursor.fetchone())[0]
            
            return {
                "total_queries": total or 0,
                "successful_queries": successful or 0,
                "unique_places": unique_places or 0
            }

