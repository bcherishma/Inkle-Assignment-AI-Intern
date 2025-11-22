import aiosqlite
from app.config import Settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


def _get_db_path(settings: Settings) -> str:
    """Extract database path from settings"""
    db_url = settings.database_url
    if db_url.startswith("sqlite+aiosqlite:///"):
        return db_url.replace("sqlite+aiosqlite:///", "")
    elif db_url.startswith("sqlite:///"):
        return db_url.replace("sqlite:///", "")
    return db_url


async def init_db(settings: Settings):
    """Initialize database and create tables"""
    db_path = _get_db_path(settings)
    logger.info(f"Initializing database: {db_path}")
    
    async with await aiosqlite.connect(db_path) as db:
        # Create query_history table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS query_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                place_name TEXT,
                user_ip TEXT,
                has_weather INTEGER DEFAULT 0,
                has_places INTEGER DEFAULT 0,
                weather_temp REAL,
                weather_rain_prob REAL,
                places_count INTEGER DEFAULT 0,
                error TEXT,
                success INTEGER DEFAULT 1,
                created_at TEXT NOT NULL
            )
        """)
        
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_place_name 
            ON query_history(place_name)
        """)
        
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_created_at 
            ON query_history(created_at)
        """)
        
        await db.commit()
    
    logger.info("Database schema initialized successfully")


async def close_db():
    """Close database connections (no-op for SQLite, but kept for consistency)"""
    logger.info("Database connections closed")
