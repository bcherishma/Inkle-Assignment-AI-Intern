# Quick Start Guide

## Fix "Network Error" - Start the Backend!

The frontend is running but can't connect because the backend isn't started yet.

### Step 1: Start Backend (Terminal 1)

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
source ../venv/bin/activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Start the backend server
python run.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Step 2: Verify Backend is Running

Open a new terminal and test:
```bash
curl http://localhost:8000/health
```

Should return: `{"status":"healthy","service":"tourism-ai-system"}`

### Step 3: Frontend Should Now Work

The frontend at http://localhost:5173 should now be able to connect!

## Troubleshooting

### If you still get Network Error:

1. **Check backend is running**: Look for "Uvicorn running on http://0.0.0.0:8000" in terminal
2. **Check port 8000**: Make sure nothing else is using port 8000
3. **Check CORS**: Backend CORS is configured for localhost:5173
4. **Check browser console**: Open DevTools (F12) → Console tab for detailed errors

### Common Issues:

**Port already in use:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

**Import errors:**
```bash
# Make sure you're in backend/ directory when running
cd backend
python run.py
```

**Virtual environment not activated:**
```bash
# Activate venv first
source ../venv/bin/activate  # or source venv/bin/activate
```

