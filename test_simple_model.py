"""
Test with a very simple model to verify data pipeline
"""
import tensorflow as tf
from tensorflow.keras import Sequential, layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
from pathlib import Path

print("\n" + "=" * 80)
print("TESTING WITH SIMPLE MODEL")
print("=" * 80)

train_dir = Path("dataset_split/train")
val_dir = Path("dataset_split/validation")

# Simple data generator WITHOUT augmentation
train_datagen = ImageDataGenerator(rescale=1./255)
val_datagen = ImageDataGenerator(rescale=1./255)

train_gen = train_datagen.flow_from_directory(
    train_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

val_gen = val_datagen.flow_from_directory(
    val_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

print(f"\nDatasets:")
print(f"  Train: {train_gen.samples} samples")
print(f"  Val: {val_gen.samples} samples")

# Build a VERY simple model
model = Sequential([
    layers.Input(shape=(224, 224, 3)),
    layers.Conv2D(16, (3, 3), activation='relu', padding='same'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(4, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print(f"\nSimple Model Summary:")
model.summary()

print(f"\n[1] Testing predictions before training...")
batch_x, batch_y = next(train_gen)
preds = model.predict(batch_x, verbose=0)
print(f"    Loss on random batch: {tf.keras.losses.categorical_crossentropy(batch_y, preds).numpy().mean():.4f}")

print(f"\n[2] Training for 1 epoch...")
history = model.fit(
    train_gen,
    epochs=1,
    validation_data=val_gen,
    verbose=1
)

print(f"\n[3] Training loss: {history.history['loss'][0]:.4f}")
print(f"    Validation loss: {history.history['val_loss'][0]:.4f}")
print(f"    Training accuracy: {history.history['accuracy'][0]:.4f}")
print(f"    Validation accuracy: {history.history['val_accuracy'][0]:.4f}")

print(f"\n[OK] Simple model test complete!")
