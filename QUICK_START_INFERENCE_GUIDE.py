"""
QUICK START GUIDE - Using the Trained Model
=============================================
How to make predictions on new skin disease images
"""

# ============================================================================
# METHOD 1: BASIC PREDICTION (Simplest)
# ============================================================================

import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import json

# Load model
model = tf.keras.models.load_model('best_model_transfer.h5')

# Load class mapping
with open('class_mapping.json', 'r') as f:
    class_mapping = json.load(f)

# Load and predict on a single image
image_path = 'your_image.jpg'
img = load_img(image_path, target_size=(224, 224))
img_array = img_to_array(img) / 255.0
img_batch = np.expand_dims(img_array, 0)

# Make prediction
proba = model.predict(img_batch, verbose=0)[0]
predicted_idx = np.argmax(proba)
predicted_class = class_mapping[str(predicted_idx)]
confidence = proba[predicted_idx]

print(f"Predicted: {predicted_class}")
print(f"Confidence: {confidence:.2%}")


# ============================================================================
# METHOD 2: BATCH PREDICTIONS (Multiple Images)
# ============================================================================

from pathlib import Path

# Get list of images
image_dir = Path('test_images/')
image_paths = list(image_dir.glob('*.jpg'))

# Batch predict
results = []
for img_path in image_paths:
    img = load_img(img_path, target_size=(224, 224))
    img_array = img_to_array(img) / 255.0
    img_batch = np.expand_dims(img_array, 0)
    
    proba = model.predict(img_batch, verbose=0)[0]
    result = {
        'image': str(img_path.name),
        'predicted_class': class_mapping[str(np.argmax(proba))],
        'confidence': float(np.max(proba))
    }
    results.append(result)

# Display results
for r in results:
    print(f"{r['image']:30s} -> {r['predicted_class']:10s} ({r['confidence']:.2%})")


# ============================================================================
# METHOD 3: DETAILED PREDICTIONS (All Probabilities)
# ============================================================================

def predict_disease(image_path):
    """Make detailed prediction on an image"""
    
    # Load model
    model = tf.keras.models.load_model('best_model_transfer.h5')
    
    with open('class_mapping.json', 'r') as f:
        class_mapping = json.load(f)
    
    # Load image
    img = load_img(image_path, target_size=(224, 224))
    img_array = img_to_array(img) / 255.0
    img_batch = np.expand_dims(img_array, 0)
    
    # Predict
    proba = model.predict(img_batch, verbose=0)[0]
    
    # Format results
    predictions = sorted(
        [(class_mapping[str(i)], float(proba[i])) for i in range(4)],
        key=lambda x: x[1],
        reverse=True
    )
    
    return {
        'top_prediction': predictions[0][0],
        'confidence': predictions[0][1],
        'all_predictions': predictions,
        'probabilities': {
            'Acne': float(proba[0]),
            'Eczema': float(proba[1]),
            'Melanoma': float(proba[2]),
            'Psoriasis': float(proba[3])
        }
    }

# Usage
result = predict_disease('test_image.jpg')
print(f"Top Prediction: {result['top_prediction']} ({result['confidence']:.2%})")
print("\nAll Predictions (Ranked):")
for disease, conf in result['all_predictions']:
    print(f"  {disease:12s}: {conf:6.2%}")


# ============================================================================
# METHOD 4: WITH CONFIDENCE THRESHOLD
# ============================================================================

def predict_with_confidence_threshold(image_path, threshold=0.7):
    """Only predict if confidence exceeds threshold"""
    
    model = tf.keras.models.load_model('best_model_transfer.h5')
    
    with open('class_mapping.json', 'r') as f:
        class_mapping = json.load(f)
    
    img = load_img(image_path, target_size=(224, 224))
    img_array = img_to_array(img) / 255.0
    img_batch = np.expand_dims(img_array, 0)
    
    proba = model.predict(img_batch, verbose=0)[0]
    max_prob = np.max(proba)
    predicted_class = class_mapping[str(np.argmax(proba))]
    
    if max_prob >= threshold:
        return {
            'status': 'SUCCESS',
            'prediction': predicted_class,
            'confidence': float(max_prob)
        }
    else:
        return {
            'status': 'UNCERTAIN',
            'message': f'Confidence {max_prob:.2%} below threshold {threshold:.0%}',
            'top_prediction': predicted_class,
            'confidence': float(max_prob)
        }

# Usage
result = predict_with_confidence_threshold('image.jpg', threshold=0.7)
if result['status'] == 'SUCCESS':
    print(f"✓ {result['prediction']} ({result['confidence']:.2%})")
else:
    print(f"? {result['message']}")


# ============================================================================
# METHOD 5: USING EVALUATION METRICS
# ============================================================================

from sklearn.metrics import confusion_matrix, classification_report
import json

# Load test evaluation results
with open('evaluation_results.json', 'r') as f:
    eval_results = json.load(f)

print(f"Test Accuracy: {eval_results['test_accuracy']:.4f}")
print(f"\nPer-Class Accuracy:")
for class_name, acc in eval_results['per_class_accuracy'].items():
    print(f"  {class_name}: {acc:.2%}")

print(f"\nConfusion Matrix:")
cm = np.array(eval_results['confusion_matrix'])
print(cm)


# ============================================================================
# METHOD 6: LOADING MODEL METADATA
# ============================================================================

import json

# Load model metadata
with open('model_metadata.json', 'r') as f:
    metadata = json.load(f)

print(f"Model: {metadata['model_name']}")
print(f"Base Model: {metadata['base_model']}")
print(f"Input Shape: {metadata['input_shape']}")
print(f"Classes: {metadata['classes']}")
print(f"Total Parameters: {metadata['total_parameters']:,}")
print(f"Test Accuracy: {metadata['test_accuracy_percent']:.2f}%")


# ============================================================================
# DEPLOYMENT: FLASK API EXAMPLE
# ============================================================================

"""
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import json

app = Flask(__name__)
model = load_model('best_model_transfer.h5')

with open('class_mapping.json', 'r') as f:
    class_mapping = json.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    img = load_img(file.stream, target_size=(224, 224))
    img_array = img_to_array(img) / 255.0
    img_batch = np.expand_dims(img_array, 0)
    
    proba = model.predict(img_batch, verbose=0)[0]
    
    return jsonify({
        'predicted_class': class_mapping[str(np.argmax(proba))],
        'confidence': float(np.max(proba)),
        'all_probabilities': {
            'Acne': float(proba[0]),
            'Eczema': float(proba[1]),
            'Melanoma': float(proba[2]),
            'Psoriasis': float(proba[3])
        }
    })

if __name__ == '__main__':
    app.run(debug=False, port=5000)
"""


# ============================================================================
# REQUIREMENTS
# ============================================================================

"""
tensorflow>=2.13.0
keras>=3.0.0
numpy>=1.24.0
pillow>=9.5.0
scikit-learn>=1.3.0
matplotlib>=3.7.0
seaborn>=0.12.0
"""


# ============================================================================
# ERROR HANDLING
# ============================================================================

def safe_predict(image_path):
    """Make prediction with error handling"""
    
    try:
        model = tf.keras.models.load_model('best_model_transfer.h5')
        
        if not Path(image_path).exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        img = load_img(image_path, target_size=(224, 224))
        img_array = img_to_array(img) / 255.0
        img_batch = np.expand_dims(img_array, 0)
        
        proba = model.predict(img_batch, verbose=0)[0]
        
        with open('class_mapping.json', 'r') as f:
            class_mapping = json.load(f)
        
        return {
            'success': True,
            'prediction': class_mapping[str(np.argmax(proba))],
            'confidence': float(np.max(proba))
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

# Usage
result = safe_predict('image.jpg')
if result['success']:
    print(f"✓ {result['prediction']} ({result['confidence']:.2%})")
else:
    print(f"✗ Error: {result['error']}")


# ============================================================================
# PERFORMANCE TIPS
# ============================================================================

"""
1. Batch Processing (Faster for multiple images):
   images = [img_to_array(load_img(p, (224,224)))/255 for p in paths]
   batch = np.array(images)
   predictions = model.predict(batch)

2. GPU Acceleration:
   import tensorflow as tf
   with tf.device('/GPU:0'):
       predictions = model.predict(images)

3. Model Quantization (Faster, lower memory):
   from tf.lite import TFLiteConverter
   converter = TFLiteConverter.from_keras_model(model)
   tflite_model = converter.convert()

4. Caching (Avoid reloading model):
   global_model = tf.keras.models.load_model('model.h5')  # Load once
   # Then reuse global_model for all predictions

5. Batch Size Optimization:
   model.predict(images, batch_size=32)  # Tune based on RAM
"""

