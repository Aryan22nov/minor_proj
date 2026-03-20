"""Flask backend for skin disease prediction.

This app serves a simple web UI and a prediction API endpoint.

Usage:
  1) Install dependencies: pip install -r requirements.txt
  2) Place your trained Keras model at `skin_model.h5` (or set MODEL_PATH env var).
  3) Run: python app.py
  4) Open: http://127.0.0.1:5000/

If a model file is not found, the server returns a dummy prediction (uniform probabilities).
"""

import os
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_from_directory
from PIL import Image
import numpy as np

#------------------------------------------------------------------------------
# Config
#------------------------------------------------------------------------------

MODEL_PATH = os.environ.get("MODEL_PATH", "skin_model.h5")
CLASS_NAMES = ["Acne", "Eczema", "Melanoma"]
TARGET_SIZE = (224, 224)

#------------------------------------------------------------------------------
# App setup
#------------------------------------------------------------------------------

# If a built React app exists under `frontend/dist`, serve it as the main UI.
# Otherwise fall back to the simple Jinja template in `templates/index.html`.

BASE_DIR = Path(__file__).resolve().parent
REACT_DIST = BASE_DIR / "frontend" / "dist"
USE_REACT_DIST = REACT_DIST.exists() and (REACT_DIST / "index.html").exists()

if USE_REACT_DIST:
    # Serve the built React app directly from the dist folder.
    app = Flask(
        __name__,
        static_folder=str(REACT_DIST),
        static_url_path="",
        template_folder=str(REACT_DIST),
    )
else:
    app = Flask(__name__)

# Try to load the model early so startup fails fast if something is wrong.
# If the model is missing, we fall back to a dummy predictor.

def _load_model(path: str):
    try:
        from tensorflow.keras.models import load_model

        if not os.path.exists(path):
            app.logger.warning("Model file not found at %s. Using dummy predictor.", path)
            return None

        model = load_model(path)
        app.logger.info("Loaded model from %s", path)
        return model

    except Exception as exc:  # pylint: disable=broad-except
        app.logger.exception("Failed to load model (using dummy predictor): %s", exc)
        return None


model = _load_model(MODEL_PATH)


#------------------------------------------------------------------------------
# Helpers
#------------------------------------------------------------------------------


def preprocess_image(image: Image.Image) -> np.ndarray:
    """Convert PIL image to model-ready numpy array."""
    image = image.convert("RGB")
    image = image.resize(TARGET_SIZE)
    arr = np.asarray(image, dtype=np.float32) / 255.0
    return np.expand_dims(arr, axis=0)


def predict_from_image(image: Image.Image):
    """Predict class probabilities from a PIL image."""
    x = preprocess_image(image)

    if model is None:
        # Dummy prediction (uniform probabilities)
        probs = np.ones(len(CLASS_NAMES), dtype=np.float32) / len(CLASS_NAMES)
    else:
        probs = model.predict(x)[0]

    class_idx = int(np.argmax(probs))
    return {
        "disease": CLASS_NAMES[class_idx],
        "confidence": float(np.max(probs)),
        "scores": {cls: float(score) for cls, score in zip(CLASS_NAMES, probs)},
    }


#------------------------------------------------------------------------------
# Routes
#------------------------------------------------------------------------------


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def index(path: str):
    """Serve the React build (if available) or fall back to the Jinja template."""
    if USE_REACT_DIST:
        # If the path exists in the built assets, serve it directly.
        candidate = REACT_DIST / path
        if path and candidate.exists():
            return send_from_directory(str(REACT_DIST), path)
        # Otherwise always return the React entry point.
        return send_from_directory(str(REACT_DIST), "index.html")

    # Fallback: use the simple Jinja template.
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "Missing file field 'image'"}), 400

    file_storage = request.files["image"]

    try:
        image = Image.open(file_storage.stream)
    except Exception:
        return jsonify({"error": "Unable to open uploaded file as an image."}), 400

    result = predict_from_image(image)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
