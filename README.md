# Tourism AI Multi-Agent System

A production-ready multi-agent tourism system that provides weather information and tourist attraction suggestions for any place. The system uses a parent agent to orchestrate child agents for weather and places information.

## Architecture

- **Parent Agent**: Tourism AI Agent (orchestrates the system)
- **Child Agent 1**: Weather Agent (fetches current/forecast weather using Open-Meteo API)
- **Child Agent 2**: Places Agent (suggests up to 5 tourist attractions using Overpass API)

## Features

- 🔍 **Intelligent Place Detection**: Automatically extracts place names from natural language queries
- 🌤️ **Weather Information**: Current temperature and rain probability
- 📍 **Tourist Attractions**: Up to 5 nearby tourist attractions, monuments, parks, and museums
- 🛡️ **Error Handling**: Graceful handling of non-existent places
- 🚀 **Production Ready**: Dockerized, scalable, and well-structured
- 📝 **API Documentation**: Auto-generated Swagger/OpenAPI docs

## Tech Stack

- **Python 3.11**
- **FastAPI** - Modern, fast web framework
- **Pydantic** - Data validation
- **httpx** - Async HTTP client
- **Open-Meteo API** - Weather data
- **Overpass API** - OpenStreetMap data for tourist attractions
- **Nominatim API** - Geocoding (place name to coordinates)

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── parent_agent.py  # Tourism AI Agent (orchestrator)
│   │   ├── weather_agent.py # Weather Agent
│   │   └── places_agent.py  # Places Agent
│   ├── clients/
│   │   ├── __init__.py
│   │   ├── geocoding_client.py  # Nominatim API client
│   │   ├── weather_client.py    # Open-Meteo API client
│   │   └── places_client.py     # Overpass API client
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py      # Application configuration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py          # Base model classes
│   │   └── schemas.py       # Pydantic request/response models
│   └── utils/
│       ├── __init__.py
│       └── logger.py        # Logging configuration
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Installation

### Prerequisites

- Python 3.11 or higher
- pip
- Docker (optional, for containerized deployment)

### Local Development

1. **Clone the repository** (if applicable)

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional):
   ```bash
   cp .env.example .env
   # Edit .env if needed
   ```

5. **Run the application**:
   ```bash
   python -m app.main
   ```

   Or using uvicorn directly:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access the API**:
   - API Base: http://localhost:8000
   - API Documentation: http://localhost:8000/docs (Swagger UI)
   - Alternative docs: http://localhost:8000/redoc (ReDoc)
   - Health Check: http://localhost:8000/health

## Docker Deployment

### Using Docker Compose (Recommended)

```bash
docker-compose up -d
```

This will build and start the container. The API will be available at http://localhost:8000

### Using Docker directly

1. **Build the image**:
   ```bash
   docker build -t tourism-ai-system .
   ```

2. **Run the container**:
   ```bash
   docker run -d -p 8000:8000 --name tourism-ai tourism-ai-system
   ```

## API Usage

### Endpoint: `POST /query`

Query the tourism system with natural language.

**Request Body**:
```json
{
  "query": "I'm going to go to Bangalore, let's plan my trip.",
  "place": null  // Optional: explicit place name
}
```

**Response**:
```json
{
  "place_name": "Bangalore",
  "weather": {
    "temperature": 24.0,
    "rain_probability": 35.0,
    "place_name": "Bangalore"
  },
  "places": [
    {"name": "Lalbagh", "type": "park", "description": null},
    {"name": "Sri Chamarajendra Park", "type": "park", "description": null},
    {"name": "Bangalore palace", "type": "tourism", "description": null},
    {"name": "Bannerghatta National Park", "type": "park", "description": null},
    {"name": "Jawaharlal Nehru Planetarium", "type": "museum", "description": null}
  ],
  "message": "In Bangalore these are the places you can go, Lalbagh\nSri Chamarajendra Park\n...",
  "error": null
}
```

### Example Queries

1. **Weather only**:
   ```json
   {
     "query": "I'm going to go to Bangalore, what is the temperature there"
   }
   ```

2. **Places only**:
   ```json
   {
     "query": "I'm going to go to Bangalore, let's plan my trip."
   }
   ```

3. **Both weather and places**:
   ```json
   {
     "query": "I'm going to go to Bangalore, what is the temperature there? And what are the places I can visit?"
   }
   ```

### Health Check: `GET /health`

Check if the service is running.

```bash
curl http://localhost:8000/health
```

## Example Responses

### Example 1: Places Only
**Input**: "I'm going to go to Bangalore, let's plan my trip."

**Output**:
```
In Bangalore these are the places you can go, 

Lalbagh
Sri Chamarajendra Park
Bangalore palace
Bannerghatta National Park
Jawaharlal Nehru Planetarium
```

### Example 2: Weather Only
**Input**: "I'm going to go to Bangalore, what is the temperature there"

**Output**:
```
In Bangalore it's currently 24°C with a chance of 35% to rain.
```

### Example 3: Both Weather and Places
**Input**: "I'm going to go to Bangalore, what is the temperature there? And what are the places I can visit?"

**Output**:
```
In Bangalore it's currently 24°C with a chance of 35% to rain. And these are the places you can go:

Lalbagh
Sri Chamarajendra Park
Bangalore palace
Bannerghatta National Park
Jawaharlal Nehru Planetarium
```

## Error Handling

If a place doesn't exist or can't be found:

```json
{
  "place_name": "InvalidPlace",
  "message": "I don't know if this place exists: InvalidPlace. Could you check the spelling?",
  "error": "PLACE_NOT_FOUND",
  "weather": null,
  "places": null
}
```

## Testing

### Manual Testing with curl

```bash
# Test query endpoint
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "I'\''m going to go to Bangalore, let'\''s plan my trip."
  }'

# Test health check
curl http://localhost:8000/health
```

### Testing with Python

```python
import httpx

response = httpx.post(
    "http://localhost:8000/query",
    json={"query": "I'm going to go to Bangalore, what is the temperature there?"}
)
print(response.json())
```

## Production Deployment

### Environment Variables

Create a `.env` file or set environment variables:

```bash
NOMINATIM_BASE_URL=https://nominatim.openstreetmap.org/search
OPEN_METEO_BASE_URL=https://api.open-meteo.com/v1/forecast
OVERPASS_BASE_URL=https://overpass-api.de/api/interpreter
USER_AGENT=TourismAI/1.0
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
```

### Production Considerations

1. **Rate Limiting**: Add rate limiting middleware for production
2. **Caching**: Consider adding Redis for caching geocoding and weather results
3. **Monitoring**: Add logging aggregation and monitoring (e.g., Prometheus, Grafana)
4. **Security**: Add authentication/authorization if needed
5. **Load Balancing**: Use a reverse proxy (nginx) with multiple instances
6. **Database**: Consider storing query history if needed

### Deploy to Cloud Platforms

#### AWS (using ECS/Fargate)
```bash
# Build and push to ECR
docker build -t tourism-ai-system .
# Push to ECR and deploy to ECS
```

#### Google Cloud Platform (using Cloud Run)
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/tourism-ai-system
gcloud run deploy tourism-ai-system --image gcr.io/PROJECT_ID/tourism-ai-system
```

#### Heroku
```bash
heroku create tourism-ai-system
heroku container:push web
heroku container:release web
```

## API Rate Limits

- **Nominatim API**: 1 request per second (be respectful, use User-Agent)
- **Open-Meteo API**: No strict limits, but reasonable use
- **Overpass API**: No strict limits, but be respectful

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Troubleshooting

### Issue: "Place not found" errors
- Verify the place name spelling
- Try using more specific place names (e.g., "Bangalore, India")
- Check Nominatim API availability

### Issue: No tourist attractions found
- The place might not have tagged attractions in OpenStreetMap
- Try a different place or larger city
- Check Overpass API status

### Issue: Weather data unavailable
- Check Open-Meteo API status
- Verify coordinates are valid
- Some remote locations may not have weather data

## Support

For issues or questions, please open an issue in the repository.

