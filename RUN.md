# How to Run the Application

## Quick Start Commands

### Backend (Terminal 1)

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment (from root directory)
source ../venv/bin/activate
# OR if venv is in backend:
# source venv/bin/activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Run the backend server
python run.py
```

**OR** using uvicorn directly:

```bash
# From backend directory
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend (Terminal 2)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (first time only)
npm install

# Run the frontend dev server
npm run dev
```

## Access Points

- **Frontend UI**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Troubleshooting

### If you get import errors:
Make sure you're running from the **root directory** (not from inside backend/), and the virtual environment is activated.

### If frontend can't connect to backend:
1. Make sure backend is running on port 8000
2. Check that CORS is configured correctly
3. Verify `VITE_API_BASE_URL` in `frontend/.env.local` (if you created one)

