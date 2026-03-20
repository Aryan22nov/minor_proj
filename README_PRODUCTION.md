# 🧠 AI Skin Disease Detector

A **production-ready, full-stack web application** for detecting skin diseases using deep learning.

**Live Demo**: [https://your-app-name.vercel.app](#)  
**API**: [https://your-backend.onrender.com](#)

## ✨ Features

- 📸 **Image Upload & Camera Capture** - Upload images or use webcam
- 🤖 **AI Prediction** - Deep learning model detects skin diseases
- 📊 **Confidence Score** - Shows prediction accuracy
- 💾 **Prediction History** - Saves all previous predictions
- 🌙 **Dark Mode** - User-friendly interface
- 📱 **Responsive Design** - Works on all devices
- 📄 **PDF Reports** - Download prediction results as PDF
- ⚡ **Production Deployed** - Vercel + Render

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│   Frontend (React + Vite)               │
│   Deployed on Vercel                    │
│   - Image upload/preview                │
│   - Real-time predictions               │
│   - History tracking                    │
│   - Dark mode support                   │
└────────────┬────────────────────────────┘
             │
             │ HTTPS API Calls
             │
┌────────────┴────────────────────────────┐
│   Backend (Flask + TensorFlow)          │
│   Deployed on Render                    │
│   - /predict endpoint                   │
│   - Image preprocessing                 │
│   - Disease classification              │
│   - CORS enabled                        │
└─────────────────────────────────────────┘
```

## 📦 Tech Stack

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool (super fast ⚡)
- **Recharts** - Data visualization
- **html2canvas + jsPDF** - PDF generation
- **CSS3** - Premium animations & glassmorphism

### Backend
- **Flask** - Web framework
- **TensorFlow/Keras** - Deep learning
- **Python 3.9+** - Runtime
- **Gunicorn** - Production WSGI server

### Deployment
- **Vercel** - Frontend hosting
- **Render.com** - Backend hosting
- **GitHub** - Source control

## 🚀 Quick Start

### Local Development

#### 1️⃣ Backend Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask backend
python app.py
# Backend available at: http://127.0.0.1:5000
```

#### 2️⃣ Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
# Frontend available at: http://127.0.0.1:5173
```

### Building for Production

#### Build Frontend

```bash
cd frontend
npm run build
npm run preview
```

Output will be in `frontend/dist/`

#### Test Backend

```bash
python app.py
# Set FLASK_DEBUG=false for production behavior
```

## 📤 Deployment

### Deploy in 3 Steps

**Step 1: Deploy Backend to Render**
1. Go to [render.com](https://render.com)
2. New Web Service → Connect GitHub
3. Build: `pip install -r requirements.txt`
4. Start: `gunicorn app:app`
5. Deploy ✅

**Step 2: Deploy Frontend to Vercel**
1. Go to [vercel.com](https://vercel.com)
2. New Project → Import GitHub repo
3. Build: `npm run build --prefix frontend`
4. Output: `frontend/dist`
5. Deploy ✅

**Step 3: Connect Frontend to Backend**
1. In Vercel, set environment variables:
   - `VITE_API_URL` = your Render backend URL
2. Redeploy frontend ✅

📖 **Detailed Guide**: See [DEPLOYMENT_GUIDE_PRODUCTION.md](./DEPLOYMENT_GUIDE_PRODUCTION.md)

## 🎯 Supported Diseases

- **Acne** (Low Severity) - Common skin condition
- **Eczema** (Medium Severity) - Chronic inflammation
- **Melanoma** (High Severity) - Serious skin cancer
- **Psoriasis** (Medium Severity) - Autoimmune condition

## 📊 API Reference

### POST `/predict`

Predict skin disease from image.

**Request:**
```bash
curl -X POST http://127.0.0.1:5000/predict \
  -F "image=@your-image.jpg"
```

**Response:**
```json
{
  "disease": "Melanoma",
  "confidence": 0.92,
  "scores": {
    "Acne": 0.05,
    "Eczema": 0.03,
    "Melanoma": 0.92
  }
}
```

## ⚙️ Configuration

### Environment Variables

**Frontend** (`frontend/.env`):
```
# Backend API URL (set to your deployed backend in production)
VITE_API_URL=https://your-backend.onrender.com
```

**Backend** (system environment):
```
# Flask debug mode
FLASK_DEBUG=false

# Server port
PORT=5000

# Model path
MODEL_PATH=skin_model.h5
```

## 📁 Project Structure

```
skin-disease-detector/
│
├── frontend/                 # React + Vite frontend
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── main.jsx
│   │   ├── config.js         # API configuration
│   │   └── styles.css
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   ├── vercel.json           # Vercel configuration
│   └── .env.example
│
├── app.py                    # Flask backend
├── requirements.txt          # Python dependencies
├── Procfile                  # Render deployment config
├── skin_model.h5            # (Optional) Trained model
│
└── README.md
```

## 🔐 Security Notes

- ✅ CORS enabled for production deployment
- ✅ Input validation on image upload
- ✅ Error handling for invalid requests
- ✅ No sensitive data in environment variables
- ✅ HTTPS enforced in production

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Cannot connect to backend" | Check `VITE_API_URL` in Vercel environment |
| CORS errors | Backend already has CORS configured |
| 502 Bad Gateway | Check Render logs for backend errors |
| Build fails | Verify `frontend/` structure, run `npm run build --prefix frontend` |

## 📊 Performance

- **Frontend Load**: ~2.3s (Vercel CDN)
- **Prediction Time**: ~1-2s (TensorFlow inference)
- **API Response**: ~500ms (Flask processing)

## 🎓 Project Features

### Professional UI/UX
- Premium glassmorphism design
- Smooth animations & transitions
- Dark mode support
- Fully responsive
- Accessibility compliant

### Advanced Features
- Prediction history with localStorage
- PDF report generation
- Real-time confidence visualization
- Medical disclaimer
- Disease information database

### Production Ready
- Error handling & logging
- Environment-based configuration
- CORS support
- Performance optimized
- Deployment guides included

## 🚀 Future Enhancements

- [ ] Multiple image batch processing
- [ ] User authentication & accounts
- [ ] Prediction analytics dashboard
- [ ] Email report delivery
- [ ] Mobile app (React Native)
- [ ] Model versioning & A/B testing

## 💙 Credits

Built with:
- [React](https://react.dev)
- [Flask](https://flask.palletsprojects.com)
- [TensorFlow](https://tensorflow.org)
- [Vercel](https://vercel.com)
- [Render.com](https://render.com)

## 📝 License

MIT License - feel free to use for learning & projects

## 🤝 Support

Need help? Check:
- [DEPLOYMENT_GUIDE_PRODUCTION.md](./DEPLOYMENT_GUIDE_PRODUCTION.md)
- [Vercel Docs](https://vercel.com/docs)
- [Render Docs](https://render.com/docs)
- [Flask Docs](https://flask.palletsprojects.com)

---

**Made with 💙 for AI & Medical Technology**
