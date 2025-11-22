# Quick Test Commands for VSCode

## Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 2: Start the Server
```bash
python -m app.main
```

The server will start at: `http://localhost:8000`

## Step 3: Test the API (in a new terminal)

### Test Health Endpoint
```bash
curl http://localhost:8000/health
```

### Test Example 1 (Places only)
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "I'\''m going to go to Bangalore, let'\''s plan my trip."}'
```

### Test Example 2 (Weather only)
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "I'\''m going to go to Bangalore, what is the temperature there"}'
```

### Test Example 3 (Both)
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "I'\''m going to go to Bangalore, what is the temperature there? And what are the places I can visit?"}'
```

### Test Error Handling (Invalid place)
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "I'\''m going to go to XyzInvalidPlace123, what is the temperature there?"}'
```

## Step 4: Test UI in Browser
Open browser and go to: `http://localhost:8000`

## Or Use Python Test Script
```bash
python test_api.py
```

## View API Documentation
Open browser: `http://localhost:8000/docs`

