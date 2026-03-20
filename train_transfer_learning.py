"""
Transfer Learning Approach Using Pre-trained MobileNetV2
This is much better for small medical imaging datasets
"""
import tensorflow as tf
from tensorflow.keras import Sequential, Model, layers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.metrics import Precision, Recall
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import json

print("\n" + "=" * 80)
print("TRANSFER LEARNING: MOBILENETV2 FOR SKIN DISEASE CLASSIFICATION")
print("=" * 80)

# Configuration
IMG_HEIGHT, IMG_WIDTH = 224, 224
IMG_CHANNELS = 3
BATCH_SIZE = 32
EPOCHS = 50
NUM_CLASSES = 4

DATASET_SPLIT_DIR = Path("dataset_split")
TRAIN_DIR = DATASET_SPLIT_DIR / "train"
VAL_DIR = DATASET_SPLIT_DIR / "validation"
TEST_DIR = DATASET_SPLIT_DIR / "test"

print(f"\nConfiguration:")
print(f"   Image Size: {IMG_HEIGHT}×{IMG_WIDTH}×{IMG_CHANNELS}")
print(f"   Batch Size: {BATCH_SIZE}")
print(f"   Epochs: {EPOCHS}")
print(f"   Classes: {NUM_CLASSES}")

# ============================================================================
# STEP 1: LOAD PRE-TRAINED BASE MODEL
# ============================================================================

print("\n" + "=" * 80)
print("STEP 1: LOAD PRE-TRAINED MOBILENET V2")
print("=" * 80)

print("\n[LOAD] Loading MobileNetV2 pre-trained on ImageNet...")
base_model = MobileNetV2(
    input_shape=(IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS),
    include_top=False,  # Remove top classification layer
    weights='imagenet'   # Use pre-trained ImageNet weights
)

print("[OK] Base model loaded!")
print(f"    Total layers: {len(base_model.layers)}")

# Freeze base model layers (don't train them)
print("\n[FREEZE] Freezing base model layers...")
base_model.trainable = False
print(f"[OK] Base model layers frozen!")

# ============================================================================
# STEP 2: BUILD TRANSFER LEARNING MODEL
# ============================================================================

print("\n" + "=" * 80)
print("STEP 2: BUILD TRANSFER LEARNING MODEL")
print("=" * 80)

print("\n[BUILD] Creating transfer learning model...")

model = Sequential([
    layers.Input(shape=(IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS)),
    
    # Pre-trained MobileNetV2
    base_model,
    
    # Custom top layers for classification
    layers.GlobalAveragePooling2D(),  # Reduce spatial dimensions
    layers.Dense(256, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.3),
    layers.Dense(128, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.2),
    layers.Dense(NUM_CLASSES, activation='softmax')
])

print("[OK] Model architecture created!")

# ============================================================================
# STEP 3: COMPILE MODEL
# ============================================================================

print("\n" + "=" * 80)
print("STEP 3: COMPILE MODEL")
print("=" * 80)

print("\n[COMPILE] Compiling model with:")

optimizer = Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999)
loss_function = 'categorical_crossentropy'
metrics = ['accuracy', Precision(), Recall()]

model.compile(
    optimizer=optimizer,
    loss=loss_function,
    metrics=metrics
)

print(f"   * Optimizer: Adam (lr=0.001)")
print(f"   * Loss: Categorical Crossentropy")
print(f"   * Metrics: Accuracy, Precision, Recall")
print(f"[OK] Model compiled!")

print(f"\n[INFO] Model Summary:")
model.summary()

# ============================================================================
# STEP 4: PREPARE DATA
# ============================================================================

print("\n" + "=" * 80)
print("STEP 4: PREPARE DATA")
print("=" * 80)

print("\n[GEN] Creating data generators...")

# ImageDataGenerator for training (with augmentation)
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True,
    vertical_flip=True,
    shear_range=0.2,
    brightness_range=[0.7, 1.3],
    width_shift_range=0.2,
    height_shift_range=0.2
)

# ImageDataGenerator for validation/test (only rescale)
val_datagen = ImageDataGenerator(rescale=1./255)

print("\n[LOAD] Loading training data...")
train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=True
)
print(f"    Found {train_generator.samples} training images")

print("\n[LOAD] Loading validation data...")
val_generator = val_datagen.flow_from_directory(
    VAL_DIR,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False
)
print(f"    Found {val_generator.samples} validation images")

print("\n[LOAD] Loading test data...")
test_generator = val_datagen.flow_from_directory(
    TEST_DIR,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False
)
print(f"    Found {test_generator.samples} test images")

# ============================================================================
# STEP 5: SET UP CALLBACKS
# ============================================================================

print("\n" + "=" * 80)
print("STEP 5: SET UP CALLBACKS")
print("=" * 80)

callbacks_list = []

print("\n[1] EarlyStopping Callback:")
early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=15,
    min_delta=0.001,
    restore_best_weights=True
)
callbacks_list.append(early_stopping)
print(f"    * Monitor: val_loss")
print(f"    * Patience: 15 epochs")

print("\n[2] ModelCheckpoint Callback:")
checkpoint = ModelCheckpoint(
    filepath='best_model_transfer.h5',
    monitor='val_accuracy',
    save_best_only=True,
    mode='max'
)
callbacks_list.append(checkpoint)
print(f"    * File: best_model_transfer.h5")
print(f"    * Monitor: val_accuracy")

print("\n[3] ReduceLROnPlateau Callback:")
reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,
    patience=5,
    min_lr=1e-6
)
callbacks_list.append(reduce_lr)
print(f"    * Monitor: val_loss")
print(f"    * Reduction Factor: 0.5x")

print(f"\n[OK] {len(callbacks_list)} callbacks configured!")

# ============================================================================
# STEP 6: TRAIN MODEL
# ============================================================================

print("\n" + "=" * 80)
print("STEP 6: TRAIN MODEL")
print("=" * 80)

print("\n[TRAIN] Starting training...")

history = model.fit(
    train_generator,
    steps_per_epoch=len(train_generator),
    validation_data=val_generator,
    validation_steps=len(val_generator),
    epochs=EPOCHS,
    callbacks=callbacks_list,
    verbose=1
)

print("\n[OK] Training completed!")

# ============================================================================
# STEP 7: EVALUATE MODEL
# ============================================================================

print("\n" + "=" * 80)
print("STEP 7: EVALUATE MODEL")
print("=" * 80)

print("\n[EVAL] Evaluating on test set...")
test_results = model.evaluate(test_generator, verbose=0)
test_loss = test_results[0]
test_accuracy = test_results[1]
test_precision = test_results[2] if len(test_results) > 2 else 0
test_recall = test_results[3] if len(test_results) > 3 else 0

print(f"\n[RESULTS] Test Set Performance:")
print(f"   * Test Loss: {test_loss:.4f}")
print(f"   * Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
print(f"   * Test Precision: {test_precision:.4f}")
print(f"   * Test Recall: {test_recall:.4f}")

# Calculate F1 Score
test_f1 = 2 * (test_precision * test_recall) / (test_precision + test_recall) if (test_precision + test_recall) > 0 else 0
print(f"   * Test F1 Score: {test_f1:.4f}")

# ============================================================================
# STEP 8: SAVE RESULTS
# ============================================================================

print("\n" + "=" * 80)
print("STEP 8: SAVE RESULTS")
print("=" * 80)

# Save model
print("\n[SAVE] Saving model...")
model.save('final_model_transfer.h5')
print(f"    Saved: final_model_transfer.h5")

# Save training history
print("\n[SAVE] Saving training history...")
training_results = {
    'train_loss': [float(x) for x in history.history['loss']],
    'train_accuracy': [float(x) for x in history.history['accuracy']],
    'val_loss': [float(x) for x in history.history['val_loss']],
    'val_accuracy': [float(x) for x in history.history['val_accuracy']],
    'test_loss': float(test_loss),
    'test_accuracy': float(test_accuracy),
    'test_precision': float(test_precision),
    'test_recall': float(test_recall),
    'test_f1': float(test_f1),
    'epochs_trained': len(history.history['loss'])
}

with open('training_results_transfer.json', 'w') as f:
    json.dump(training_results, f, indent=2)
print(f"    Saved: training_results_transfer.json")

# ============================================================================
# STEP 9: VISUALIZE RESULTS
# ============================================================================

print("\n" + "=" * 80)
print("STEP 9: VISUALIZE RESULTS")
print("=" * 80)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Transfer Learning Model - Training Results', fontsize=16, fontweight='bold')

# Plot 1: Training & Validation Accuracy
axes[0, 0].plot(history.history['accuracy'], label='Train Accuracy', marker='o', markersize=4)
axes[0, 0].plot(history.history['val_accuracy'], label='Val Accuracy', marker='s', markersize=4)
axes[0, 0].set_xlabel('Epoch')
axes[0, 0].set_ylabel('Accuracy')
axes[0, 0].set_title('Model Accuracy')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# Plot 2: Training & Validation Loss
axes[0, 1].plot(history.history['loss'], label='Train Loss', marker='o', markersize=4)
axes[0, 1].plot(history.history['val_loss'], label='Val Loss', marker='s', markersize=4)
axes[0, 1].set_xlabel('Epoch')
axes[0, 1].set_ylabel('Loss')
axes[0, 1].set_title('Model Loss')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# Plot 3: Test Metrics
metrics_names = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
metrics_values = [test_accuracy, test_precision, test_recall, test_f1]
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
bars = axes[1, 0].bar(metrics_names, metrics_values, color=colors, alpha=0.7)
axes[1, 0].set_ylabel('Score')
axes[1, 0].set_title('Test Set Metrics')
axes[1, 0].set_ylim([0, 1])
axes[1, 0].grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for bar, val in zip(bars, metrics_values):
    height = bar.get_height()
    axes[1, 0].text(bar.get_x() + bar.get_width()/2., height,
                   f'{val:.3f}', ha='center', va='bottom', fontweight='bold')

# Plot 4: Model Architecture Info
axes[1, 1].axis('off')
info_text = f"""
Transfer Learning Model Summary

Base Model: MobileNetV2 (Pre-trained on ImageNet)
Base Model Layers: {len(base_model.layers)}

Custom Layers:
  • GlobalAveragePooling2D
  • Dense(256, ReLU) + BatchNorm + Dropout(0.3)
  • Dense(128, ReLU) + BatchNorm + Dropout(0.2)
  • Dense({NUM_CLASSES}, Softmax)

Total Parameters: {model.count_params():,}
Trainable Parameters: {sum([tf.size(w).numpy() for w in model.trainable_weights]):,}

Training Configuration:
  • Optimizer: Adam (lr=0.001)
  • Loss: Categorical Crossentropy
  • Batch Size: {BATCH_SIZE}
  • Epochs Trained: {len(history.history['loss'])}

Test Performance:
  • Accuracy: {test_accuracy:.4f}
  • Precision: {test_precision:.4f}
  • Recall: {test_recall:.4f}
  • F1 Score: {test_f1:.4f}
"""
axes[1, 1].text(0.1, 0.5, info_text, fontsize=10, verticalalignment='center',
               fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('training_results_transfer.png', dpi=150, bbox_inches='tight')
print(f"[SAVE] Saved: training_results_transfer.png")

print("\n" + "=" * 80)
print("TRANSFER LEARNING TRAINING COMPLETE!")
print("=" * 80)
print("\nFiles created:")
print("  • best_model_transfer.h5 - Best model checkpoint")
print("  • final_model_transfer.h5 - Final trained model")
print("  • training_results_transfer.json - Training metrics")
print("  • training_results_transfer.png - Result visualizations")
