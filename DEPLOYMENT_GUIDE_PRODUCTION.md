# 🚀 Deployment Guide: Vercel + Render

This guide walks you through deploying the **AI Skin Disease Detector** to production.

**Architecture:**
- **Frontend**: React app → Vercel
- **Backend**: Flask API → Render.com

---

## 📋 Prerequisites

Before deploying, ensure you have:

- [ ] GitHub account
- [ ] Vercel account (free tier available)
- [ ] Render.com account (free tier available)
- [ ] Your GitHub repository with code pushed

---

## 🔧 Part 1: Prepare Backend for Render

### Step 1: Create `Procfile` (for Render)

In project root, create `Procfile`:

```
web: python app.py
```

### Step 2: Update `requirements.txt`

Ensure backend dependencies are listed:

```
Flask>=2.0
flask-cors>=4.0
numpy>=1.23
pillow>=9.0
tensorflow>=2.12
gunicorn>=21.0
```

**Note**: `flask-cors` is already added. `gunicorn` is for production serving.

### Step 3: Update `app.py`

Ensure app listens on environment variables:

```python
if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=debug)
```

✅ Already configured!

---

## 📤 Part 2: Deploy Backend to Render

### Step 1: Go to [render.com](https://render.com)

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Select your repository

### Step 2: Configure Web Service

Fill in these fields:

| Field | Value |
|-------|-------|
| **Name** | `skin-disease-detector-api` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |
| **Instance Type** | `Free` (or upgrade later) |

### Step 3: Deploy

Click **"Deploy"** and wait (~5-10 minutes)

Once deployed, you'll get a URL like:
```
https://skin-disease-detector-api.onrender.com
```

**⚠️ IMPORTANT**: Copy this URL! You'll need it for frontend.

---

## 🎨 Part 3: Deploy Frontend to Vercel

### Step 1: Go to [vercel.com](https://vercel.com)

1. Click **"Add New..."** → **"Project"**
2. Import your GitHub repository
3. Select the root directory (not `/frontend`)

### Step 2: Configure Build Settings

Vercel should **auto-detect**, but confirm:

| Field | Value |
|-------|-------|
| **Framework Preset** | `Vite` |
| **Build Command** | `npm run build --prefix frontend` |
| **Output Directory** | `frontend/dist` |
| **Install Command** | `npm install --prefix frontend` |

### Step 3: Set Environment Variables

1. Go to **"Settings"** → **"Environment Variables"**
2. Add variable:

```
VITE_API_URL = https://skin-disease-detector-api.onrender.com
```

(Replace with your actual Render backend URL)

3. Click **"Save"** and redeploy

### Step 4: Deploy

Click **"Deploy"** and wait (~3-5 minutes)

Your frontend will be live at:
```
https://your-project-name.vercel.app
```

---

## ✅ Testing the Deployment

### Test Backend API

Open in browser:
```
https://skin-disease-detector-api.onrender.com/
```

You should see the interface (or JSON response).

### Test Frontend

Open:
```
https://your-project-name.vercel.app
```

### Test Full Flow

1. Upload an image
2. Click "Predict"
3. You should see prediction result ✅

If it fails, check browser console (F12) for error messages.

---

## 🐛 Troubleshooting

### Issue: "Cannot connect to backend"

**Solution**: 
1. Check your `VITE_API_URL` environment variable in Vercel
2. Verify Render backend is running
3. Check browser console (F12) for exact error

### Issue: "CORS error"

**Solution**: 
Backend already has CORS configured. If error persists:
1. Check Flask has `from flask_cors import CORS` 
2. Verify `CORS(app)` is called

### Issue: "502 Bad Gateway" on backend

**Solution**:
1. Check Render logs for errors
2. Ensure `requirements.txt` has all dependencies
3. Verify `app.py` has no syntax errors

### Issue: Build fails on Vercel

**Solution**:
1. Check "Deployments" tab for error logs
2. Ensure `frontend/` folder structure is correct
3. Run locally: `npm run build --prefix frontend`

---

## 🔄 Continuous Deployment

After initial setup:

1. **Make code changes** on your machine
2. **Git push** to GitHub
3. **Automatic deploy** happens on both Vercel & Render ✨

No manual steps needed!

---

## 📊 Useful Commands

### Test frontend build locally

```bash
cd frontend
npm run build
npm run preview
```

### Test backend locally

```bash
python app.py
```

Visit `http://127.0.0.1:5000`

### View Render logs

On Render dashboard → Click your service → "Logs" tab

### View Vercel logs

On Vercel dashboard → Click your project → "Deployments" tab

---

## 💾 Environment Variables Checklist

**Vercel (Frontend):**
- [ ] `VITE_API_URL` = `https://your-backend.onrender.com`

**Render (Backend):**
- [ ] `PORT` = (auto-set, no need to configure)
- [ ] `FLASK_DEBUG` = `false` (default)

---

## 🎉 You're Live!

Your AI Skin Disease Detector is now deployed! 🚀

**Share your project:**
- Frontend: `https://your-project-name.vercel.app`
- Backend API: `https://skin-disease-detector-api.onrender.com/predict`

---

## 📝 Next Steps (Optional)

- [ ] Add custom domain to Vercel ($12/year)
- [ ] Set up GitHub Actions for advanced CI/CD
- [ ] Add monitoring + error tracking (Sentry)
- [ ] Scale backend to paid tier if needed
- [ ] Create professional README + screenshots

---

**Questions?** Check Vercel & Render documentation or reach out! 💙
