# 🔧 Render Deployment Troubleshooting Guide

**Error**: `No flask entrypoint found`

This happens when Render can't find your Flask application entry point. Here's the complete fix.

---

## 🎯 Solution (Step-by-Step)

### **Step 1: Verify Files Exist**

Your project should have these files in the **root directory**:

- ✅ `wsgi.py` - Main entry point
- ✅ `app.py` - Flask application
- ✅ `requirements.txt` - Dependencies
- ✅ `Procfile` - Deployment config
- ✅ `runtime.txt` - Python version

Check they're there:
```bash
ls -la | grep -E "(wsgi|app|requirements|Procfile|runtime)"
```

Should show:
```
-rw-r--r--  app.py
-rw-r--r--  wsgi.py
-rw-r--r--  requirements.txt
-rw-r--r--  Procfile
-rw-r--r--  runtime.txt
```

### **Step 2: Check Procfile**

Your `Procfile` should contain **EXACTLY**:

```
web: gunicorn wsgi:app
```

NOT:
- ~~`web: gunicorn app:app`~~
- ~~`web: python app.py`~~
- ~~`web: flask run`~~

### **Step 3: Check wsgi.py Content**

Your `wsgi.py` should be:

```python
"""WSGI entry point for Render deployment."""

from app import app

__all__ = ['app']

if __name__ == "__main__":
    app.run()
```

### **Step 4: Verify app.py Structure**

Your `app.py` should have `app` defined at module level. Check it has:

```python
# Somewhere in app.py (not inside a function):
app = Flask(__name__)

# And later:
@app.route("/predict", methods=["POST"])
def predict():
    # ... prediction logic
```

### **Step 5: Check requirements.txt**

Must include:

```
Flask>=2.0
flask-cors>=4.0
gunicorn>=21.0
numpy>=1.23
pillow>=9.0
tensorflow>=2.12
```

### **Step 6: Set Render Configuration Correctly**

In **Render Dashboard** for your service:

#### Build Command:
```
pip install --upgrade pip && pip install -r requirements.txt
```

#### Start Command:
```
gunicorn wsgi:app
```

⚠️ **NOT** `gunicorn app:app` ⚠️

### **Step 7: Click "Clear Build Cache" and Redeploy**

1. In Render dashboard, click your service
2. Go to **Settings**
3. Scroll down and click **"Clear Build Cache"**
4. Click **"Manual Deploy"** → **"Deploy Latest Commit"**
5. Wait 5-15 minutes

---

## ✅ If It Still Fails

### Check Render Logs

In Render dashboard:
1. Click your service
2. Go to **"Logs"** tab
3. Look for actual Python error messages

Common errors:

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError: No module named 'app'` | Check wsgi.py imports correctly |
| `AttributeError: cannot import name 'app'` | Check app.py defines `app = Flask(...)` |
| `No module named 'tensorflow'` | Add tensorflow to requirements.txt |
| `ImportError: cannot import flask_cors` | Add flask-cors to requirements.txt |

### Test Locally First

Before deploying, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Test wsgi import
python -c "from wsgi import app; print('✅ Import successful')"

# Test with gunicorn
gunicorn wsgi:app
```

Should see:
```
[2026-03-20 ...] [INFO] Starting gunicorn
[2026-03-20 ...] [INFO] Listening at: http://0.0.0.0:8000
```

### Verify GitHub Has Latest Code

1. Check GitHub repo has these files:
```
https://github.com/Aryan22nov/minor_proj/blob/main/wsgi.py
https://github.com/Aryan22nov/minor_proj/blob/main/Procfile
https://github.com/Aryan22nov/minor_proj/blob/main/runtime.txt
```

2. If not, push latest:
```bash
git add .
git commit -m "Fix Render deployment config"
git push origin main
```

3. Then in Render, click **"Manual Deploy"**

---

## 🎯 Exact File Checklist

Before you deploy, copy-paste these exact contents:

### `Procfile` (1 line exactly):
```
web: gunicorn wsgi:app
```

### `runtime.txt` (1 line):
```
python-3.11.5
```

### `wsgi.py`:
```python
"""WSGI entry point for Render deployment."""

from app import app

__all__ = ['app']

if __name__ == "__main__":
    app.run()
```

### `requirements.txt` (minimum):
```
Flask>=2.0
flask-cors>=4.0
gunicorn>=21.0
numpy>=1.23
pillow>=9.0
tensorflow>=2.12
```

---

## 🚀 After Fix

Once deployment succeeds, you should see:

```
Build started
...
[INFO] Started gunicorn [PID 1]
...
Listening on 0.0.0.0:10000 (Press CTRL+C to quit)
```

And your service should show ✅ **"Live"** status.

---

## 💡 Pro Tips

1. **Click "Clear Build Cache"** before redeploying - Render sometimes caches old builds
2. **Check Render Logs first** when something fails - the error message is there
3. **Test locally first** before pushing to Render
4. **Use `runtime.txt`** to lock Python version (avoids compatibility issues)

---

## 🆘 Still Not Working?

Send me:
1. Screenshot of Render logs (click Logs tab)
2. Run locally: `python -c "from wsgi import app; print(app)"`
3. Confirm GitHub has wsgi.py in root

We'll fix it immediately! 💙
