# Tourism AI Backend

FastAPI backend for the Tourism AI Multi-Agent System.

## Structure

```
backend/
├── app/
│   ├── agents/          # Multi-agent system (Parent, Weather, Places)
│   ├── clients/         # API clients (Geocoding, Weather, Places)
│   ├── config/          # Configuration and settings
│   ├── database/        # Database connection and schema
│   ├── models/          # Pydantic models
│   ├── repositories/    # Repository Pattern for data access
│   ├── utils/           # Utility functions (logging)
│   └── main.py          # FastAPI application
├── requirements.txt      # Python dependencies
└── run.py               # Run script
```

## Setup

1. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional):
   ```bash
   # Create .env file in backend/ or root directory
   cp ../.env.example .env
   # Edit .env if needed
   ```

## Running

### Option 1: Using run.py (Recommended)
```bash
python run.py
```

### Option 2: Using uvicorn directly
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: http://localhost:8000

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Environment Variables

- `API_HOST` - Server host (default: 0.0.0.0)
- `API_PORT` - Server port (default: 8000)
- `LOG_LEVEL` - Logging level (default: INFO)
- `DATABASE_URL` - SQLite database path (default: sqlite+aiosqlite:///./tourism_ai.db)

