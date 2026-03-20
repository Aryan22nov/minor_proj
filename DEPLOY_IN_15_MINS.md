# 🚀 Deploy in 15 Minutes!

Quick deployment checklist for getting your AI Skin Disease Detector live.

---

## ✅ Pre-Deployment Checklist

- [ ] Code is pushed to GitHub
- [ ] All files are committed (no uncommitted changes)
- [ ] `requirements.txt` has all dependencies
- [ ] `frontend/package.json` has all packages
- [ ] You have Vercel + Render.com accounts (free tier)

---

## 📤 Part 1: Deploy Backend (Render)

### 1. Go to https://render.com (5 minutes)

### 2. Create Web Service
- Click "New +" → "Web Service"
- Select your GitHub repo
- Click "Connect"

### 3. Configure (use these exact values)

```
Name:           skin-disease-detector-api
Environment:    Python 3
Region:         Choose nearest
Build Command:  pip install -r requirements.txt
Start Command:  gunicorn app:app
Plan:           Free
```

### 4. Deploy
- Click "Create Web Service"
- Wait for green checkmark (5-10 min)
- Copy your backend URL:
  ```
  https://skin-disease-detector-api.onrender.com
  ```

✅ **Backend is LIVE!**

---

## 🎨 Part 2: Deploy Frontend (Vercel)

### 1. Go to https://vercel.com (5 minutes)

### 2. Import Project
- Click "Add New..." → "Project"
- Select your GitHub repo
- Click "Import"

### 3. Configure

**Build Settings** (Vercel auto-detects, confirm these):
```
Framework:        Vite
Build Command:    npm run build --prefix frontend
Output Directory: frontend/dist
Install Command:  npm install --prefix frontend
```

**Environment Variables:**
1. Click "Environment Variables"
2. Add new variable:
   ```
   Name:  VITE_API_URL
   Value: https://skin-disease-detector-api.onrender.com
   ```
   (Use YOUR backend URL from Part 1)
3. Click "Save"

### 4. Deploy
- Click "Deploy"
- Wait for green checkmark (3-5 min)
- Your frontend URL will be shown:
  ```
  https://your-project-name-123.vercel.app
  ```

✅ **Frontend is LIVE!**

---

## 🧪 Test Your Deployment

### 1. Test Backend
Open: `https://skin-disease-detector-api.onrender.com`

You should see your interface or a homepage.

### 2. Test Frontend
Open: `https://your-project-name-123.vercel.app`

You should see the full app interface.

### 3. Test Upload
1. Click "Upload Image" or use camera
2. Select an image
3. Click "Predict"
4. **You should see prediction result!** ✅

**If it works, you're done!** 🎉

---

## ⚠️ If Something Goes Wrong

### "Cannot connect to backend"
```
✓ Check VITE_API_URL in Vercel settings
✓ Make sure backend URL is correct
✓ Redeploy frontend after changing URL
```

### "Error uploading image"
```
✓ Use JPG or PNG format
✓ Make sure file size < 10MB
✓ Check browser console (F12) for errors
```

### Backend shows 502 error
```
✓ Check Render logs: Dashboard → Logs tab
✓ Verify app.py has no syntax errors
✓ Ensure all packages are in requirements.txt
```

### Frontend shows 404
```
✓ Vercel needs "frontend/dist" folder
✓ Run: npm run build --prefix frontend
✓ Commit and push to GitHub
```

---

## 📊 Your Live Project

```
🌍 Frontend:  https://your-project-name-123.vercel.app
🔗 Backend:   https://skin-disease-detector-api.onrender.com
📱 API:       https://skin-disease-detector-api.onrender.com/predict
```

**Share this with interviewers/clients!**

---

## 🔄 Making Changes (After Deployment)

Now anytime you push to GitHub:
1. Vercel automatically redeploys frontend ✨
2. Render automatically redeploys backend ✨

**No manual steps needed!**

```bash
# Just commit and push
git add .
git commit -m "Your changes"
git push origin main
```

Wait ~ 5-10 seconds, refresh the site. ✅

---

## 💡 Pro Tips

### Enable Automatic Deployments
- Vercel + Render both support GitHub auto-deploy
- Enable in dashboard settings
- Zero-downtime deployments

### Set Up Custom Domain (Optional)
- Vercel: Go to Project Settings → Domains
- Costs ~$12/year

### Monitor Performance
- **Vercel**: Dashboard → Analytics
- **Render**: Dashboard → Usage

### Enable Alerts
- Set up email alerts for deploy failures
- Available in both Render & Vercel settings

---

## 🎓 You're Now a Full-Stack Developer! 🚀

Your AI app is **live on the internet** ✨

Next steps:
- [ ] Add to portfolio
- [ ] Share the live link
- [ ] Use in interviews/demos
- [ ] Collect user feedback
- [ ] Iterate and improve

---

## ❓ Need Help?

1. Check [DEPLOYMENT_GUIDE_PRODUCTION.md](./DEPLOYMENT_GUIDE_PRODUCTION.md) for detailed guide
2. View error logs in Render/Vercel dashboards
3. Check console errors (F12 → Console tab)
4. Review [README_PRODUCTION.md](./README_PRODUCTION.md)

---

**🎉 Congratulations! Your project is live!**

Made with 💙
