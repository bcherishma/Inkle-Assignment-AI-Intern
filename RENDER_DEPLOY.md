# 🚀 Render Deployment Guide

## Quick Start

### Step 1: Sign Up
1. Go to [render.com](https://render.com)
2. Sign up with GitHub

### Step 2: Create Backend Service

1. **Click "New +" → "Web Service"**
2. **Connect your GitHub repository**
3. **Configure:**
   - **Name**: `tourism-ai-backend`
   - **Environment**: `Docker`
   - **Dockerfile Path**: `Dockerfile` (or leave default)
   - **Docker Context**: `.` (root directory)
   - **Plan**: `Free` (or choose paid for always-on)

4. **Add Environment Variables:**
   Click "Advanced" → "Add Environment Variable" and add:
   ```
   NOMINATIM_BASE_URL=https://nominatim.openstreetmap.org/search
   OPEN_METEO_BASE_URL=https://api.open-meteo.com/v1/forecast
   OVERPASS_BASE_URL=https://overpass-api.de/api/interpreter
   USER_AGENT=TourismAI/1.0
   API_HOST=0.0.0.0
   LOG_LEVEL=INFO
   DATABASE_URL=sqlite+aiosqlite:///./tourism_ai.db
   ```

   **⚠️ IMPORTANT:** Do NOT set `PORT` - Render sets it automatically!

5. **Click "Create Web Service"**

### Step 3: Deploy Frontend

**You have 2 options:**

#### Option A: Deploy on Render (Same Platform)

1. **Click "New +" → "Web Service"**
2. **Connect same GitHub repository**
3. **Configure:**
   - **Name**: `tourism-ai-frontend`
   - **Root Directory**: `frontend`
   - **Environment**: `Node`
   - **Build Command**: `npm install`
   - **Start Command**: `npm run dev -- --host 0.0.0.0`
   - **Plan**: `Free`

4. **Add Environment Variable:**
   ```
   VITE_API_BASE_URL=https://your-backend-service.onrender.com
   ```
   (Replace with your actual backend URL)

5. **Click "Create Web Service"**

**Or use `render.yaml`** - Frontend is already configured!

#### Option B: Deploy on Vercel (Better Performance)

See [FRONTEND_DEPLOY.md](./FRONTEND_DEPLOY.md) for Vercel setup.

**Recommendation:** Use Render for both (simpler) OR Vercel for frontend (better performance).

1. **Click "New +" → "Web Service"**
2. **Connect same GitHub repository**
3. **Configure:**
   - **Name**: `tourism-ai-frontend`
   - **Root Directory**: `frontend`
   - **Environment**: `Node`
   - **Build Command**: `npm install`
   - **Start Command**: `npm run dev -- --host 0.0.0.0`
   - **Plan**: `Free`

4. **Add Environment Variable:**
   ```
   VITE_API_BASE_URL=https://your-backend-service.onrender.com
   ```
   (Replace with your actual backend URL)

5. **Click "Create Web Service"**

## Using render.yaml (Recommended)

Instead of manual setup, you can use the `render.yaml` file:

1. **Push `render.yaml` to your repository**
2. **In Render Dashboard:**
   - Click "New +" → "Blueprint"
   - Select your repository
   - Render will auto-detect `render.yaml`
   - Click "Apply"

This creates all services automatically!

## Environment Variables

### Backend Variables

| Variable | Value | Required |
|----------|-------|----------|
| `NOMINATIM_BASE_URL` | `https://nominatim.openstreetmap.org/search` | No |
| `OPEN_METEO_BASE_URL` | `https://api.open-meteo.com/v1/forecast` | No |
| `OVERPASS_BASE_URL` | `https://overpass-api.de/api/interpreter` | No |
| `USER_AGENT` | `TourismAI/1.0` | No |
| `API_HOST` | `0.0.0.0` | No |
| `LOG_LEVEL` | `INFO` | No |
| `DATABASE_URL` | `sqlite+aiosqlite:///./tourism_ai.db` | No |

**Note:** Render automatically sets `PORT` - don't set it manually!

### Frontend Variables

| Variable | Value | Required |
|----------|-------|----------|
| `VITE_API_BASE_URL` | Your backend Render URL | Yes |

## Access Your App

After deployment:
- **Backend**: `https://your-backend-service.onrender.com`
- **Frontend**: `https://your-frontend-service.onrender.com`
- **API Docs**: `https://your-backend-service.onrender.com/docs`

## Render Free Tier Notes

### ⚠️ Important Limitations:

1. **Spins Down After 15 Minutes Inactivity**
   - Free tier services sleep after 15 min of no requests
   - First request after sleep takes ~30-50 seconds to wake up
   - Subsequent requests are fast

2. **Solution:**
   - Use paid plan ($7/month) for always-on
   - Or use a service like [UptimeRobot](https://uptimerobot.com) to ping your service every 5 minutes (keeps it awake)

3. **Database:**
   - SQLite files are ephemeral (lost on restart)
   - For persistence, use Render PostgreSQL (free tier available)

## Troubleshooting

### Issue: Service Won't Start

**Check Logs:**
1. Render Dashboard → Your Service
2. Click "Logs" tab
3. Look for error messages

**Common Issues:**
- `ModuleNotFoundError` → Check requirements.txt
- `Port already in use` → Don't set PORT manually
- `Database error` → Check database path

### Issue: Health Check Failing

**Fix:**
- Make sure `/health` endpoint exists (it does)
- Health check should respond in < 5 seconds
- Check Render logs for timeout errors

### Issue: Frontend Can't Connect to Backend

**Fix:**
1. Get your backend URL from Render dashboard
2. Update frontend `VITE_API_BASE_URL` environment variable
3. Redeploy frontend

### Issue: Service Spins Down

**Free Tier Behavior:**
- Services sleep after 15 min inactivity
- First request wakes them up (takes ~30s)
- This is normal for free tier

**Solutions:**
1. Upgrade to paid plan ($7/month)
2. Use UptimeRobot to ping every 5 minutes
3. Accept the wake-up delay

## Quick Commands

### View Logs
- Render Dashboard → Service → Logs tab

### Restart Service
- Render Dashboard → Service → Manual Deploy → Clear build cache & deploy

### Update Environment Variables
- Render Dashboard → Service → Environment → Add/Edit variables

## Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Backend service created
- [ ] Environment variables set
- [ ] Backend deployed successfully
- [ ] Backend URL copied
- [ ] Frontend service created (optional)
- [ ] Frontend `VITE_API_BASE_URL` set to backend URL
- [ ] Frontend deployed
- [ ] Test health endpoint
- [ ] Test API endpoint

## Support

- **Render Docs**: https://render.com/docs
- **Render Status**: https://status.render.com
- **Render Support**: Via dashboard Help section

## Why Render?

✅ **Free tier available** (with limitations)  
✅ **Easy Docker deployment**  
✅ **Auto-deploy from GitHub**  
✅ **Free PostgreSQL** (if you need it later)  
✅ **Simple dashboard**  
✅ **Good documentation**  

Perfect for your project! 🚀

