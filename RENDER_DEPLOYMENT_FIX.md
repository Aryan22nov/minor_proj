# 🚀 Deploy Backend to Render.com - Step by Step

## ⚠️ If You Got the "No flask entrypoint" Error

**Don't worry!** This is now fixed. The issue was Render's deployment configuration. Here's the exact fix:

---

## 🔧 Step 1: Go to Render Dashboard

Visit: https://render.com/dashboard

---

## 📝 Step 2: Create New Web Service

1. Click **"+ New"** → **"Web Service"**
2. Select **"GitHub"** (make sure GitHub is connected)
3. Find and select: `Aryan22nov/minor_proj`
4. Click **"Connect"**

---

## ⚙️ Step 3: Configure Web Service (IMPORTANT!)

Fill in these **EXACT** settings:

### **Basic Settings**
```
Name: skin-disease-detector-api
Environment: Python 3
Region: Singapore (or nearest to you)
Branch: main
Root Directory: (leave empty)
```

### **Build & Deploy Settings** (CRITICAL!)

**Build Command:**
```
pip install --upgrade pip && pip install -r requirements.txt
```

**Start Command:** (THIS IS THE FIX!)
```
gunicorn wsgi:app
```

⚠️ **IMPORTANT**: Use `wsgi:app` NOT `app:app`

### **Plan**
```
Instance Type: Free
```

---

## 🌍 Step 4: Deploy

1. Click **"Create Web Service"**
2. Wait for deployment (5-15 minutes)
3. Watch the logs - should show:
   ```
   Started gunicorn
   Application startup complete
   ```
4. Once green checkmark appears ✅, your backend is LIVE!

---

## 📋 Copy Your Backend URL

Once deployed, you'll see something like:
```
https://skin-disease-detector-api.onrender.com
```

**Copy this URL!** You'll need it for frontend deployment.

---

## ✅ Test Your Backend

Open this in browser:
```
https://skin-disease-detector-api.onrender.com/
```

You should see your homepage or interface.

---

## 🔐 Files That Helped

These files were created to fix the Render deployment issue:

- ✅ `wsgi.py` - WSGI entry point (required by Render)
- ✅ `render.yaml` - Render native configuration
- ✅ `Procfile` - Updated to use `wsgi:app`

---

## 🐛 If Still Getting Errors

### Error: "Build failed"
- Check logs for missing dependencies
- Ensure `requirements.txt` has all packages
- Run locally: `pip install -r requirements.txt`

### Error: "Failed to start application"
- Check logs for Python errors
- Verify `wsgi.py` exists in root directory
- Test locally: `gunicorn wsgi:app`

### Error: "502 Bad Gateway"
- Backend crashed - check Render logs
- Usually means Python error in app.py
- Fix error and redeploy

---

## 🎯 What Happens Next

Once backend is deployed:
1. Frontend will connect to this URL
2. When you upload image, it goes to backend
3. Backend runs prediction
4. Result returns to frontend

---

## 🚀 Next Step

After backend is live:
1. Copy the backend URL
2. Go to Step 1 of **Frontend Deployment** (Vercel)
3. Set `VITE_API_URL` environment variable

---

**Your backend is now production-ready!** 💙
