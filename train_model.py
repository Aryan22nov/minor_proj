"""
Steps 7-10: Compile Model, Set Up Callbacks, Train Model, and Evaluate

This script covers:
7. Compile the Model - Optimizer, Loss, Metrics
8. Set Up Callbacks - Early Stopping, Checkpoints, LR Reduction
9. Train the Model - Fit on training data with validation
10. Evaluate Model Performance - Accuracy, Loss, Test Metrics

Complete end-to-end training pipeline!
"""

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Conv2D, MaxPooling2D, Dropout, Flatten, Dense, 
    BatchNormalization, Input
)
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import (
    EarlyStopping, ModelCheckpoint, ReduceLROnPlateau, TensorBoard
)
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import json
from sklearn.metrics import (
    classification_report, confusion_matrix, accuracy_score,
    precision_score, recall_score, f1_score
)
import seaborn as sns

# ============================================================================
# STEP 0: CONFIGURATION
# ============================================================================

print("=" * 80)
print("STEPS 7-10: MODEL COMPILATION, CALLBACKS, TRAINING, AND EVALUATION")
print("=" * 80)

# Image specifications
IMG_HEIGHT = 224
IMG_WIDTH = 224
IMG_CHANNELS = 3
BATCH_SIZE = 32
EPOCHS = 50

# Paths
DATASET_SPLIT_DIR = Path("dataset_split")
TRAIN_DIR = DATASET_SPLIT_DIR / "train"
VAL_DIR = DATASET_SPLIT_DIR / "validation"
TEST_DIR = DATASET_SPLIT_DIR / "test"

DISEASE_CLASSES = ['Acne', 'Eczema', 'Melanoma', 'Psoriasis']
NUM_CLASSES = len(DISEASE_CLASSES)

print(f"\nConfiguration:")
print(f"   Image Size: {IMG_HEIGHT}×{IMG_WIDTH}×{IMG_CHANNELS}")
print(f"   Batch Size: {BATCH_SIZE}")
print(f"   Epochs: {EPOCHS}")
print(f"   Classes: {NUM_CLASSES}")

# ============================================================================
# STEP 7: BUILD AND COMPILE THE MODEL
# ============================================================================

print("\n" + "=" * 80)
print("STEP 7: BUILD AND COMPILE MODEL")
print("=" * 80)

print("\n[BUILD] Creating CNN model architecture...")

model = Sequential([
    Input(shape=(IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS)),
    
    # Block 1
    Conv2D(32, (3, 3), padding='same', activation='relu'),
    BatchNormalization(),
    Conv2D(32, (3, 3), padding='same', activation='relu'),
    BatchNormalization(),
    MaxPooling2D((2, 2), strides=2),
    Dropout(0.25),
    
    # Block 2
    Conv2D(64, (3, 3), padding='same', activation='relu'),
    BatchNormalization(),
    Conv2D(64, (3, 3), padding='same', activation='relu'),
    BatchNormalization(),
    MaxPooling2D((2, 2), strides=2),
    Dropout(0.25),
    
    # Block 3
    Conv2D(128, (3, 3), padding='same', activation='relu'),
    BatchNormalization(),
    Conv2D(128, (3, 3), padding='same', activation='relu'),
    BatchNormalization(),
    MaxPooling2D((2, 2), strides=2),
    Dropout(0.25),
    
    # Block 4
    Conv2D(256, (3, 3), padding='same', activation='relu'),
    BatchNormalization(),
    Conv2D(256, (3, 3), padding='same', activation='relu'),
    BatchNormalization(),
    MaxPooling2D((2, 2), strides=2),
    Dropout(0.25),
    
    # Dense layers
    Flatten(),
    Dense(512, activation='relu'),
    BatchNormalization(),
    Dropout(0.5),
    Dense(256, activation='relu'),
    BatchNormalization(),
    Dropout(0.5),
    Dense(128, activation='relu'),
    BatchNormalization(),
    Dropout(0.5),
    Dense(NUM_CLASSES, activation='softmax')
])

print("[OK] Model architecture created!")

# ─────────────────────────────────────────────────────────────────────────
# COMPILATION
# ─────────────────────────────────────────────────────────────────────────

print("\n[COMPILE] Compiling model with:")

# Optimizer: Adam
optimizer = Adam(
    learning_rate=0.001,
    beta_1=0.9,
    beta_2=0.999,
    epsilon=1e-7
)
print(f"   * Optimizer: Adam")
print(f"   * Learning Rate: 0.001")
print(f"   * Beta_1: 0.9, Beta_2: 0.999")

# Loss function: Categorical Crossentropy
loss_function = 'categorical_crossentropy'
print(f"   * Loss Function: Categorical Crossentropy")

# Metrics: Accuracy, Precision, Recall
metrics = [
    'accuracy',
    tf.keras.metrics.Precision(),
    tf.keras.metrics.Recall()
]
print(f"   * Metrics: Accuracy, Precision, Recall")

# Compile
model.compile(
    optimizer=optimizer,
    loss=loss_function,
    metrics=metrics
)

print("[OK] Model compiled successfully!")

# Display model summary
print("\n[INFO] Model Summary:")
model.summary()

# ============================================================================
# STEP 8: SET UP CALLBACKS
# ============================================================================

print("\n" + "=" * 80)
print("STEP 8: SET UP CALLBACKS")
print("=" * 80)

callbacks_list = []

# ─────────────────────────────────────────────────────────────────────────
# CALLBACK 1: Early Stopping
# ─────────────────────────────────────────────────────────────────────────
print("\n[1] EarlyStopping Callback:")
early_stopping = EarlyStopping(
    monitor='val_loss',           # Monitor validation loss
    patience=15,                   # Stop if no improvement for 15 epochs
    min_delta=0.001,              # Minimum change to qualify as improvement
    restore_best_weights=True,    # Restore weights from best epoch
    verbose=1
)
callbacks_list.append(early_stopping)

print(f"    * Monitor: val_loss")
print(f"    * Patience: 15 epochs")
print(f"    * Min Delta: 0.001")
print(f"    * Action: Stop training & restore best weights")

# ─────────────────────────────────────────────────────────────────────────
# CALLBACK 2: Model Checkpoint
# ─────────────────────────────────────────────────────────────────────────
print("\n[2] ModelCheckpoint Callback:")
checkpoint = ModelCheckpoint(
    filepath='best_model.h5',     # Save to this file
    monitor='val_accuracy',       # Monitor validation accuracy
    save_best_only=True,          # Only save if better than previous
    mode='max',                   # Maximize accuracy
    verbose=1
)
callbacks_list.append(checkpoint)

print(f"    * File: best_model.h5")
print(f"    * Monitor: val_accuracy")
print(f"    * Save: Only best weights")

# ─────────────────────────────────────────────────────────────────────────
# CALLBACK 3: Reduce Learning Rate on Plateau
# ─────────────────────────────────────────────────────────────────────────
print("\n[3] ReduceLROnPlateau Callback:")
reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',           # Monitor validation loss
    factor=0.5,                   # Multiply learning rate by 0.5
    patience=5,                   # Wait 5 epochs before reducing
    min_lr=1e-6,                 # Minimum learning rate
    verbose=1
)
callbacks_list.append(reduce_lr)

print(f"    * Monitor: val_loss")
print(f"    * Reduction Factor: 0.5x")
print(f"    * Patience: 5 epochs")
print(f"    * Min LR: 1e-6")

print(f"\n[OK] {len(callbacks_list)} callbacks configured!")

# ============================================================================
# STEP 9: PREPARE DATA AND TRAIN
# ============================================================================

print("\n" + "=" * 80)
print("STEP 9: PREPARE DATA AND TRAIN MODEL")
print("=" * 80)

# ─────────────────────────────────────────────────────────────────────────
# Create Data Generators
# ─────────────────────────────────────────────────────────────────────────

print("\n[DATA] Creating data generators...")

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    vertical_flip=True,
    brightness_range=[0.7, 1.3],
    fill_mode='nearest'
)

val_test_datagen = ImageDataGenerator(rescale=1./255)

# Load training data
print("\n[LOAD] Loading training data...")
train_data = train_datagen.flow_from_directory(
    str(TRAIN_DIR),
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=True,
    seed=42
)
print(f"   * Found {train_data.samples} training images")
print(f"   * Classes: {train_data.class_indices}")

# Load validation data
print("\n[LOAD] Loading validation data...")
val_data = val_test_datagen.flow_from_directory(
    str(VAL_DIR),
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False,
    seed=42
)
print(f"   * Found {val_data.samples} validation images")

# Load test data
print("\n[LOAD] Loading test data...")
test_data = val_test_datagen.flow_from_directory(
    str(TEST_DIR),
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False,
    seed=42
)
print(f"   * Found {test_data.samples} test images")

# ─────────────────────────────────────────────────────────────────────────
# Train Model
# ─────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 80)
print("TRAINING ON GPU/CPU...")
print("=" * 80)

history = model.fit(
    train_data,
    epochs=EPOCHS,
    steps_per_epoch=len(train_data),
    validation_data=val_data,
    validation_steps=len(val_data),
    callbacks=callbacks_list,
    verbose=1
)

print("\n[OK] Training completed!")

# ============================================================================
# STEP 10: EVALUATE MODEL PERFORMANCE
# ============================================================================

print("\n" + "=" * 80)
print("STEP 10: EVALUATE MODEL PERFORMANCE")
print("=" * 80)

# ─────────────────────────────────────────────────────────────────────────
# Evaluate on Test Set
# ─────────────────────────────────────────────────────────────────────────

print("\n[EVAL] Evaluating model on test set...")

test_loss, test_accuracy, test_precision, test_recall = model.evaluate(
    test_data,
    verbose=0
)

print(f"\n[RESULTS] Test Set Performance:")
print(f"   * Test Loss: {test_loss:.4f}")
print(f"   * Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
print(f"   * Test Precision: {test_precision:.4f}")
print(f"   * Test Recall: {test_recall:.4f}")

# Calculate F1 Score
test_f1 = 2 * (test_precision * test_recall) / (test_precision + test_recall) if (test_precision + test_recall) > 0 else 0
print(f"   * Test F1 Score: {test_f1:.4f}")

# ─────────────────────────────────────────────────────────────────────────
# Get Predictions on Test Set
# ─────────────────────────────────────────────────────────────────────────

print("\n[PRED] Generating predictions on test set...")

test_data.reset()
y_pred_probs = model.predict(test_data, verbose=0)
y_pred = np.argmax(y_pred_probs, axis=1)
y_true = test_data.classes

print(f"   * Predictions shape: {y_pred_probs.shape}")
print(f"   * Predicted classes: {np.unique(y_pred)}")

# ─────────────────────────────────────────────────────────────────────────
# Classification Report
# ─────────────────────────────────────────────────────────────────────────

print("\n[REPORT] Detailed Classification Report:")
print("\n" + classification_report(y_true, y_pred, target_names=DISEASE_CLASSES))

# ─────────────────────────────────────────────────────────────────────────
# Plot 1: Training and Validation Accuracy
# ─────────────────────────────────────────────────────────────────────────

print("\n[VIZ] Creating visualizations...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Accuracy
ax1 = axes[0, 0]
ax1.plot(history.history['accuracy'], label='Training Accuracy', linewidth=2)
ax1.plot(history.history['val_accuracy'], label='Validation Accuracy', linewidth=2)
ax1.set_xlabel('Epoch', fontweight='bold')
ax1.set_ylabel('Accuracy', fontweight='bold')
ax1.set_title('Model Accuracy', fontweight='bold', fontsize=12)
ax1.legend()
ax1.grid(alpha=0.3)

# Plot 2: Loss
ax2 = axes[0, 1]
ax2.plot(history.history['loss'], label='Training Loss', linewidth=2)
ax2.plot(history.history['val_loss'], label='Validation Loss', linewidth=2)
ax2.set_xlabel('Epoch', fontweight='bold')
ax2.set_ylabel('Loss', fontweight='bold')
ax2.set_title('Model Loss', fontweight='bold', fontsize=12)
ax2.legend()
ax2.grid(alpha=0.3)

# Plot 3: Confusion Matrix
ax3 = axes[1, 0]
cm = confusion_matrix(y_true, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=DISEASE_CLASSES, yticklabels=DISEASE_CLASSES,
            ax=ax3, cbar_kws={'label': 'Count'})
ax3.set_xlabel('Predicted', fontweight='bold')
ax3.set_ylabel('Actual', fontweight='bold')
ax3.set_title('Confusion Matrix (Test Set)', fontweight='bold', fontsize=12)

# Plot 4: Metrics
ax4 = axes[1, 1]
metrics_names = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
metrics_values = [test_accuracy, test_precision, test_recall, test_f1]
colors = ['#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F']
bars = ax4.bar(metrics_names, metrics_values, color=colors, edgecolor='black', linewidth=2)
ax4.set_ylabel('Score', fontweight='bold')
ax4.set_title('Test Set Metrics', fontweight='bold', fontsize=12)
ax4.set_ylim([0, 1])
ax4.grid(axis='y', alpha=0.3)

# Add value labels on bars
for bar, value in zip(bars, metrics_values):
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height,
             f'{value:.3f}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('training_evaluation.png', dpi=200, bbox_inches='tight')
print("   [OK] Saved: training_evaluation.png")
plt.close()

# ─────────────────────────────────────────────────────────────────────────
# Per-Class Performance
# ─────────────────────────────────────────────────────────────────────────

print("\n[PERF] Per-class performance:")
for i, disease in enumerate(DISEASE_CLASSES):
    class_mask = y_true == i
    class_accuracy = accuracy_score(y_true[class_mask], y_pred[class_mask]) if class_mask.sum() > 0 else 0
    print(f"   * {disease}: {class_accuracy*100:.2f}%")

# ─────────────────────────────────────────────────────────────────────────
# Save Training Results
# ─────────────────────────────────────────────────────────────────────────

training_results = {
    "training_config": {
        "epochs_trained": len(history.history['loss']),
        "batch_size": BATCH_SIZE,
        "optimizer": "Adam",
        "learning_rate": 0.001,
        "loss_function": "categorical_crossentropy"
    },
    "test_metrics": {
        "test_loss": float(test_loss),
        "test_accuracy": float(test_accuracy),
        "test_precision": float(test_precision),
        "test_recall": float(test_recall),
        "test_f1_score": float(test_f1)
    },
    "callbacks": {
        "early_stopping": {
            "monitor": "val_loss",
            "patience": 15,
            "best_epoch": len(history.history['loss']) - 15
        },
        "model_checkpoint": {
            "save_best_only": True,
            "monitor": "val_accuracy"
        },
        "reduce_lr": {
            "monitor": "val_loss",
            "factor": 0.5,
            "patience": 5
        }
    },
    "disease_classes": DISEASE_CLASSES,
    "training_history": {
        "accuracy": [float(x) for x in history.history['accuracy']],
        "val_accuracy": [float(x) for x in history.history['val_accuracy']],
        "loss": [float(x) for x in history.history['loss']],
        "val_loss": [float(x) for x in history.history['val_loss']]
    }
}

with open('training_results.json', 'w') as f:
    json.dump(training_results, f, indent=2)
print("\n   [OK] Saved: training_results.json")

# ─────────────────────────────────────────────────────────────────────────
# Save Model
# ─────────────────────────────────────────────────────────────────────────

print("\n[SAVE] Saving model...")

# Save as HDF5
model.save('final_model.h5')
print("   [OK] Saved: final_model.h5")

# Save model architecture
model_json = model.to_json()
with open('final_model_architecture.json', 'w') as f:
    f.write(model_json)
print("   [OK] Saved: final_model_architecture.json")

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("TRAINING COMPLETE - SUMMARY")
print("=" * 80)

print(f"\n[SUMMARY] Model Training Results:")
print(f"\n   Epochs Trained: {len(history.history['loss'])}")
print(f"   Best Val Accuracy: {max(history.history['val_accuracy']):.4f}")
print(f"   Best Val Loss: {min(history.history['val_loss']):.4f}")

print(f"\n   Final Test Performance:")
print(f"   - Accuracy:  {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
print(f"   - Precision: {test_precision:.4f}")
print(f"   - Recall:    {test_recall:.4f}")
print(f"   - F1 Score:  {test_f1:.4f}")

print(f"\n   Saved Files:")
print(f"   - best_model.h5 (best checkpoint)")
print(f"   - final_model.h5 (final model)")
print(f"   - training_results.json (metrics)")
print(f"   - training_evaluation.png (visualizations)")

print(f"\n[OK] Model training and evaluation complete!")
print("\n" + "=" * 80)
