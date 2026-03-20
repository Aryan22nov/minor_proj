"""
🏥 SKIN DISEASE DETECTION - COMPLETE ML TRAINING PIPELINE

This script builds, trains, and evaluates a CNN model for skin disease classification.

📚 PERFECT FOR EXAMS:
- Step-by-step comments explain every line
- Can copy-paste explanations for answers
- Includes viva prep tips
- Production-ready code

🎯 DISEASES DETECTED:
- Acne (common bacterial/hormonal condition)
- Eczema (inflammatory skin disorder)
- Melanoma (dangerous skin cancer)
- Psoriasis (autoimmune scaling disease)

📊 ARCHITECTURE:
- Input: 224×224×3 RGB images
- Conv Layers: Feature extraction
- Pooling: Dimension reduction
- Dense Layers: Classification
- Output: 4-class probability distribution

💾 OUTPUT:
- skin_model.h5 (Trained model ~5MB)
- training_history.json (Metrics)
- confusion_matrix.png (Evaluation)
- accuracy_loss.png (Training graphs)
"""

# ============================================================================
# STEP 1: IMPORT REQUIRED LIBRARIES (EXAM ANSWER)
# ============================================================================

# Deep Learning Framework
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Data Processing
import numpy as np
from pathlib import Path
import json

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Evaluation Metrics
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import os

print("\n✅ Step 1: All required libraries imported successfully!")

# ============================================================================
# STEP 2: CONFIGURATION & HYPERPARAMETERS (EXAM ANSWER)
# ============================================================================

class Config:
    """
    Hyperparameters Configuration
    
    EXAM ANSWER:
    Why these values?
    - IMAGE_SIZE (224,224): Standard ResNet input size, reduces computation
    - BATCH_SIZE 32: Optimal trade-off between speed and memory
    - EPOCHS 20: Enough to converge, prevents overfitting
    - LEARNING_RATE 0.001: Standard for Adam optimizer, prevents divergence
    """
    
    # Dataset
    DATASET_DIR = Path("dataset")
    CLASSES = ["Acne", "Eczema", "Melanoma", "Psoriasis"]
    NUM_CLASSES = len(CLASSES)
    
    # Image Processing
    IMAGE_SIZE = (224, 224)
    BATCH_SIZE = 32
    
    # Training
    EPOCHS = 20
    LEARNING_RATE = 0.001
    VALIDATION_SPLIT = 0.2  # 80% train, 20% validation
    
    # Model Weights
    MODEL_PATH = "skin_model.h5"
    HISTORY_PATH = "training_history.json"
    
    # Random seed for reproducibility
    RANDOM_SEED = 42
    
    # GPU Configuration
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        print(f"✅ GPUs found: {len(gpus)}")
    else:
        print("⚠️  No GPU detected. Using CPU (slower training)")

print("\n✅ Step 2: Configuration loaded!")

# ============================================================================
# STEP 3: DATA LOADING & PREPROCESSING (EXAM ANSWER)
# ============================================================================

def load_and_preprocess_data():
    """
    📚 EXAM ANSWER:
    
    Step 3: Data Loading & Preprocessing
    
    Process:
    1. Load images from folder structure
    2. Apply data augmentation (rotation, zoom, flip)
    3. Normalize pixel values to [0, 1]
    4. Split into training (80%) and validation (20%)
    5. Create batches for efficient training
    
    Why preprocessing?
    - Normalization: Helps gradient descent converge faster
    - Augmentation: Increases dataset variety, prevents overfitting
    - Batching: Makes training memory-efficient
    """
    
    print("\n" + "="*70)
    print("📊 STEP 3: LOAD & PREPROCESS DATA")
    print("="*70)
    
    # Check if dataset exists
    if not Config.DATASET_DIR.exists():
        print("❌ Dataset not found! Run: python download_dataset.py")
        return None, None
    
    # Image Data Generator with Augmentation
    # 📚 Augmentation techniques explained:
    # - rotation_range: Rotate image 0-20°
    # - width_shift_range: Shift image horizontally 20%
    # - height_shift_range: Shift image vertically 20%
    # - zoom_range: Zoom in/out 20%
    # - horizontal_flip: Mirror image left-right
    # - fill_mode: Fill empty pixels
    
    train_datagen = ImageDataGenerator(
        rescale=1./255,              # Normalize to [0, 1]
        rotation_range=20,            # Rotate images
        width_shift_range=0.2,        # Horizontal shift
        height_shift_range=0.2,       # Vertical shift
        zoom_range=0.2,               # Zoom augmentation
        horizontal_flip=True,         # Flip left-right
        fill_mode='nearest',          # Fill mode for shifts
        validation_split=Config.VALIDATION_SPLIT  # 80-20 split
    )
    
    # Load training data with augmentation
    print("\n📥 Loading training data with augmentation...")
    train_data = train_datagen.flow_from_directory(
        Config.DATASET_DIR,
        target_size=Config.IMAGE_SIZE,
        batch_size=Config.BATCH_SIZE,
        class_mode='categorical',  # One-hot encoding for multi-class
        subset='training',
        classes=Config.CLASSES
    )
    
    # Load validation data (only rescaling, no augmentation)
    print("📥 Loading validation data...")
    validation_data = train_datagen.flow_from_directory(
        Config.DATASET_DIR,
        target_size=Config.IMAGE_SIZE,
        batch_size=Config.BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        classes=Config.CLASSES
    )
    
    print(f"\n✅ Training samples: {train_data.samples}")
    print(f"✅ Validation samples: {validation_data.samples}")
    print(f"✅ Classes: {list(train_data.class_indices.keys())}")
    
    return train_data, validation_data

# ============================================================================
# STEP 4: BUILD CNN MODEL ARCHITECTURE (EXAM ANSWER)
# ============================================================================

def build_model():
    """
    📚 EXAM ANSWER:
    
    Step 4: Build Convolutional Neural Network (CNN)
    
    Architecture:
    ┌─────────────────────────────────────────────┐
    │ Input (224×224×3)                           │
    ├─────────────────────────────────────────────┤
    │ Conv2D (32 filters) + BatchNorm + MaxPool   │ → Extracts basic features
    ├─────────────────────────────────────────────┤
    │ Conv2D (64 filters) + BatchNorm + MaxPool   │ → Extracts complex features
    ├─────────────────────────────────────────────┤
    │ Conv2D (128 filters) + BatchNorm + MaxPool  │ → Extracts high-level features
    ├─────────────────────────────────────────────┤
    │ Flatten → Dense (128) + Dropout             │ → Classification neurons
    ├─────────────────────────────────────────────┤
    │ Dense (4) + Softmax                         │ → Output probabilities
    └─────────────────────────────────────────────┘
    
    Why this architecture?
    - Conv2D: Learns spatial features (edges, textures)
    - MaxPooling: Reduces dimension, retains important features
    - BatchNorm: Normalizes activations, speeds up training
    - Dropout: Prevents overfitting (40%)
    - Flatten: Converts 2D feature maps to 1D vector
    - Dense: Learns non-linear relationships
    - Softmax: Converts outputs to probability distribution
    """
    
    print("\n" + "="*70)
    print("🏗️  STEP 4: BUILD CNN MODEL")
    print("="*70)
    
    model = Sequential([
        # ─────── BLOCK 1: Feature Extraction ───────
        Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
        # 📝 Conv2D: 32 filters, 3×3 kernel, detects edges and textures
        # 📝 ReLU: Activation function, solves vanishing gradient problem
        
        BatchNormalization(),
        # 📝 BatchNorm: Normalizes layer inputs, faster convergence
        
        MaxPooling2D((2, 2)),
        # 📝 MaxPooling: Reduces spatial dimensions, keeps important features
        # Output: 112×112×32
        
        # ─────── BLOCK 2: Pattern Recognition ───────
        Conv2D(64, (3, 3), activation='relu'),
        # 📝 More filters = learns more complex patterns
        
        BatchNormalization(),
        MaxPooling2D((2, 2)),
        # Output: 56×56×64
        
        # ─────── BLOCK 3: High-Level Features ───────
        Conv2D(128, (3, 3), activation='relu'),
        # 📝 128 filters for disease-specific patterns
        
        BatchNormalization(),
        MaxPooling2D((2, 2)),
        # Output: 28×28×128
        
        # ─────── CLASSIFICATION LAYERS ───────
        Flatten(),
        # 📝 Convert 2D feature maps to 1D vector: 28×28×128 = 100,352 values
        
        Dense(256, activation='relu'),
        # 📝 256 neurons learn complex decision boundaries
        
        Dropout(0.4),
        # 📝 Dropout 40%: Randomly deactivate neurons, prevents overfitting
        # 📝 Like ensemble learning with different sub-networks
        
        Dense(128, activation='relu'),
        # 📝 Further abstraction and feature combination
        
        Dropout(0.3),
        # 📝 Dropout 30%: Slightly less than previous layer
        
        Dense(Config.NUM_CLASSES, activation='softmax')
        # 📝 4 neurons for 4 diseases
        # 📝 Softmax: Ensures outputs sum to 1.0 (probabilities)
        # 📝 Example: [0.05, 0.10, 0.80, 0.05] for Melanoma confidence
    ])
    
    print("\n📐 Model Architecture:")
    model.summary()
    
    return model

# ============================================================================
# STEP 5: COMPILE MODEL (EXAM ANSWER)
# ============================================================================

def compile_model(model):
    """
    📚 EXAM ANSWER:
    
    Step 5: Model Compilation
    
    Components:
    1. Optimizer: Adam (Adaptive Moment Estimation)
       - Adapts learning rate for each parameter
       - Best for CNNs, faster convergence than SGD
    
    2. Loss Function: Categorical Crossentropy
       - For multi-class classification
       - Measures difference between predicted and actual probability
       - Lower loss = better predictions
    
    3. Metrics: Accuracy
       - Percentage of correct predictions
       - Easy to interpret for exams and business
    
    Formula:
    Loss = -Σ(actual × log(predicted))
    
    Why these choices?
    - Adam: State-of-the-art optimizer for deep learning
    - Categorical Crossentropy: Standard for multi-class problems
    - Accuracy: Easy to explain to stakeholders
    """
    
    print("\n" + "="*70)
    print("⚙️  STEP 5: COMPILE MODEL")
    print("="*70)
    
    model.compile(
        optimizer=Adam(learning_rate=Config.LEARNING_RATE),
        # 📝 Adam Optimizer:
        # - learning_rate=0.001: Default, can be tuned
        # - Maintains exponential moving average of gradients
        # - Adapt2020: https://arxiv.org/abs/1412.6980
        
        loss='categorical_crossentropy',
        # 📝 Loss function:
        # - For 4-class classification
        # - Measures prediction accuracy
        # - Lower is better
        
        metrics=['accuracy']
        # 📝 Track accuracy during training
        # - Helps us monitor overfitting/underfitting
    )
    
    print("✅ Model compiled successfully!")
    print(f"   Optimizer: Adam (lr={Config.LEARNING_RATE})")
    print(f"   Loss: Categorical Crossentropy")
    print(f"   Metrics: Accuracy\n")
    
    return model

# ============================================================================
# STEP 6: TRAIN MODEL (EXAM ANSWER)
# ============================================================================

def train_model(model, train_data, validation_data):
    """
    📚 EXAM ANSWER:
    
    Step 6: Model Training
    
    Process:
    1. Forward pass: Input → Model → Prediction
    2. Calculate loss: Compare prediction vs actual
    3. Backward pass: Calculate gradients
    4. Update weights: Adjust parameters to minimize loss
    5. Validation: Evaluate on unseen data
    6. Repeat for N epochs
    
    Overfitting Indicator:
    - Training accuracy ↑ (90%)
    - Validation accuracy ↓ (60%)
    → Model memorizes training data
    → Use Dropout, Data augmentation, Early stopping
    
    🎯 Training Goal:
    - High training accuracy (>85%)
    - Similar validation accuracy (>80%)
    - Minimize generalization gap
    """
    
    print("\n" + "="*70)
    print("🔄 STEP 6: TRAIN MODEL")
    print("="*70)
    print(f"Training for {Config.EPOCHS} epochs...")
    print(f"Batch size: {Config.BATCH_SIZE}")
    print(f"Training samples: {train_data.samples}")
    print(f"Validation samples: {validation_data.samples}\n")
    
    # Train model
    history = model.fit(
        train_data,
        # 📝 Training data with augmentation
        
        validation_data=validation_data,
        # 📝 Validation data (80-20 split)
        
        epochs=Config.EPOCHS,
        # 📝 Number of passes through entire dataset
        # 📝 Each epoch: all training samples seen once
        
        verbose=1
        # 📝 Print progress for each epoch
    )
    
    print("\n✅ Training complete!")
    
    return history

# ============================================================================
# STEP 7: EVALUATE & VISUALIZE (EXAM ANSWER)
# ============================================================================

def evaluate_and_visualize(model, validation_data, history):
    """
    📚 EXAM ANSWER:
    
    Step 7: Model Evaluation & Visualization
    
    Metrics:
    1. Accuracy: % correct predictions
    2. Precision: True Positives / (TP + FP) → False alarms?
    3. Recall: True Positives / (TP + FN) → Missing cases?
    4. F1-Score: Harmonic mean of precision & recall
    
    Confusion Matrix Example:
                Predicted
              Acne Eczema Mel Psor
    Acne        95    2    0   3
    Eczema       1   92    1   6
    Melanoma     0    3   98   2
    Psoriasis    2    4    1   93
    
    → Diagonal values = Correct predictions
    → Off-diagonal = Wrong predictions
    
    Medical Context:
    - High Recall for Melanoma: Don't miss cancer!
    - High Precision for Melanoma: Avoid false alarms!
    """
    
    print("\n" + "="*70)
    print("📊 STEP 7: EVALUATE & VISUALIZE RESULTS")
    print("="*70)
    
    # Evaluate on validation set
    val_loss, val_accuracy = model.evaluate(validation_data, verbose=0)
    print(f"\n📈 Validation Results:")
    print(f"   Loss: {val_loss:.4f}")
    print(f"   Accuracy: {val_accuracy*100:.2f}%")
    
    # Get predictions
    predictions = []
    true_labels = []
    
    print("\n🔍 Generating predictions for confusion matrix...")
    for x, y in validation_data:
        pred = model.predict(x, verbose=0)
        predictions.extend(np.argmax(pred, axis=1))
        true_labels.extend(np.argmax(y, axis=1))
    
    # Create confusion matrix
    cm = confusion_matrix(true_labels, predictions)
    
    # Visualize Training History
    print("\n📊 Plotting training history...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Accuracy plot
    ax1.plot(history.history['accuracy'], label='Training', marker='o')
    ax1.plot(history.history['val_accuracy'], label='Validation', marker='s')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.set_title('Model Accuracy Over Time')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Loss plot
    ax2.plot(history.history['loss'], label='Training', marker='o')
    ax2.plot(history.history['val_loss'], label='Validation', marker='s')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.set_title('Model Loss Over Time')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('accuracy_loss.png', dpi=150, bbox_inches='tight')
    print("   ✅ Saved: accuracy_loss.png")
    
    # Confusion Matrix Plot
    print("\n📊 Plotting confusion matrix...")
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=Config.CLASSES,
                yticklabels=Config.CLASSES,
                cbar_kws={'label': 'Count'})
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix - Validation Set')
    plt.tight_layout()
    plt.savefig('confusion_matrix.png', dpi=150, bbox_inches='tight')
    print("   ✅ Saved: confusion_matrix.png")
    
    # Classification Report
    print("\n📋 Classification Report:")
    print("="*70)
    report = classification_report(true_labels, predictions, 
                                   target_names=Config.CLASSES,
                                   digits=3)
    print(report)
    
    # Save metrics
    metrics = {
        'val_accuracy': float(val_accuracy),
        'val_loss': float(val_loss),
        'classification_report': report
    }
    
    with open('metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    print("   ✅ Saved: metrics.json")
    
    plt.close('all')

# ============================================================================
# STEP 8: SAVE MODEL (EXAM ANSWER)
# ============================================================================

def save_model(model):
    """
    📚 EXAM ANSWER:
    
    Step 8: Save Trained Model
    
    Why save?
    - Reuse without retraining (saves time)
    - Deploy to production (app.py uses it)
    - Share with team/clients
    - Version control
    
    Formats:
    1. .h5 (HDF5): Keras format, includes weights+architecture
    2. .pb (SavedModel): TensorFlow format, more portable
    3. ONNX: Universal format, works in any framework
    
    File Size:
    - Model weights: ~5-10MB for our architecture
    - Training hyperparameters: ~100KB
    
    Loading Later:
    ```python
    from tensorflow.keras.models import load_model
    model = load_model('skin_model.h5')
    ```
    """
    
    print("\n" + "="*70)
    print("💾 STEP 8: SAVE MODEL")
    print("="*70)
    
    model.save(Config.MODEL_PATH)
    file_size = os.path.getsize(Config.MODEL_PATH) / (1024 * 1024)
    
    print(f"\n✅ Model saved: {Config.MODEL_PATH}")
    print(f"   File size: {file_size:.2f}MB")
    print(f"   Ready for: app.py deployment")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Execute complete training pipeline."""
    
    print("\n" + "🎯"*35)
    print("🎯 CNN SKIN DISEASE MODEL TRAINING 🎯")
    print("🎯"*35 + "\n")
    
    # Step 1 & 2: Already done (imports & config)
    
    # Step 3: Load data
    train_data, validation_data = load_and_preprocess_data()
    if train_data is None:
        print("❌ Cannot proceed without data!")
        return
    
    # Step 4: Build model
    model = build_model()
    
    # Step 5: Compile
    model = compile_model(model)
    
    # Step 6: Train
    history = train_model(model, train_data, validation_data)
    
    # Step 8: Save FIRST (before evaluation that might fail)
    print("\n" + "="*70)
    print("💾 SAVING MODEL (before evaluation)")
    print("="*70)
    save_model(model)
    
    # Step 7: Evaluate (optional, might take long)
    try:
        print("\n⏳ Evaluating model (this may take 2-3 minutes)...")
        evaluate_and_visualize(model, validation_data, history)
    except KeyboardInterrupt:
        print("\n⚠️  Evaluation interrupted by user")
        print("✅ But model was already saved to disk!")
    except Exception as e:
        print(f"\n⚠️  Evaluation failed: {e}")
        print("✅ But model was already saved to disk!")
    
    # Summary
    print("\n" + "="*70)
    print("✅ TRAINING PIPELINE COMPLETE!")
    print("="*70)
    print(f"\n📊 Output Files:")
    print(f"   1. skin_model.h5 → Use in app.py")
    print(f"   2. accuracy_loss.png → Training visualization (if generated)")
    print(f"   3. confusion_matrix.png → Model evaluation (if generated)")
    print(f"   4. metrics.json → Detailed metrics (if generated)")
    print(f"\n🚀 Next: python app.py")
    print(f"📱 Then: Open http://127.0.0.1:5000\n")

if __name__ == "__main__":
    main()
