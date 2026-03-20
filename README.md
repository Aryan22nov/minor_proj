# Skin Disease Detector (Flask + CNN)

This repository contains a full-stack demo for a skin disease classification system.
It includes:

- ✅ A **Flask backend** that exposes a `/predict` API and serves the frontend
- ✅ A **React frontend** (modern UI, drag‑and‑drop, image preview, result cards)
- ✅ A **placeholder CNN model loader** (expects `skin_model.h5`)
- ✅ Built-in support for serving a **production build** from Flask

> Note: This repo does **not** include a trained model file. Add your own Keras `.h5` model for real predictions.

---

## 🚀 Quick Start

1) Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Place your trained Keras model at `skin_model.h5` (or set `MODEL_PATH`):

```bash
# example
mv ~/downloads/skin_model.h5 .
```

3) Run the server:

```bash
python app.py
```

4) Open the demo in your browser:

```
http://127.0.0.1:5000/
```

---

## 🧠 How it works

- Frontend uploads an image to `/predict`.
- Backend preprocesses the image (resize + normalize).
- Backend loads the CNN model and runs a prediction.
- Backend returns the most likely disease and confidence score.

---

## ✅ Files & structure

- `app.py` - Flask server + prediction endpoint
- `templates/index.html` - Simple web UI
- `static/` - Frontend JS + CSS
- `requirements.txt` - Python dependencies

---

## 📌 Tips for training your model

When training your Keras model, make sure preprocessing matches the code in `app.py`:

- Resize images to `224×224`
- Normalize pixels to `[0, 1]`

Save the model as:

```python
model.save("skin_model.h5")
```

---

## 🧩 Extending the project

Ideas you can add:

- Add a **camera upload** flow using `getUserMedia`
- Store prediction history in a **database**
- Add **authentication** (login) to protect access
- Deploy to **Railway/Render/Heroku**

---

If you'd like, I can also help you convert this into a **React UI**, add a **login system**, or create a full **project report** with diagrams for your viva.

---

## 🧩 Frontend (React + Vite)

A full React frontend is included under `frontend/`.

### Run the React app

```bash
cd frontend
npm install
npm run dev
```

Then open:

```
http://localhost:5173
```

The React app uses a proxy so requests to `/predict` are forwarded to `http://127.0.0.1:5000`.

### Build a production frontend

Option A (manual):

```bash
cd frontend
npm run build
```

Option B (single command):

```bash
./build.sh
```

You can then serve `frontend/dist` using any static host.

### Serve the built frontend via Flask

After running `npm run build`, the Flask server will automatically serve the built React app from `frontend/dist` (no additional copy needed). Just run:

```bash
python app.py
```

Then open:

```
http://127.0.0.1:5000/
```
