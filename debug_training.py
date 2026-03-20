"""
Debug script to check data loading and model training issues
"""
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

print("=" * 80)
print("DEBUGGING DATA LOADING AND MODEL TRAINING")
print("=" * 80)

# Path configuration
train_dir = Path("dataset_split/train")
val_dir = Path("dataset_split/validation")
test_dir = Path("dataset_split/test")

# Data generators
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

val_datagen = ImageDataGenerator(rescale=1./255)

print("\n[1] LOADING TRAINING DATA...")
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    shuffle=True
)
print(f"    Classes: {train_generator.class_indices}")
print(f"    Total training samples: {train_generator.samples}")
print(f"    Classes in dataset: {train_generator.classes}")

print("\n[2] LOADING VALIDATION DATA...")
val_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    shuffle=False
)
print(f"    Classes: {val_generator.class_indices}")
print(f"    Total validation samples: {val_generator.samples}")

print("\n[3] INSPECTING FIRST BATCH...")
batch_x, batch_y = next(train_generator)
print(f"    Batch X shape: {batch_x.shape} (expected: (32, 224, 224, 3))")
print(f"    Batch X range: [{batch_x.min():.4f}, {batch_x.max():.4f}] (expected: [0, 1])")
print(f"    Batch Y shape: {batch_y.shape} (expected: (32, 4))")
print(f"    Batch Y sample:\n{batch_y[:5]}")
print(f"    Class distribution in batch: {batch_y.sum(axis=0)}")

print("\n[4] CHECKING CLASS LABELS...")
class_order = list(train_generator.class_indices.items())
class_order.sort(key=lambda x: x[1])
print(f"    Class mapping: {class_order}")

# Verify class distribution
print("\n[5] CLASS DISTRIBUTION IN DATASETS:")
train_counts = np.bincount(train_generator.classes)
val_counts = np.bincount(val_generator.classes)
print(f"    Train: {train_counts} (total: {train_counts.sum()})")
print(f"    Val:   {val_counts} (total: {val_counts.sum()})")

print("\n[6] VISUALIZING BATCH SAMPLES...")
# Get original class names
class_names = {v: k for k, v in train_generator.class_indices.items()}
fig, axes = plt.subplots(2, 4, figsize=(12, 6))
axes = axes.ravel()
for i in range(8):
    img = (batch_x[i] * 255).astype(np.uint8)
    label_idx = np.argmax(batch_y[i])
    label_name = class_names[label_idx]
    axes[i].imshow(img)
    axes[i].set_title(f"Class: {label_name}")
    axes[i].axis("off")
plt.tight_layout()
plt.savefig("debug_batch_visualization.png", dpi=100, bbox_inches='tight')
print("    Saved: debug_batch_visualization.png")

print("\n[7] TESTING MODEL WITH BATCH...")
# Build simple test model
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(4, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

print("    Model compiled successfully")
print(f"    Testing prediction on batch...")
predictions = model.predict(batch_x[:4], verbose=0)
print(f"    Predictions shape: {predictions.shape}")
print(f"    Predictions:\n{predictions}")
print(f"    Ground truth:\n{batch_y[:4]}")

# Test one epoch
print("\n[8] TESTING ONE EPOCH OF TRAINING...")
history = model.fit(
    train_generator,
    steps_per_epoch=min(5, len(train_generator)),
    validation_data=val_generator,
    validation_steps=min(2, len(val_generator)),
    epochs=1,
    verbose=1
)

print("\n[9] TESTING PREDICTIONS ON VALIDATION...")
val_predictions = model.predict(val_generator, steps=1, verbose=0)
val_batch_x, val_batch_y = next(val_generator)
print(f"    Val accuracy: {np.mean(np.argmax(val_predictions, axis=1) == np.argmax(val_batch_y, axis=1)):.4f}")

print("\n[OK] Debug complete!")
