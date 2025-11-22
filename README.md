# 🌍 WanderWise: Tourism AI Multi-Agent System

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?logo=typescript&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker&logoColor=white)
![Render](https://img.shields.io/badge/Deployed_on-Render-46E3B7?logo=render&logoColor=white)

**WanderWise** is a production-ready multi-agent tourism recommendation system. It utilizes an orchestrated multi-agent architecture to provide real-time weather forecasts and curated tourist attractions for any location globally.

---

## 🚀 Live Demo

| Service | URL |
| :--- | :--- |
| **Frontend UI** | https://wanderwise-frontend-9zer.onrender.com |
| **Backend API** | https://wanderwise-backend-r9ml.onrender.com |
| **API Docs** | https://wanderwise-backend-r9ml.onrender.com/docs |

---

## 🧠 System Architecture

A production-ready multi-agent tourism recommendation system providing:

- Real-time **weather forecasts**
- Curated **tourist attractions**
- Intelligent **place extraction**
- Complete **query history + analytics**

Built using an orchestrated multi-agent architecture with FastAPI, async Python, SQLite, and a modern React/TypeScript frontend.

---

# 🧠 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      User Query                              │
│         "I'm going to Bangalore, what's the weather?"        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Parent Agent (TourismAIAgent)                 │
│  • Extracts place name from natural language                │
│  • Parses user intent (weather/places/both)                 │
│  • Orchestrates child agents in parallel                    │
└──────┬──────────────────────────────┬───────────────────────┘
       │                              │
       ▼                              ▼
┌──────────────────┐        ┌──────────────────┐
│  Weather Agent    │        │   Places Agent   │
│  • Geocoding      │        │   • Geocoding    │
│  • Open-Meteo     │        │   • Overpass OSM │
└──────┬────────────┘        └──────┬───────────┘
       │                             │
       ▼                             ▼
┌──────────────────┐        ┌──────────────────┐
│   Open-Meteo API  │        │  Overpass API     │
│  (Weather Data)   │        │ (Tourist Places)  │
└──────────────────┘        └───────────────────┘
       │                             │
       └─────────────┬───────────────┘
                     ▼
        ┌────────────────────────┐
        │   Response Aggregation │
        │   + Query History      │
        └────────────┬───────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │      User Response     │
        └────────────────────────┘
```

Key components:
- Parent Agent: orchestrates parsing, intent detection, parallel child calls, aggregation.
- Weather Agent: geocodes -> Open‑Meteo for weather (temperature, rain probability).
- Places Agent: geocodes -> Overpass (OSM) to find up to 5 attractions (parks, museums, monuments).
- Geocoding: Nominatim (OSM) for place → lat/lon normalization.
- Persistence: SQLite via aiosqlite (async), repository pattern for history and stats.
- API: FastAPI with auto-generated OpenAPI/Swagger.

---

# ✨ Features

### 🧭 Multi-Agent Intelligence
- Parent Agent orchestrates WeatherAgent + PlacesAgent
- Extracts place names from natural language queries
- Combines weather + attraction results elegantly

### 🌤 Weather Data  
- Temperature  
- Rain probability  
- Location normalization  

### 🗺 Tourist Attractions  
- Up to 5 nearby attractions  
- Based on OpenStreetMap (Overpass API)  
- Parks, museums, monuments, landmarks  

### 🗃 Query History + Analytics  
- Stores past queries  
- Computes statistics  
- Filter by date / place  
- SQLite + async I/O  

### 🐳 Production-ready  
- Dockerfile for backend  
- Render deployment  
- CORS configured  
- API documentation auto-generated  

---

# 🛠 Tech Stack

### Backend
- Python 3.11  
- FastAPI  
- Async httpx  
- Async aiosqlite  
- Pydantic V2  
- SQLite  
- Open-Meteo, Nominatim, Overpass APIs  

### Frontend
- React 18  
- TypeScript  
- Vite  
- Axios  

---

# 📦 Project Structure

```
.
├── backend/
│ ├── app/
│ │ ├── main.py # FastAPI entry point
│ │ ├── agents/ # Parent + child agents
│ │ ├── clients/ # API clients
│ │ ├── config/ # Settings
│ │ ├── database/ # DB initialization
│ │ ├── repositories/ # Query history storage
│ │ ├── models/ # Schemas
│ │ └── utils/ # Logger
│ ├── run.py # Run script
│ └── requirements.txt
│
├── frontend/
│ ├── src/
│ │ ├── components/ # UI components
│ │ ├── services/api.ts # API calls
│ │ ├── types/ # TS interfaces
│ │ └── App.tsx
│ ├── index.html
│ ├── package.json
│ └── vite.config.ts
│
├── Dockerfile # Backend Dockerfile
├── docker-compose.yml # Local dev only
├── README.md # You are here
└── RUN.md
```

---

# 📥 Installation — Local Development

Prerequisites:
- Python 3.11+
- Node.js v18+ and npm/yarn
- Docker (optional)

Clone:
```bash
git clone https://github.com/bcherishma/Inkle-Assignment-AI-Intern.git
cd Inkle-Assignment-AI-Intern
```

Backend:
```bash
cd backend
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

Frontend:
```bash
cd frontend
npm install
# or
yarn install
```

Environment variables:
```bash
# root .env (copy from .env.example)
cp .env.example .env
# frontend (if separate)
cd frontend
cp .env.example .env.local
```
Example backend env variables:
```
NOMINATIM_BASE_URL=https://nominatim.openstreetmap.org/search
OPEN_METEO_BASE_URL=https://api.open-meteo.com/v1/forecast
OVERPASS_BASE_URL=https://overpass-api.de/api/interpreter
USER_AGENT=TourismAI/1.0
API_HOST=0.0.0.0
LOG_LEVEL=INFO
```

Run locally:
- Backend:
  ```bash
  cd backend
  # dev:
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
  # or
  python run.py
  ```
- Frontend:
  ```bash
  cd frontend
  npm run dev
  ```

Access:
- Frontend UI: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

---

# 🐳 Docker — Local Development (recommended)

Build & run:
```bash
docker-compose up -d --build
docker-compose ps
docker-compose logs -f
```

Access same endpoints as above. Note: docker-compose is intended for local development; Render uses the Dockerfile and their build flow.

---

## Render Deployment Notes (critical)

- Render supplies $PORT — app MUST bind to $PORT (run.py handles this).
- CORS must include the exact frontend URL. Example:
  ```py
  allow_origins = [
    "https://wanderwise-frontend-9zer.onrender.com",
    "http://localhost:5173"
  ]
  ```
  Incorrect CORS causes OPTIONS /query 400.
- For frontend, set:
  ```
  VITE_API_BASE_URL=https://wanderwise-backend-r9ml.onrender.com
  ```

---

# 📡 API Reference

## POST /query
- Description: send a natural-language query (weather / places / both).
- Request:
  ```json
  {
    "query": "I'm going to Bangalore, what is the temperature there?",
    "place": null
  }
  ```
- Response (example):
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
      ...
    ],
    "message": "In Bangalore it's currently 24°C with a chance of 35% to rain. Places: Lalbagh, ...",
    "success": true,
    "error": null
  }
  ```

## GET /health
- Health check. Returns 200 OK.

## GET /history
- Query params: limit (default 10), days (optional)
- Returns recent queries.

## GET /history/stats
- Returns total queries, successful queries, unique places, etc.

## GET /history/place/{place_name}
- Returns history filtered by place.

All endpoints are documented in the auto-generated Swagger UI at /docs.

---

# 🔎 Examples

cURL — Weather and Places:
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query":"I am going to Bangalore, what's the weather and places?"}'
```

Python:
```python
import requests
resp = requests.post("http://localhost:8000/query",
                     json={"query": "What's the weather in Paris?"})
print(resp.json())
```

TypeScript / Fetch:
```ts
const resp = await fetch('http://localhost:8000/query', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({ query: "What's the weather in Paris?" })
});
const data = await resp.json();
console.log(data);
```

---

# ⚠️ Error Handling

If place not found:
```json
{
  "place_name": "InvalidPlace",
  "message": "I don't know if this place exists: InvalidPlace. Could you check the spelling?",
  "error": "PLACE_NOT_FOUND",
  "weather": null,
  "places": null,
  "success": false
}
```

Upstream failures (Nominatim / Overpass / Open-Meteo) are handled gracefully with informative messages and retries where appropriate.

---

# 📐 Architecture Decisions (summary)

- Async Python (FastAPI + httpx + aiosqlite) → parallel external calls, low latency.
- SQLite → zero-config, portable, suitable for demo/prototype and small production use. Repository pattern keeps DB replaceable.
- Modular agent design → isolated responsibilities, easy to extend/add agents (e.g., transit, events).

---

# 🧾 Rate Limits & Etiquette

- Nominatim: respect their usage policy (≈1 req/sec). Use USER_AGENT header.
- Overpass & Open-Meteo: be courteous; cache frequent queries.

---

# 🐞 Troubleshooting

- OPTIONS /query 400 → Check CORS allow_origins includes exact frontend URL.
- Place not found → increase specificity ("Bangalore, India") or check Nominatim availability.
- No attractions returned → OSM may lack tags for some locations; try a larger city.
- Backend sleeping on Render → allow 30–60s for wake-up on first request (free tier).

---

# 🤝 Contributing

1. Fork the repo  
2. Create branch: git checkout -b feat/your-feature  
3. Add tests and run them  
4. Open a PR with a clear description  

Please follow code style (Black / isort for Python, ESLint + Prettier for frontend).

---


# 📫 Contact

- Email: cherishmawork@gmail.com  
- LinkedIn: https://www.linkedin.com/in/cherishma-bodapati-940158258

---
