# 📋 Production Deployment Verification Checklist

Use this checklist to ensure your project is **fully production-ready** before deploying.

---

## ✅ Backend (Flask) Verification

### Code Quality
- [ ] `app.py` has CORS enabled (`from flask_cors import CORS` + `CORS(app)`)
- [ ] App listens on `0.0.0.0` and environment PORT
- [ ] No hardcoded localhost URLs (use environment variables)
- [ ] Error handling for all API endpoints
- [ ] No debug prints or sensitive logs

### Dependencies
- [ ] `requirements.txt` includes:
  - [ ] Flask
  - [ ] flask-cors
  - [ ] tensorflow (or mock it if not needed)
  - [ ] pillow
  - [ ] numpy
  - [ ] gunicorn
- [ ] No version conflicts in requirements
- [ ] Run `pip install -r requirements.txt` successfully locally

### Deployment Config
- [ ] `Procfile` exists with: `web: gunicorn app:app`
- [ ] All environment variables documented in comments
- [ ] `.env.example` created with template values
- [ ] No `.env` file committed to git (only `.env.example`)

### Testing
- [ ] Backend runs locally: `python app.py`
- [ ] API responds to POST `/predict` with image
- [ ] CORS headers present in response
- [ ] Error handling works (invalid image, missing file, etc)

---

## ✅ Frontend (React/Vite) Verification

### Configuration
- [ ] `frontend/src/config.js` exists with API URL logic
- [ ] API calls use `PREDICT_ENDPOINT` from config
- [ ] Environment variables used: `VITE_API_URL`
- [ ] `.env.example` has `VITE_API_URL=http://127.0.0.1:5000`
- [ ] `.env.local` for local development (NOT committed)

### Build
- [ ] `npm run build --prefix frontend` succeeds
- [ ] No build warnings or errors
- [ ] `frontend/dist/` folder created with content
- [ ] `frontend/dist/index.html` exists
- [ ] All assets bundled correctly

### Code Quality
- [ ] No hardcoded backend URLs (use config.js)
- [ ] No console.log or debug code left
- [ ] Error messages user-friendly
- [ ] Loading states implemented
- [ ] No sensitive data in comments

### Testing
- [ ] `npm run dev --prefix frontend` works locally
- [ ] Can upload images and get predictions
- [ ] Works with both localhost AND deployed backend
- [ ] Dark mode works
- [ ] Mobile responsive

---

## ✅ GitHub & Version Control

- [ ] Code pushed to GitHub main branch
- [ ] All commits have clear messages
- [ ] No uncommitted changes (`git status` = clean)
- [ ] `.gitignore` excludes:
  - [ ] `.env` files
  - [ ] `node_modules/`
  - [ ] `__pycache__/`
  - [ ] `*.pyc`
  - [ ] `.venv/`
  - [ ] `*.h5` model files

---

## ✅ Vercel (Frontend) Setup

- [ ] Created Vercel account
- [ ] Connected GitHub repo to Vercel
- [ ] Build settings configured:
  - [ ] Build Command: `npm run build --prefix frontend`
  - [ ] Output Directory: `frontend/dist`
  - [ ] Install Command: `npm install --prefix frontend`
- [ ] Environment Variables added:
  - [ ] `VITE_API_URL` = your Render backend URL
- [ ] `frontend/vercel.json` created with rewrites

---

## ✅ Render (Backend) Setup

- [ ] Created Render account
- [ ] Connected GitHub repo
- [ ] Web Service configured:
  - [ ] Build Command: `pip install -r requirements.txt`
  - [ ] Start Command: `gunicorn app:app`
  - [ ] Region: Selected (nearest preferable)
  - [ ] Plan: Free (or paid if needed)
- [ ] Deployment successful (green checkmark)
- [ ] Backend URL copied: `https://xxx.onrender.com`

---

## ✅ Integration Testing

### In Vercel Dashboard
- [ ] Set `VITE_API_URL` environment variable
- [ ] Trigger redeploy
- [ ] Wait for deployment to complete

### Test Frontend at Vercel URL
- [ ] Can access the app
- [ ] Upload/Camera buttons work
- [ ] Can select image
- [ ] Prediction works (shows result)
- [ ] History saves predictions
- [ ] Dark mode toggles
- [ ] PDF download works

### Test API Directly
```bash
# Should return prediction
curl -X POST https://your-backend.onrender.com/predict \
  -F "image=@test-image.jpg"
```

### Check Browser Console (F12)
- [ ] No CORS errors
- [ ] No 404 errors
- [ ] API URL is correct
- [ ] Network tab shows successful POST to backend

---

## ✅ Security & Performance

### Security
- [ ] No sensitive data in frontend code
- [ ] No API keys/secrets in repository
- [ ] CORS properly configured (not overly permissive)
- [ ] HTTPS enforced (automatic on Vercel/Render)
- [ ] Environment variables not logged

### Performance
- [ ] Frontend loads in < 3 seconds
- [ ] Prediction returns in < 3 seconds
- [ ] No console warnings
- [ ] Images optimized (< 50KB where possible)
- [ ] CSS/JS minified in production build

---

## ✅ Documentation

- [ ] `DEPLOY_IN_15_MINS.md` created (quick reference)
- [ ] `DEPLOYMENT_GUIDE_PRODUCTION.md` created (detailed)
- [ ] `README_PRODUCTION.md` created (overview)
- [ ] API documentation in comments
- [ ] Environment variables documented
- [ ] Deployment steps clearly explained

---

## ✅ Final Verification

### Live App Test
- [ ] Frontend URL works: `https://your-app.vercel.app`
- [ ] Backend URL works: `https://your-api.onrender.com`
- [ ] Can upload image from frontend
- [ ] Predication works end-to-end
- [ ] Results display correctly
- [ ] No errors in console or logs

### Share Proof
- [ ] Take screenshot of live app
- [ ] Document the URLs
- [ ] Test URL in Incognito mode (no cache)
- [ ] Verify from different browser

---

## 🎯 Deployment Summary

### URLs to Share
```
Frontend:  https://your-app-name.vercel.app
Backend:   https://your-api-name.onrender.com
```

### Key Deployments
| Component | Platform | Status |
|-----------|----------|--------|
| Frontend | Vercel | ✅ Deployed |
| Backend | Render | ✅ Deployed |
| Database | - | N/A |

---

## 📝 Post-Deployment

### After Go-Live
- [ ] Monitor analytics (Vercel dashboard)
- [ ] Check error logs regularly (Render dashboard)
- [ ] Collect user feedback
- [ ] Plan improvements

### Ongoing Maintenance
- [ ] Keep dependencies updated
- [ ] Monitor API response times
- [ ] Backup if user data is stored
- [ ] Update documentation

---

## 🚨 Emergency Procedures

If something breaks:

1. **Check Render logs first**
   - Dashboard → Logs tab
   - Look for Python errors

2. **Check Vercel logs second**
   - Go to Deployments tab
   - Check build logs for errors

3. **Verify environment variables**
   - Backend: Render dashboard settings
   - Frontend: Vercel dashboard settings

4. **Simple fix: Redeploy**
   - Git push to main branch
   - Both services auto-redeploy

---

## ✨ Congratulations!

If you've checked all boxes, your **production-ready AI app is LIVE!** 🚀

**Share this achievement:**
- Portfolio
- GitHub PIN
- LinkedIn
- Job interviews
- Resume

---

**Last Updated**: March 2026  
**Status**: ✅ Production Ready
