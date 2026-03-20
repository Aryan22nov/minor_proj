"""
Step 3: Data Preprocessing for Skin Disease Classification

This script handles:
1. Setting image dimensions (height and width)
2. Defining batch size for training
3. Creating data generators for loading images
4. Rescaling pixel values to 0-1 range
5. Converting labels to categorical format

The preprocessed data is ready for model training!
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical
import json

# ============================================================================
# STEP 1: CONFIGURE IMAGE DIMENSIONS AND BATCH SIZE
# ============================================================================

print("=" * 70)
print("STEP 3: DATA PREPROCESSING")
print("=" * 70)

# Image dimensions (standard for CNN models)
IMG_HEIGHT = 224
IMG_WIDTH = 224
IMG_CHANNELS = 3  # RGB color channels

# Batch size for training (balance between memory and gradient stability)
BATCH_SIZE = 32

# Disease classes
DISEASE_CLASSES = ['Acne', 'Eczema', 'Melanoma', 'Psoriasis']
NUM_CLASSES = len(DISEASE_CLASSES)

print(f"\n📐 IMAGE CONFIGURATION:")
print(f"   • Height: {IMG_HEIGHT} pixels")
print(f"   • Width: {IMG_WIDTH} pixels")
print(f"   • Channels: {IMG_CHANNELS} (RGB)")
print(f"   • Batch Size: {BATCH_SIZE}")
print(f"   • Classes: {NUM_CLASSES} ({', '.join(DISEASE_CLASSES)})")

# ============================================================================
# STEP 2: CREATE DATA GENERATORS WITH AUGMENTATION & RESCALING
# ============================================================================

print(f"\n📊 CREATING DATA GENERATORS:")

# Training data generator with augmentation
# Rescalesion: pixel values 0-255 → 0-1 range (normalization)
train_datagen = ImageDataGenerator(
    rescale=1./255,                    # Rescale pixel values to 0-1
    rotation_range=20,                 # Rotate images ±20 degrees
    width_shift_range=0.2,             # Shift width by 20%
    height_shift_range=0.2,            # Shift height by 20%
    shear_range=0.2,                   # Shear transformation
    zoom_range=0.2,                    # Zoom in/out by 20%
    horizontal_flip=True,              # Random horizontal flip
    vertical_flip=True,                # Random vertical flip
    fill_mode='nearest'                # Fill mode for new pixels
)

# Validation/Test data generator (only rescaling, NO augmentation)
val_datagen = ImageDataGenerator(rescale=1./255)

print(f"   • Training generator: Rescaling + Data Augmentation enabled")
print(f"   • Validation generator: Rescaling only (no augmentation)")

# ============================================================================
# STEP 3: LOAD TRAINING DATA FROM DIRECTORY
# ============================================================================

print(f"\n📂 LOADING TRAINING DATASET:")

dataset_path = Path("dataset")

# Load training data
train_data = train_datagen.flow_from_directory(
    directory=str(dataset_path),           # Dataset directory
    target_size=(IMG_HEIGHT, IMG_WIDTH),   # Resize to 224x224
    batch_size=BATCH_SIZE,                 # Batch size = 32
    class_mode='categorical',              # One-hot encoded labels
    shuffle=True,                          # Shuffle samples
    seed=42                                # Reproducibility
)

print(f"   ✓ Found {train_data.samples} images")
print(f"   ✓ Classes: {train_data.class_indices}")
print(f"   ✓ Number of batches: {len(train_data)}")
print(f"   ✓ Image shape per sample: {train_data.image_shape}")

# ============================================================================
# STEP 4: EXTRACT AND ANALYZE ONE BATCH
# ============================================================================

print(f"\n🔍 ANALYZING FIRST BATCH:")

# Get first batch of images and labels
sample_images, sample_labels = next(train_data)

print(f"   • Batch images shape: {sample_images.shape}")
print(f"   • Batch labels shape: {sample_labels.shape}")
print(f"   • Pixel value range: [{sample_images.min():.3f}, {sample_images.max():.3f}]")
print(f"   • Label encoding (one-hot): \n     {[f'{cls}: {idx}' for idx, cls in enumerate(DISEASE_CLASSES)]}")

# Check class distribution in batch
label_counts = np.sum(sample_labels, axis=0)
print(f"\n   📈 Class distribution in batch:")
for idx, disease_class in enumerate(DISEASE_CLASSES):
    count = int(label_counts[idx])
    print(f"      • {disease_class}: {count} images")

# ============================================================================
# STEP 5: VISUALIZE PREPROCESSED SAMPLE IMAGES
# ============================================================================

print(f"\n📸 VISUALIZING PREPROCESSED SAMPLES:")

# Create figure with subplots
fig, axes = plt.subplots(2, 4, figsize=(14, 7))
fig.suptitle('Preprocessed Sample Images (Normalized to 0-1 range)', fontsize=14, fontweight='bold')

# Plot 8 sample images
for idx in range(8):
    ax = axes[idx // 4, idx % 4]
    
    # Get image and label
    image = sample_images[idx]
    label = sample_labels[idx]
    
    # Get class name from label
    class_idx = np.argmax(label)
    class_name = DISEASE_CLASSES[class_idx]
    
    # Display image
    ax.imshow(image)
    ax.set_title(f"{class_name}\n(Normalized)", fontsize=10, fontweight='bold')
    ax.axis('off')
    
    # Print pixel statistics
    print(f"   • Image {idx+1}: {class_name}")
    print(f"     - Min pixel: {image.min():.3f}, Max pixel: {image.max():.3f}")
    print(f"     - Shape: {image.shape}")

plt.tight_layout()
plt.savefig('preprocessed_samples.png', dpi=150, bbox_inches='tight')
print(f"   ✓ Saved visualization: preprocessed_samples.png")
plt.close()

# ============================================================================
# STEP 6: DATA STATISTICS REPORT
# ============================================================================

print(f"\n📊 DATA PREPROCESSING SUMMARY:")

# Count images per class
class_counts = {}
for class_dir in dataset_path.glob("*/"):
    if class_dir.is_dir():
        class_name = class_dir.name
        image_count = len(list(class_dir.glob("*.jpg"))) + len(list(class_dir.glob("*.png")))
        class_counts[class_name] = image_count

print(f"\n   Dataset Statistics:")
total_images = 0
for disease_class in DISEASE_CLASSES:
    count = class_counts.get(disease_class, 0)
    total_images += count
    percentage = (count / sum(class_counts.values())) * 100
    bar = "█" * (count // 5)
    print(f"   • {disease_class:12} {count:3} images ({percentage:5.1f}%) {bar}")

print(f"\n   Total Images: {total_images}")
print(f"   Batch Size: {BATCH_SIZE}")
print(f"   Total Batches: {len(train_data)}")
print(f"   Image Dimensions: {IMG_HEIGHT}×{IMG_WIDTH}×{IMG_CHANNELS}")
print(f"   Pixel Range (normalized): 0.0 - 1.0")
print(f"   Label Encoding: One-hot categorical")

# ============================================================================
# STEP 7: SAVE PREPROCESSING CONFIGURATION
# ============================================================================

config = {
    "image_height": IMG_HEIGHT,
    "image_width": IMG_WIDTH,
    "image_channels": IMG_CHANNELS,
    "batch_size": BATCH_SIZE,
    "num_classes": NUM_CLASSES,
    "disease_classes": DISEASE_CLASSES,
    "total_images": total_images,
    "class_distribution": class_counts,
    "pixel_normalization": "0-1 range",
    "label_encoding": "one-hot categorical",
    "data_augmentation": {
        "rotation_range": 20,
        "width_shift_range": 0.2,
        "height_shift_range": 0.2,
        "shear_range": 0.2,
        "zoom_range": 0.2,
        "horizontal_flip": True,
        "vertical_flip": True
    }
}

# Save configuration
with open('preprocessing_config.json', 'w') as f:
    json.dump(config, f, indent=2)

print(f"\n   ✓ Saved config: preprocessing_config.json")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("✅ DATA PREPROCESSING COMPLETE!")
print("=" * 70)
print(f"\n✓ Images normalized to 0-1 range")
print(f"✓ Labels converted to one-hot categorical format")
print(f"✓ Data augmentation configured for training")
print(f"✓ Ready for model training!")
print("\n" + "=" * 70)
