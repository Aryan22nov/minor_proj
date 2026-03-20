"""
Steps 11-14: Model Evaluation, Predictions, Visualization & Export
===================================================================
- Step 11: Make Predictions
- Step 12: Visualize Results
- Step 13: Save and Export Model
- Step 14: Test with New Images
"""

import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc
from sklearn.preprocessing import label_binarize
from pathlib import Path
import json
import pickle

print("\n" + "="*80)
print("STEP 11-14: PREDICTIONS, VISUALIZATION, EXPORT & TESTING")
print("="*80)

# Configuration
IMG_HEIGHT, IMG_WIDTH = 224, 224
CLASS_NAMES = ['Acne', 'Eczema', 'Melanoma', 'Psoriasis']
NUM_CLASSES = len(CLASS_NAMES)
TEST_DIR = Path("dataset_split/test")

# ============================================================================
# STEP 11: MAKE PREDICTIONS
# ============================================================================

print("\n" + "="*80)
print("STEP 11: MAKE PREDICTIONS ON TEST SET")
print("="*80)

print("\n[LOAD] Loading trained model...")
model = tf.keras.models.load_model('best_model_transfer.h5')
print(f"[OK] Model loaded!")

# Load test images
from tensorflow.keras.preprocessing.image import ImageDataGenerator

test_datagen = ImageDataGenerator(rescale=1./255)
test_generator = test_datagen.flow_from_directory(
    TEST_DIR,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=32,
    class_mode='categorical',
    shuffle=False
)

print(f"\n[LOAD] Loading {test_generator.samples} test images...")

# Get all test predictions and labels
y_true = test_generator.classes
y_pred_proba = model.predict(test_generator, verbose=1)
y_pred = np.argmax(y_pred_proba, axis=1)

print(f"[OK] Predictions complete!")
print(f"    Test samples: {len(y_true)}")
print(f"    Predictions shape: {y_pred_proba.shape}")

# ============================================================================
# CALCULATE TEST ACCURACY
# ============================================================================

print("\n" + "-"*80)
print("TEST SET ACCURACY")
print("-"*80)

test_accuracy = np.mean(y_pred == y_true)
print(f"\nOverall Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")

# Per-class accuracy
print(f"\nPer-Class Accuracy:")
for i, class_name in enumerate(CLASS_NAMES):
    class_mask = y_true == i
    if class_mask.sum() > 0:
        class_acc = np.mean(y_pred[class_mask] == y_true[class_mask])
        total = class_mask.sum()
        correct = (y_pred[class_mask] == y_true[class_mask]).sum()
        print(f"  {class_name:12s}: {class_acc:.4f} ({correct}/{total})")

# ============================================================================
# GENERATE CONFUSION MATRIX
# ============================================================================

print("\n" + "-"*80)
print("CONFUSION MATRIX")
print("-"*80)

cm = confusion_matrix(y_true, y_pred)
print(f"\nConfusion Matrix:")
print(f"{'':12s} " + " ".join(f"{name:>12s}" for name in CLASS_NAMES))
for i, row in enumerate(cm):
    print(f"{CLASS_NAMES[i]:12s} " + " ".join(f"{val:>12d}" for val in row))

# ============================================================================
# CLASSIFICATION REPORT
# ============================================================================

print("\n" + "-"*80)
print("CLASSIFICATION REPORT")
print("-"*80)

report = classification_report(y_true, y_pred, target_names=CLASS_NAMES, digits=4)
print(f"\n{report}")

# ============================================================================
# STEP 12: VISUALIZE RESULTS
# ============================================================================

print("\n" + "="*80)
print("STEP 12: VISUALIZE RESULTS")
print("="*80)

# Create comprehensive visualization figure
fig = plt.figure(figsize=(20, 16))

# 1. Confusion Matrix Heatmap
ax1 = plt.subplot(3, 3, 1)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=CLASS_NAMES, 
            yticklabels=CLASS_NAMES, cbar=True, ax=ax1, annot_kws={'size': 12})
ax1.set_title('Confusion Matrix', fontsize=14, fontweight='bold')
ax1.set_ylabel('True Label')
ax1.set_xlabel('Predicted Label')

# 2. Normalized Confusion Matrix
ax2 = plt.subplot(3, 3, 2)
cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
sns.heatmap(cm_normalized, annot=True, fmt='.2f', cmap='RdYlGn', 
            xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES, cbar=True, ax=ax2,
            annot_kws={'size': 10}, vmin=0, vmax=1)
ax2.set_title('Normalized Confusion Matrix', fontsize=14, fontweight='bold')
ax2.set_ylabel('True Label')
ax2.set_xlabel('Predicted Label')

# 3. Per-Class Accuracy
ax3 = plt.subplot(3, 3, 3)
per_class_acc = []
for i in range(NUM_CLASSES):
    class_mask = y_true == i
    if class_mask.sum() > 0:
        acc = np.mean(y_pred[class_mask] == y_true[class_mask])
        per_class_acc.append(acc)
    else:
        per_class_acc.append(0)

bars = ax3.bar(CLASS_NAMES, per_class_acc, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
ax3.set_ylim([0, 1])
ax3.set_ylabel('Accuracy', fontweight='bold')
ax3.set_title('Per-Class Accuracy', fontsize=14, fontweight='bold')
ax3.grid(True, alpha=0.3, axis='y')
for bar, acc in zip(bars, per_class_acc):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
            f'{acc:.2%}', ha='center', va='bottom', fontweight='bold')

# 4. Prediction Confidence Distribution
ax4 = plt.subplot(3, 3, 4)
max_confidence = np.max(y_pred_proba, axis=1)
ax4.hist(max_confidence, bins=20, color='steelblue', alpha=0.7, edgecolor='black')
ax4.set_xlabel('Prediction Confidence', fontweight='bold')
ax4.set_ylabel('Frequency', fontweight='bold')
ax4.set_title('Prediction Confidence Distribution', fontsize=14, fontweight='bold')
ax4.axvline(np.mean(max_confidence), color='red', linestyle='--', linewidth=2, label=f'Mean: {np.mean(max_confidence):.3f}')
ax4.legend()
ax4.grid(True, alpha=0.3, axis='y')

# 5-8. Per-class probability distributions
for class_idx in range(NUM_CLASSES):
    ax = plt.subplot(3, 3, 5 + class_idx)
    class_mask = y_true == class_idx
    if class_mask.sum() > 0:
        class_probs = y_pred_proba[class_mask, class_idx]
        ax.hist(class_probs, bins=15, color=f'C{class_idx}', alpha=0.7, edgecolor='black')
        ax.set_xlabel('Confidence Score', fontweight='bold')
        ax.set_ylabel('Frequency', fontweight='bold')
        ax.set_title(f'{CLASS_NAMES[class_idx]} Confidence Distribution', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
    else:
        ax.text(0.5, 0.5, 'No samples', ha='center', va='center', transform=ax.transAxes)

plt.tight_layout()
plt.savefig('step12_evaluation_visualizations.png', dpi=150, bbox_inches='tight')
print("\n[SAVE] Saved: step12_evaluation_visualizations.png")

# ============================================================================
# VISUALIZE SAMPLE PREDICTIONS WITH IMAGES
# ============================================================================

print("\n[VIZ] Generating sample predictions with images...")

fig, axes = plt.subplots(3, 4, figsize=(16, 12))
fig.suptitle('Sample Test Set Predictions', fontsize=16, fontweight='bold')

# Get actual image paths
image_paths = []
for class_idx, class_name in enumerate(CLASS_NAMES):
    class_dir = TEST_DIR / class_name
    image_paths.extend(list(class_dir.glob('*.jpg')))

# Randomly select 12 images
selected_indices = np.random.choice(len(image_paths), min(12, len(image_paths)), replace=False)

for plot_idx, img_idx in enumerate(selected_indices):
    ax = axes[plot_idx // 4, plot_idx % 4]
    
    img_path = image_paths[img_idx]
    img = load_img(img_path, target_size=(IMG_HEIGHT, IMG_WIDTH))
    img_array = img_to_array(img) / 255.0
    
    # Get prediction
    pred_proba = model.predict(np.expand_dims(img_array, 0), verbose=0)[0]
    pred_class_idx = np.argmax(pred_proba)
    pred_class = CLASS_NAMES[pred_class_idx]
    confidence = pred_proba[pred_class_idx]
    
    # Get true class
    true_class_idx = 0
    for i, name in enumerate(CLASS_NAMES):
        if img_path.parent.name == name:
            true_class_idx = i
            break
    true_class = CLASS_NAMES[true_class_idx]
    
    # Display
    ax.imshow(np.array(img))
    is_correct = pred_class == true_class
    color = 'green' if is_correct else 'red'
    
    title = f"True: {true_class}\nPred: {pred_class} ({confidence:.2%})"
    ax.set_title(title, fontweight='bold', color=color, fontsize=10)
    ax.axis('off')

plt.tight_layout()
plt.savefig('step12_sample_predictions.png', dpi=150, bbox_inches='tight')
print("[SAVE] Saved: step12_sample_predictions.png")

# ============================================================================
# ROC CURVES (Multi-class)
# ============================================================================

print("\n[VIZ] Generating ROC curves...")

fig, ax = plt.subplots(figsize=(12, 8))

# Binarize labels for multi-class ROC
y_true_bin = label_binarize(y_true, classes=range(NUM_CLASSES))

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

for i in range(NUM_CLASSES):
    fpr, tpr, _ = roc_curve(y_true_bin[:, i], y_pred_proba[:, i])
    roc_auc = auc(fpr, tpr)
    ax.plot(fpr, tpr, color=colors[i], lw=2, label=f'{CLASS_NAMES[i]} (AUC = {roc_auc:.3f})')

ax.plot([0, 1], [0, 1], 'k--', lw=2, label='Random Classifier')
ax.set_xlim([0.0, 1.0])
ax.set_ylim([0.0, 1.05])
ax.set_xlabel('False Positive Rate', fontweight='bold', fontsize=12)
ax.set_ylabel('True Positive Rate', fontweight='bold', fontsize=12)
ax.set_title('ROC Curves - Multi-class', fontweight='bold', fontsize=14)
ax.legend(loc="lower right", fontsize=10)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('step12_roc_curves.png', dpi=150, bbox_inches='tight')
print("[SAVE] Saved: step12_roc_curves.png")

# ============================================================================
# STEP 13: SAVE AND EXPORT MODEL
# ============================================================================

print("\n" + "="*80)
print("STEP 13: SAVE AND EXPORT MODEL")
print("="*80)

# Save model in multiple formats
print("\n[EXPORT] Saving model in multiple formats...")

# 1. Native Keras format (recommended)
print("  • Saving as native Keras format...")
model.save('skin_disease_model.keras')
print("    Saved: skin_disease_model.keras")

# 2. H5 format (already done, but confirm)
print("  • Model already saved as best_model_transfer.h5")

# 3. Model JSON (architecture)
print("  • Exporting model architecture...")
model_json = model.to_json()
with open('model_architecture.json', 'w') as f:
    json.dump(json.loads(model_json), f, indent=2)
print("    Saved: model_architecture.json")

# 4. Class names mapping
print("  • Exporting class names mapping...")
class_mapping = {i: name for i, name in enumerate(CLASS_NAMES)}
with open('class_mapping.json', 'w') as f:
    json.dump(class_mapping, f, indent=2)
print("    Saved: class_mapping.json")

# 5. Model metadata
print("  • Exporting model metadata...")
model_info = {
    'model_name': 'Skin Disease Classification - Transfer Learning',
    'base_model': 'MobileNetV2 (ImageNet pre-trained)',
    'input_shape': [IMG_HEIGHT, IMG_WIDTH, 3],
    'num_classes': NUM_CLASSES,
    'classes': CLASS_NAMES,
    'total_parameters': int(model.count_params()),
    'trainable_parameters': int(sum([tf.size(w).numpy() for w in model.trainable_weights])),
    'test_accuracy': float(test_accuracy),
    'test_accuracy_percent': float(test_accuracy * 100),
    'confusion_matrix': cm.tolist(),
    'per_class_accuracy': {CLASS_NAMES[i]: float(per_class_acc[i]) for i in range(NUM_CLASSES)},
    'training_framework': 'TensorFlow/Keras',
    'creation_date': '2026-03-20'
}

with open('model_metadata.json', 'w') as f:
    json.dump(model_info, f, indent=2)
print("    Saved: model_metadata.json")

# 6. Evaluation results
print("  • Exporting evaluation results...")
eval_results = {
    'test_accuracy': float(test_accuracy),
    'per_class_accuracy': {CLASS_NAMES[i]: float(per_class_acc[i]) for i in range(NUM_CLASSES)},
    'confusion_matrix': cm.tolist(),
    'classification_report': report,
    'num_test_samples': len(y_true),
    'num_correct': int((y_pred == y_true).sum()),
    'num_incorrect': int((y_pred != y_true).sum())
}

with open('evaluation_results.json', 'w') as f:
    json.dump(eval_results, f, indent=2)
print("    Saved: evaluation_results.json")

print("\n[OK] Model export complete!")
print("\nExported files:")
print("  • skin_disease_model.keras - Native Keras format")
print("  • best_model_transfer.h5 - HDF5 format model")
print("  • model_architecture.json - Model architecture")
print("  • class_mapping.json - Class name mapping")
print("  • model_metadata.json - Complete model metadata")
print("  • evaluation_results.json - Test results")

# ============================================================================
# STEP 14: TEST WITH NEW IMAGES
# ============================================================================

print("\n" + "="*80)
print("STEP 14: TEST WITH NEW IMAGES")
print("="*80)

def predict_image(image_path, confidence_threshold=0.3):
    """
    Load an image and make a prediction
    
    Args:
        image_path: Path to image file
        confidence_threshold: Minimum confidence to show prediction
    
    Returns:
        Dictionary with prediction results
    """
    try:
        # Load and preprocess image
        img = load_img(image_path, target_size=(IMG_HEIGHT, IMG_WIDTH))
        img_array = img_to_array(img) / 255.0
        img_batch = np.expand_dims(img_array, 0)
        
        # Make prediction
        proba = model.predict(img_batch, verbose=0)[0]
        pred_class_idx = np.argmax(proba)
        pred_class = CLASS_NAMES[pred_class_idx]
        confidence = proba[pred_class_idx]
        
        result = {
            'image_path': str(image_path),
            'predicted_class': pred_class,
            'confidence': float(confidence),
            'all_probabilities': {CLASS_NAMES[i]: float(proba[i]) for i in range(NUM_CLASSES)},
            'is_high_confidence': bool(confidence >= confidence_threshold),
            'top_3_predictions': sorted(
                [(CLASS_NAMES[i], float(proba[i])) for i in range(NUM_CLASSES)],
                key=lambda x: x[1],
                reverse=True
            )[:3]
        }
        
        return result
    
    except Exception as e:
        return {'error': str(e), 'image_path': str(image_path)}

# Test with some validation set images
print("\n[TEST] Making predictions on sample images...\n")

sample_test_images = list(TEST_DIR.glob('*/*.jpg'))[:5]

for img_path in sample_test_images:
    result = predict_image(img_path)
    
    if 'error' not in result:
        true_class = img_path.parent.name
        is_correct = result['predicted_class'] == true_class
        status = "[OK]" if is_correct else "[--]"
        
        print(f"{status} Image: {img_path.name}")
        print(f"  True Class:      {true_class}")
        print(f"  Predicted Class: {result['predicted_class']}")
        print(f"  Confidence:      {result['confidence']:.4f}")
        print(f"  Top-3 Predictions:")
        for pred_class, prob in result['top_3_predictions']:
            print(f"    • {pred_class:12s}: {prob:.4f}")
        print()

# Save predictions on all test images
print("[SAVE] Saving predictions on all test images...")

all_predictions = []
for img_path in sample_test_images:
    result = predict_image(img_path)
    all_predictions.append(result)

with open('test_image_predictions.json', 'w') as f:
    json.dump(all_predictions, f, indent=2)
print("Saved: test_image_predictions.json")

# ============================================================================
# VISUALIZATION: SINGLE IMAGE PREDICTION
# ============================================================================

print("\n[VIZ] Generating single image prediction visualization...")

# Select a test image
test_img_path = sample_test_images[0]
result = predict_image(test_img_path)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Load and display image
img = load_img(test_img_path, target_size=(IMG_HEIGHT, IMG_WIDTH))
axes[0].imshow(img)
axes[0].set_title(f'Image: {test_img_path.name}', fontweight='bold', fontsize=12)
axes[0].axis('off')

# Display predictions as bar chart
proba = result['all_probabilities']
colors_list = ['green' if CLASS_NAMES[i] == result['predicted_class'] else 'steelblue' 
               for i in range(NUM_CLASSES)]
bars = axes[1].barh(CLASS_NAMES, list(proba.values()), color=colors_list, alpha=0.8)
axes[1].set_xlabel('Probability', fontweight='bold', fontsize=11)
axes[1].set_title('Prediction Probabilities', fontweight='bold', fontsize=12)
axes[1].set_xlim([0, 1])

# Add value labels
for bar, (class_name, prob) in zip(bars, proba.items()):
    axes[1].text(prob + 0.02, bar.get_y() + bar.get_height()/2, 
                f'{prob:.4f}', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('step14_single_prediction.png', dpi=150, bbox_inches='tight')
print("Saved: step14_single_prediction.png")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*80)
print("STEPS 11-14 COMPLETE!")
print("="*80)

summary = f"""
FINAL RESULTS SUMMARY
=====================

Test Set Performance:
  • Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)
  • Correct Predictions: {(y_pred == y_true).sum()}/{len(y_true)}
  • Confusion Matrix: {len(CLASS_NAMES)}×{len(CLASS_NAMES)}

Per-Class Performance:
"""

for i, class_name in enumerate(CLASS_NAMES):
    class_mask = y_true == i
    if class_mask.sum() > 0:
        class_acc = np.mean(y_pred[class_mask] == y_true[class_mask])
        correct = (y_pred[class_mask] == y_true[class_mask]).sum()
        total = class_mask.sum()
        summary += f"\n  • {class_name:12s}: {class_acc:.4f} ({correct}/{total})"

summary += f"""

Model Architecture:
  • Base Model: MobileNetV2 (ImageNet pre-trained)
  • Total Parameters: {int(model.count_params()):,}
  • Trainable Parameters: {int(sum([tf.size(w).numpy() for w in model.trainable_weights])):,}
  • Input Shape: {IMG_HEIGHT}×{IMG_WIDTH}×3
  • Output Classes: {NUM_CLASSES}

Exported Files:
  [OK] skin_disease_model.keras - Native Keras format
  [OK] best_model_transfer.h5 - HDF5 format
  [OK] model_architecture.json - Architecture
  [OK] class_mapping.json - Class labels
  [OK] model_metadata.json - Full metadata
  [OK] evaluation_results.json - Test results
  [OK] test_image_predictions.json - Sample predictions

Visualizations Generated:
  [OK] step12_evaluation_visualizations.png - Confusion matrix & metrics
  [OK] step12_sample_predictions.png - Sample predictions
  [OK] step12_roc_curves.png - ROC curves
  [OK] step14_single_prediction.png - Single image prediction

Ready for Deployment!
"""

print(summary)

# Save summary
with open('FINAL_RESULTS_SUMMARY.txt', 'w') as f:
    f.write(summary)

print("\nSummary saved to: FINAL_RESULTS_SUMMARY.txt")
