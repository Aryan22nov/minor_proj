# 🚀 Production Stack - What's Used

Complete breakdown of all **production technologies** and services for your AI Skin Disease Detector.

---

## 🏗️ Architecture Overview

```
┌────────────────────────────────────────────────────────────────┐
│                     USERS                                      │
│              (Accessing your app)                              │
└────────┬────────────────────────────────┬─────────────────────┘
         │                                │
         │ HTTPS                          │ HTTPS
         │                                │
┌────────▼──────────────────┐    ┌───────▼──────────────────────┐
│   VERCEL (Frontend)       │    │   RENDER (Backend)           │
│                           │    │                              │
│  • React 18              │    │  • Flask (Python)            │
│  • Vite Build            │    │  • TensorFlow (DL)           │
│  • Hosted at:            │    │  • Hosted at:                │
│  https://app.vercel.app  │───→│ https://api.onrender.com     │
│                           │    │                              │
│  Files: frontend/dist/   │    │  Files: app.py, wsgi.py      │
└─────────────────────────┘    └──────────────────────────────┘
```

---

## 📋 Complete Production Stack

### **1. FRONTEND - Deployed on Vercel**

#### What:
- **Framework**: React 18
- **Build Tool**: Vite
- **Language**: JavaScript/JSX
- **Package Manager**: npm

#### Services:
```
Platform: Vercel (vercel.com)
URL: https://your-app-name.vercel.app
Region: Auto-selected by Vercel (CDN worldwide)
Build Time: ~3-5 minutes
```

#### Key Files:
```
frontend/
├── src/
│   ├── App.jsx              (Main React component)
│   ├── main.jsx             (Entry point)
│   ├── styles.css           (UI Styling)
│   └── config.js            (API configuration)
├── package.json             (Dependencies)
├── vite.config.js           (Build config)
├── vercel.json              (Vercel deployment config)
└── dist/                    (Built output - uploaded to Vercel)
```

#### Environment Variables (Set in Vercel):
```
VITE_API_URL = https://your-backend-url.onrender.com
```

#### Dependencies:
```json
{
  "react": "^18.3.1",
  "react-dom": "^18.3.1",
  "recharts": "^2.10.0",
  "jspdf": "^2.5.1",
  "html2canvas": "^1.4.1"
}
```

---

### **2. BACKEND - Deployed on Render**

#### What:
- **Framework**: Flask (Python)
- **ML Library**: TensorFlow/Keras
- **Server**: Gunicorn (WSGI)
- **Language**: Python 3.11

#### Services:
```
Platform: Render.com (render.com)
URL: https://your-api-name.onrender.com
Region: Configurable
Build Time: ~5-15 minutes
```

#### Key Files:
```
.
├── app.py                   (Flask application)
├── wsgi.py                  (WSGI entry point for Gunicorn)
├── requirements.txt         (Python dependencies)
├── Procfile                 (Deployment config: gunicorn wsgi:app)
├── runtime.txt              (Python version: 3.11.5)
├── render.yaml              (Render-specific config)
└── skin_model.h5            (Trained TensorFlow model - optional)
```

#### API Endpoints:
```
POST /predict
  - Accepts: image file
  - Returns: {disease, confidence, scores}

GET /
  - Returns: Frontend HTML/React app
```

#### Dependencies:
```
Flask>=2.0
flask-cors>=4.0
numpy>=1.23
pillow>=9.0
tensorflow>=2.12
gunicorn>=21.0
```

---

## 🔌 How They Connect

### **Frontend → Backend Communication**

#### In Development (localhost):
```
Frontend: http://localhost:5173
Backend:  http://localhost:5000

API Call: fetch('http://127.0.0.1:5000/predict', {
  method: 'POST',
  body: formData
})
```

#### In Production (Deployed):
```
Frontend: https://your-app.vercel.app
Backend:  https://your-api.onrender.com

API Call: fetch('https://your-api.onrender.com/predict', {
  method: 'POST',
  body: formData
})
```

#### Configuration Logic (`frontend/src/config.js`):
```javascript
const isDevelopment = import.meta.env.DEV;

if (isDevelopment) {
  API_URL = 'http://127.0.0.1:5000'  // Local
} else {
  API_URL = process.env.VITE_API_URL  // Production
}
```

---

## 🗂️ Deployment Files Reference

### **Root Directory Files**

| File | Purpose | Platform |
|------|---------|----------|
| `Procfile` | Tells Render how to start | Render |
| `runtime.txt` | Python version | Render |
| `requirements.txt` | Python packages | Render |
| `wsgi.py` | WSGI entry point | Render |
| `render.yaml` | Render config (alternative) | Render |
| `app.py` | Flask application | Render |

### **Frontend Directory**

| File | Purpose | Platform |
|------|---------|----------|
| `frontend/vercel.json` | Vercel config | Vercel |
| `frontend/.env.example` | Template variables | Vercel |
| `frontend/.env.local` | Local development | Vercel |
| `frontend/vite.config.js` | Build config | Vercel |
| `frontend/package.json` | Dependencies | Vercel |
| `frontend/src/config.js` | API configuration | Vercel |

---

## 📊 Production Workflow

### **User Flow**

```
1. User opens: https://your-app.vercel.app
2. Browser loads React app from Vercel CDN
3. React app initializes with frontend/src/config.js
4. User selects image
5. React makes API call to: https://your-api.onrender.com/predict
6. Backend (Flask) receives image
7. TensorFlow model processes image
8. Backend returns prediction JSON
9. React displays result with confidence score
10. User can download PDF report
11. Prediction saved to browser localStorage
```

### **Deployment Workflow**

```
GitHub (main branch)
        ↓
git push origin main
        ↓
        ├─→ Vercel: Auto-detects changes
        │           Builds: npm run build
        │           Deploys: frontend/dist
        │           Live in: 3-5 minutes ✅
        │
        └─→ Render: Auto-detects changes
                    Builds: pip install -r requirements.txt
                    Deploys: gunicorn wsgi:app
                    Live in: 5-15 minutes ✅
```

---

## 🔐 Security & Configuration

### **CORS Configuration** (Backend)
```python
# app.py
CORS(app, resources={
    r"/predict": {"origins": "*"},
    r"/": {"origins": "*"}
})
```

### **Environment Variables**

**Vercel (Frontend)**:
```
VITE_API_URL = https://your-api-name.onrender.com
```

**Render (Backend)**:
```
FLASK_DEBUG = false
PORT = 5000 (auto-set by Render)
```

### **HTTPS**
- ✅ Vercel: Auto HTTPS on `*.vercel.app`
- ✅ Render: Auto HTTPS on `*.onrender.com`
- ✅ All traffic encrypted end-to-end

---

## 💰 Cost Breakdown

| Service | Plan | Cost | Limits |
|---------|------|------|--------|
| **Vercel** | Free | $0/month | 100GB bandwidth/month |
| **Render** | Free | $0/month | Sleeps after 15min idle |
| **GitHub** | Free | $0/month | Public repo |
| **Total** | Free Tier | **$0/month** | Sufficient for learning/portfolio |

⚠️ **Note**: Free tier Render instance sleeps after 15 minutes of inactivity (cold start = 30-60 sec first request)

---

## 🗄️ Data Storage

### **Frontend Data** (Browser)
```javascript
// localStorage
{
  predictions: [...],
  darkMode: true,
  preferences: {}
}
```

### **Backend Process**
- No database (stateless)
- Model loaded into memory
- Each prediction is independent
- ✅ Perfect for serverless/containers

---

## 🚀 Scaling Architecture

If you need to scale from free tier:

### **Scale Frontend** (Vercel)
```
Free → Pro: $20/month
- Increased bandwidth
- Priority support
- Advanced analytics
```

### **Scale Backend** (Render)
```
Free (sleepy) → Standard: $7-15/month
- Always running (no cold starts)
- More memory
- Better performance
```

### **Add Database** (Optional)
```
PostgreSQL @ Render: $7-15/month
Useful if you want to:
- Store user predictions
- Track analytics
- User authentication
```

---

## 📊 Production Load Estimation

### **Expected Performance**

| Metric | Value |
|--------|-------|
| Frontend Load Time | 2-3 seconds (Vercel CDN) |
| API Response | 1-2 seconds (prediction) |
| Total E2E Time | 3-5 seconds |
| Concurrent Users | 100+ (Vercel) / 5+ (Render free) |
| Monthly Requests | 1000+ (free tier sufficient) |

### **Bottlenecks**
- **Cold Start** (Render free): First request after 15min = 30-60 sec
- **Model Loading**: TensorFlow takes ~2-3 sec on first request
- **Image Processing**: Depends on image size (up to 10MB handled)

---

## 🔧 Monitoring & Debugging

### **Vercel Dashboard**
```
https://vercel.com/dashboard
- View deployments
- Check analytics
- View function logs
- Set environment variables
```

### **Render Dashboard**
```
https://render.com/dashboard
- View service status
- Check logs in real-time
- Manually redeploy
- Clear build cache
```

### **GitHub**
```
https://github.com/Aryan22nov/minor_proj
- Monitor commits
- Enable Actions for CI/CD
- Release versions
```

---

## 📝 Deployment Checklist

### **Before Going Live**
- [ ] All tests pass locally
- [ ] No hardcoded URLs (use env vars)
- [ ] Dependencies in requirements.txt
- [ ] .env files in .gitignore
- [ ] Code pushed to GitHub main branch

### **During Deployment**
- [ ] Monitor Render build logs
- [ ] Monitor Vercel build logs
- [ ] Check Render app is "Live" ✅
- [ ] Check Vercel deployment is "Ready" ✅

### **After Deployment**
- [ ] Test frontend URL in browser
- [ ] Upload test image
- [ ] Verify prediction returns
- [ ] Check browser console for errors
- [ ] Test in Incognito mode (no cache)

---

## 🎯 Production URLs Template

Replace with your actual URLs:

```
Frontend: https://your-app-name.vercel.app
Backend:  https://your-api-name.onrender.com

API Endpoint: https://your-api-name.onrender.com/predict
```

---

## 💙 Summary

| Component | Technology | Deployment | Cost |
|-----------|-----------|-----------|------|
| Frontend | React + Vite | **Vercel** | Free |
| Backend | Flask + TensorFlow | **Render** | Free |
| Version Control | Git | **GitHub** | Free |
| ML Model | TensorFlow/Keras | **Render** | Included |
| **Total** | | | **$0** |

**Your production app is enterprise-ready!** 🚀

All components auto-deploy from GitHub. Push once → live everywhere in 5-15 minutes.

---

## 📚 Additional Resources

- [Vercel Docs](https://vercel.com/docs)
- [Render Docs](https://render.com/docs)
- [Flask Deployment](https://flask.palletsprojects.com/deployment/)
- [React Production Build](https://react.dev/learn/start-a-new-react-project)

---

**Questions?** Check the deployment guides in your repo! 💙
