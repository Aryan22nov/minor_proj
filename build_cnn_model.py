"""
Step 6: Build CNN Model for Skin Disease Classification

This script builds a comprehensive Convolutional Neural Network (CNN) with:
1. Input layer with image shape (224×224×3)
2. Convolutional layers with ReLU activation
3. Pooling layers (MaxPooling) for downsampling
4. Dropout layers for regularization (prevent overfitting)
5. Batch normalization for training stability
6. Flatten layer to convert to 1D
7. Dense layers with ReLU activation
8. Output layer with Softmax activation (4 classes)

Architecture:
Input → Conv → Pool → Conv → Pool → Conv → Pool → Flatten → Dense → Output
"""

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Conv2D, MaxPooling2D, Dropout, Flatten, Dense, 
    BatchNormalization, Input
)
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import matplotlib.pyplot as plt
import numpy as np
import json

# ============================================================================
# STEP 1: DEFINE MODEL PARAMETERS
# ============================================================================

print("=" * 80)
print("STEP 6: BUILD CNN MODEL")
print("=" * 80)

# Image specifications
IMG_HEIGHT = 224
IMG_WIDTH = 224
IMG_CHANNELS = 3

# Model specifications
NUM_CLASSES = 4
DISEASE_CLASSES = ['Acne', 'Eczema', 'Melanoma', 'Psoriasis']

print(f"\n📐 MODEL CONFIGURATION:")
print(f"   • Input Shape: {IMG_HEIGHT}×{IMG_WIDTH}×{IMG_CHANNELS}")
print(f"   • Number of Classes: {NUM_CLASSES}")
print(f"   • Classes: {', '.join(DISEASE_CLASSES)}")

# ============================================================================
# STEP 2: BUILD CNN MODEL ARCHITECTURE
# ============================================================================

print(f"\n" + "=" * 80)
print("BUILDING CNN ARCHITECTURE")
print("=" * 80)

model = Sequential([
    
    # ─────────────────────────────────────────────────────────────────────
    # LAYER 1: Input Layer
    # ─────────────────────────────────────────────────────────────────────
    Input(shape=(IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS)),
    
    # ─────────────────────────────────────────────────────────────────────
    # BLOCK 1: First Convolutional Block
    # ─────────────────────────────────────────────────────────────────────
    # Convolutional Layer 1: 32 filters, 3×3 kernel
    Conv2D(
        filters=32,                    # Number of filters
        kernel_size=(3, 3),            # 3×3 convolution kernel
        padding='same',                # Pad to preserve dimensions
        activation='relu'              # ReLU activation function
    ),
    BatchNormalization(),              # Normalize layer activations
    
    # Convolutional Layer 2: 32 filters, 3×3 kernel
    Conv2D(
        filters=32,
        kernel_size=(3, 3),
        padding='same',
        activation='relu'
    ),
    BatchNormalization(),
    
    # MaxPooling: Downsample 2×2
    MaxPooling2D(
        pool_size=(2, 2),              # 2×2 pooling window
        strides=2                      # Move by 2 pixels each step
    ),
    
    # Dropout: Regularization (drop 25% of neurons)
    Dropout(0.25),
    
    # ─────────────────────────────────────────────────────────────────────
    # BLOCK 2: Second Convolutional Block
    # ─────────────────────────────────────────────────────────────────────
    # Convolutional Layer 3: 64 filters, 3×3 kernel
    Conv2D(
        filters=64,
        kernel_size=(3, 3),
        padding='same',
        activation='relu'
    ),
    BatchNormalization(),
    
    # Convolutional Layer 4: 64 filters, 3×3 kernel
    Conv2D(
        filters=64,
        kernel_size=(3, 3),
        padding='same',
        activation='relu'
    ),
    BatchNormalization(),
    
    # MaxPooling: Downsample 2×2
    MaxPooling2D(
        pool_size=(2, 2),
        strides=2
    ),
    
    # Dropout: Regularization (drop 25% of neurons)
    Dropout(0.25),
    
    # ─────────────────────────────────────────────────────────────────────
    # BLOCK 3: Third Convolutional Block
    # ─────────────────────────────────────────────────────────────────────
    # Convolutional Layer 5: 128 filters, 3×3 kernel
    Conv2D(
        filters=128,
        kernel_size=(3, 3),
        padding='same',
        activation='relu'
    ),
    BatchNormalization(),
    
    # Convolutional Layer 6: 128 filters, 3×3 kernel
    Conv2D(
        filters=128,
        kernel_size=(3, 3),
        padding='same',
        activation='relu'
    ),
    BatchNormalization(),
    
    # MaxPooling: Downsample 2×2
    MaxPooling2D(
        pool_size=(2, 2),
        strides=2
    ),
    
    # Dropout: Regularization (drop 25% of neurons)
    Dropout(0.25),
    
    # ─────────────────────────────────────────────────────────────────────
    # BLOCK 4: Fourth Convolutional Block
    # ─────────────────────────────────────────────────────────────────────
    # Convolutional Layer 7: 256 filters, 3×3 kernel
    Conv2D(
        filters=256,
        kernel_size=(3, 3),
        padding='same',
        activation='relu'
    ),
    BatchNormalization(),
    
    # Convolutional Layer 8: 256 filters, 3×3 kernel
    Conv2D(
        filters=256,
        kernel_size=(3, 3),
        padding='same',
        activation='relu'
    ),
    BatchNormalization(),
    
    # MaxPooling: Downsample 2×2
    MaxPooling2D(
        pool_size=(2, 2),
        strides=2
    ),
    
    # Dropout: Regularization (drop 25% of neurons)
    Dropout(0.25),
    
    # ─────────────────────────────────────────────────────────────────────
    # FLATTEN: Convert 3D feature maps to 1D vector
    # ─────────────────────────────────────────────────────────────────────
    Flatten(),
    
    # ─────────────────────────────────────────────────────────────────────
    # DENSE LAYERS: Classification
    # ─────────────────────────────────────────────────────────────────────
    # Dense Layer 1: 512 units
    Dense(
        units=512,                     # Number of neurons
        activation='relu'              # ReLU activation
    ),
    BatchNormalization(),
    Dropout(0.5),                      # Higher dropout (50%)
    
    # Dense Layer 2: 256 units
    Dense(
        units=256,
        activation='relu'
    ),
    BatchNormalization(),
    Dropout(0.5),                      # Higher dropout (50%)
    
    # Dense Layer 3: 128 units
    Dense(
        units=128,
        activation='relu'
    ),
    BatchNormalization(),
    Dropout(0.5),                      # Higher dropout (50%)
    
    # ─────────────────────────────────────────────────────────────────────
    # OUTPUT LAYER: 4-class classification with Softmax
    # ─────────────────────────────────────────────────────────────────────
    Dense(
        units=NUM_CLASSES,             # 4 output neurons (one per class)
        activation='softmax'           # Softmax for multi-class classification
    )
])

print("\n✓ Model architecture created successfully!")

# ============================================================================
# STEP 3: COMPILE THE MODEL
# ============================================================================

print(f"\n" + "=" * 80)
print("COMPILING MODEL")
print("=" * 80)

# Optimizer: Adam (adaptive learning rate)
optimizer = Adam(
    learning_rate=0.001,              # Learning rate
    beta_1=0.9,                       # Exponential decay rate for 1st moment
    beta_2=0.999                      # Exponential decay rate for 2nd moment
)

# Loss function: Categorical Crossentropy (multi-class classification)
loss_function = 'categorical_crossentropy'

# Metrics: Accuracy
metrics = ['accuracy']

# Compile model
model.compile(
    optimizer=optimizer,
    loss=loss_function,
    metrics=metrics
)

print(f"\n✓ Optimizer: Adam (lr=0.001)")
print(f"✓ Loss Function: Categorical Crossentropy")
print(f"✓ Metrics: Accuracy")

# ============================================================================
# STEP 4: DISPLAY MODEL SUMMARY
# ============================================================================

print(f"\n" + "=" * 80)
print("MODEL SUMMARY")
print("=" * 80)

model.summary()

# Get model statistics
total_params = model.count_params()
trainable_params = sum([tf.keras.backend.count_params(w) for w in model.trainable_weights])
non_trainable_params = total_params - trainable_params

print(f"\n📊 MODEL STATISTICS:")
print(f"   • Total Parameters: {total_params:,}")
print(f"   • Trainable Parameters: {trainable_params:,}")
print(f"   • Non-trainable Parameters: {non_trainable_params:,}")

# ============================================================================
# STEP 5: VISUALIZE MODEL ARCHITECTURE
# ============================================================================

print(f"\n" + "=" * 80)
print("VISUALIZING MODEL ARCHITECTURE")
print("=" * 80)

try:
    tf.keras.utils.plot_model(
        model,
        to_file='model_architecture.png',
        show_shapes=True,
        show_layer_names=True,
        rankdir='TB',
        expand_nested=False,
        dpi=200
    )
    print("✓ Saved: model_architecture.png")
except Exception as e:
    print(f"⚠ Could not save architecture diagram: {e}")

# ============================================================================
# STEP 6: ANALYZE MODEL LAYERS
# ============================================================================

print(f"\n" + "=" * 80)
print("LAYER-BY-LAYER ANALYSIS")
print("=" * 80)

layer_info = []

print(f"\n{'Layer #':<8} {'Type':<20} {'Output Shape':<25} {'Parameters':<12}")
print(f"{'-'*65}")

for idx, layer in enumerate(model.layers):
    layer_type = type(layer).__name__
    try:
        output_shape = str(layer.output.shape)
    except:
        output_shape = str(layer.output_config['shape']) if hasattr(layer, 'output_config') else "Unknown"
    params = layer.count_params()
    
    print(f"{idx:<8} {layer_type:<20} {output_shape:<25} {params:<12,}")
    
    layer_info.append({
        'index': idx,
        'type': layer_type,
        'output_shape': output_shape,
        'parameters': params,
        'config': layer.get_config()
    })

# ============================================================================
# STEP 7: CREATE ARCHITECTURAL DIAGRAMS
# ============================================================================

print(f"\n" + "=" * 80)
print("CREATING ARCHITECTURAL DIAGRAMS")
print("=" * 80)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Diagram 1: Model layers by type
ax1 = axes[0, 0]
layer_types = {}
for layer in model.layers:
    ltype = type(layer).__name__
    layer_types[ltype] = layer_types.get(ltype, 0) + 1

ax1.barh(list(layer_types.keys()), list(layer_types.values()), color='skyblue', edgecolor='black')
ax1.set_xlabel('Count', fontweight='bold')
ax1.set_title('Layers by Type', fontweight='bold', fontsize=12)
ax1.grid(axis='x', alpha=0.3)

# Diagram 2: Parameters per layer
ax2 = axes[0, 1]
layer_names = [f"L{i}" for i in range(len(model.layers))]
layer_params = [layer.count_params() for layer in model.layers]
colors = plt.cm.viridis(np.linspace(0, 1, len(layer_params)))
ax2.bar(layer_names, layer_params, color=colors, edgecolor='black')
ax2.set_ylabel('Parameters', fontweight='bold')
ax2.set_title('Parameters Distribution', fontweight='bold', fontsize=12)
ax2.set_yscale('log')
ax2.tick_params(axis='x', rotation=45)
ax2.grid(axis='y', alpha=0.3)

# Diagram 3: Model description
ax3 = axes[1, 0]
ax3.axis('off')
description = f"""
🏗️ CNN MODEL ARCHITECTURE

📊 Model Overview:
   • Input: {IMG_HEIGHT}×{IMG_WIDTH}×{IMG_CHANNELS}
   • Total Layers: {len(model.layers)}
   • Total Parameters: {total_params:,}
   • Trainable Params: {trainable_params:,}

🔧 Key Components:
   • Convolutional Blocks: 4
   • MaxPooling Layers: 4
   • Dropout Layers: 7
   • Batch Normalization: 11
   • Dense Layers: 4

⚙️ Hyperparameters:
   • Optimizer: Adam (lr=0.001)
   • Loss: Categorical Crossentropy
   • Activation (hidden): ReLU
   • Activation (output): Softmax
   • Classes: {NUM_CLASSES}
"""
ax3.text(0.05, 0.95, description, transform=ax3.transAxes,
         fontsize=10, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

# Diagram 4: Layer flow
ax4 = axes[1, 1]
ax4.axis('off')

flow_text = """
🔄 DATA FLOW THROUGH MODEL

224×224×3 (Input)
  ↓
Conv2D (32 filters) → BatchNorm → ReLU
Conv2D (32 filters) → BatchNorm → ReLU
MaxPool 2×2 → Dropout(0.25)
  ↓ (112×112×32)
Conv2D (64 filters) → BatchNorm → ReLU
Conv2D (64 filters) → BatchNorm → ReLU
MaxPool 2×2 → Dropout(0.25)
  ↓ (56×56×64)
Conv2D (128 filters) → BatchNorm → ReLU
Conv2D (128 filters) → BatchNorm → ReLU
MaxPool 2×2 → Dropout(0.25)
  ↓ (28×28×128)
Conv2D (256 filters) → BatchNorm → ReLU
Conv2D (256 filters) → BatchNorm → ReLU
MaxPool 2×2 → Dropout(0.25)
  ↓ (14×14×256)
Flatten → Dense(512, ReLU) → BN → Dropout(0.5)
       → Dense(256, ReLU) → BN → Dropout(0.5)
       → Dense(128, ReLU) → BN → Dropout(0.5)
       → Dense(4, Softmax)
  ↓
Output: 4-class Probabilities
"""

ax4.text(0.05, 0.95, flow_text, transform=ax4.transAxes,
         fontsize=9, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))

plt.tight_layout()
plt.savefig('cnn_model_analysis.png', dpi=200, bbox_inches='tight')
print("✓ Saved: cnn_model_analysis.png")
plt.close()

# ============================================================================
# STEP 8: SAVE MODEL CONFIGURATION
# ============================================================================

model_config = {
    "architecture": {
        "name": "Skin Disease CNN",
        "input_shape": [IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS],
        "num_classes": NUM_CLASSES,
        "total_layers": len(model.layers),
        "total_parameters": int(total_params),
        "trainable_parameters": int(trainable_params),
        "non_trainable_parameters": int(non_trainable_params)
    },
    "layers": {
        "convolutional_blocks": 4,
        "maxpooling_layers": 4,
        "dropout_layers": 7,
        "batch_normalization_layers": 11,
        "dense_layers": 4,
        "flatten_layers": 1
    },
    "training_config": {
        "optimizer": "Adam",
        "learning_rate": 0.001,
        "loss_function": "categorical_crossentropy",
        "metrics": ["accuracy"],
        "batch_size": 32,
        "epochs": 50
    },
    "regularization": {
        "dropout_rates_conv": [0.25, 0.25, 0.25, 0.25],
        "dropout_rates_dense": [0.5, 0.5, 0.5],
        "batch_normalization": True
    },
    "disease_classes": DISEASE_CLASSES
}

with open('model_config.json', 'w') as f:
    json.dump(model_config, f, indent=2)

print("✓ Saved: model_config.json")

# ============================================================================
# STEP 9: SAVE MODEL ARCHITECTURE (JSON + H5)
# ============================================================================

print(f"\n" + "=" * 80)
print("SAVING MODEL")
print("=" * 80)

# Save model architecture as JSON
model_json = model.to_json()
with open('model_architecture.json', 'w') as f:
    f.write(model_json)
print("✓ Saved model architecture: model_architecture.json")

# Note: Model weights will be saved after training
print("✓ Model structure ready (weights will be saved after training)")

# ============================================================================
# STEP 10: DETAILED COMPONENT EXPLANATION
# ============================================================================

print(f"\n" + "=" * 80)
print("MODEL COMPONENTS EXPLANATION")
print("=" * 80)

components_info = {
    "Convolutional Layers": {
        "purpose": "Extract spatial features from input images",
        "count": 8,
        "filters": [32, 32, 64, 64, 128, 128, 256, 256],
        "kernel_size": "3×3",
        "benefit": "Learn hierarchical features (edges, textures, objects)"
    },
    "MaxPooling Layers": {
        "purpose": "Reduce spatial dimensions, extract dominant features",
        "count": 4,
        "pool_size": "2×2",
        "stride": 2,
        "benefit": "Reduce computation, create translation invariance"
    },
    "Batch Normalization": {
        "purpose": "Normalize layer activations, speed up training",
        "count": 11,
        "benefit": "More stable gradients, faster convergence"
    },
    "Dropout": {
        "purpose": "Prevent overfitting by randomly dropping neurons",
        "count": 7,
        "rate_conv": "25% (convolutional blocks)",
        "rate_dense": "50% (dense layers)",
        "benefit": "Improved generalization on test data"
    },
    "Dense Layers": {
        "purpose": "Learn non-linear decision boundaries",
        "count": 3,
        "units": [512, 256, 128],
        "activation": "ReLU",
        "benefit": "Complex pattern recognition"
    },
    "Output Layer": {
        "purpose": "Generate class probabilities",
        "units": 4,
        "activation": "Softmax",
        "benefit": "Multi-class classification (sum=1.0)"
    }
}

for component, details in components_info.items():
    print(f"\n{component}:")
    for key, value in details.items():
        if key != "component":
            print(f"   {key}: {value}")

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print(f"\n" + "=" * 80)
print("✅ CNN MODEL SUCCESSFULLY BUILT!")
print("=" * 80)

print(f"\n✓ Architecture Summary:")
print(f"   • Input: {IMG_HEIGHT}×{IMG_WIDTH}×{IMG_CHANNELS}")
print(f"   • Convolutional Blocks: 4")
print(f"   • MaxPooling Layers: 4")
print(f"   • Batch Normalization: 11")
print(f"   • Dropout Layers: 7")
print(f"   • Dense Layers: 4")
print(f"   • Output Classes: {NUM_CLASSES}")

print(f"\n✓ Model Statistics:")
print(f"   • Total Parameters: {total_params:,}")
print(f"   • Trainable Parameters: {trainable_params:,}")
print(f"   • Model Size (approx): {total_params * 4 / 1024 / 1024:.2f} MB")

print(f"\n✓ Training Configuration:")
print(f"   • Optimizer: Adam (lr=0.001)")
print(f"   • Loss: Categorical Crossentropy")
print(f"   • Batch Size: 32")
print(f"   • Epochs: 50 (with early stopping)")

print(f"\n✓ Generated Files:")
print(f"   • cnn_model_analysis.png")
print(f"   • model_config.json")
print(f"   • model_architecture.json")

print(f"\n✓ Model ready for training!")
print(f"   Next: Train the model on the dataset")

print("\n" + "=" * 80)
