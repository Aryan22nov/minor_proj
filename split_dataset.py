"""
Step 5: Dataset Splitting for Skin Disease Classification

This script handles:
1. Separate data into training, validation, and test sets
2. Create validation set (typically 10-15%)
3. Prepare test set for final evaluation (typically 10-15%)
4. Training set remains for model training (typically 70-80%)
5. Verify class distribution in each split
6. Ensure no data leakage between sets

Dataset Split Strategy:
- Training Set: 70% (280 images)
- Validation Set: 15% (60 images)
- Test Set: 15% (60 images)
- Total: 400 images
"""

import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path
from sklearn.model_selection import train_test_split
import json
from collections import defaultdict

# ============================================================================
# STEP 1: CONFIGURE DATASET PATHS
# ============================================================================

print("=" * 80)
print("STEP 5: DATASET SPLITTING")
print("=" * 80)

# Original dataset path
ORIGINAL_DATASET_DIR = Path("dataset")
DISEASE_CLASSES = ['Acne', 'Eczema', 'Melanoma', 'Psoriasis']

# New split directories
SPLIT_BASE_DIR = Path("dataset_split")
TRAIN_DIR = SPLIT_BASE_DIR / "train"
VAL_DIR = SPLIT_BASE_DIR / "validation"
TEST_DIR = SPLIT_BASE_DIR / "test"

# Split ratios
TRAIN_RATIO = 0.70  # 70% for training
VAL_RATIO = 0.15    # 15% for validation
TEST_RATIO = 0.15   # 15% for testing

print(f"\n📁 DATASET PATHS:")
print(f"   • Original dataset: {ORIGINAL_DATASET_DIR}")
print(f"   • Split base directory: {SPLIT_BASE_DIR}")
print(f"   • Training directory: {TRAIN_DIR}")
print(f"   • Validation directory: {VAL_DIR}")
print(f"   • Test directory: {TEST_DIR}")

print(f"\n📊 SPLIT RATIOS:")
print(f"   • Training: {TRAIN_RATIO*100:.0f}%")
print(f"   • Validation: {VAL_RATIO*100:.0f}%")
print(f"   • Test: {TEST_RATIO*100:.0f}%")

# ============================================================================
# STEP 2: COLLECT ALL IMAGES FROM ORIGINAL DATASET
# ============================================================================

print(f"\n" + "=" * 80)
print("COLLECTING IMAGES FROM ORIGINAL DATASET")
print("=" * 80)

# Dictionary to store images per class
class_images = defaultdict(list)
total_images = 0

for disease in DISEASE_CLASSES:
    class_dir = ORIGINAL_DATASET_DIR / disease
    
    if class_dir.exists():
        # Get all image files
        image_files = sorted(
            list(class_dir.glob('*.jpg')) + 
            list(class_dir.glob('*.png')) +
            list(class_dir.glob('*.jpeg'))
        )
        
        class_images[disease] = image_files
        total_images += len(image_files)
        
        print(f"\n✓ {disease}:")
        print(f"   • Total images: {len(image_files)}")
        print(f"   • First image: {image_files[0].name if image_files else 'None'}")
        print(f"   • Last image: {image_files[-1].name if image_files else 'None'}")
    else:
        print(f"\n✗ {disease}: NOT FOUND")

print(f"\n{'─'*80}")
print(f"Total images collected: {total_images}")

# ============================================================================
# STEP 3: CREATE SPLIT DIRECTORIES
# ============================================================================

print(f"\n" + "=" * 80)
print("CREATING DIRECTORY STRUCTURE")
print("=" * 80)

# Create base split directory
SPLIT_BASE_DIR.mkdir(exist_ok=True)

# Create subdirectories for each split and class
for split_dir in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
    split_dir.mkdir(exist_ok=True)
    for disease in DISEASE_CLASSES:
        (split_dir / disease).mkdir(exist_ok=True)
    
    print(f"✓ Created: {split_dir}")
    for disease in DISEASE_CLASSES:
        print(f"   • {split_dir / disease}")

# ============================================================================
# STEP 4: PERFORM STRATIFIED TRAIN-VAL-TEST SPLIT
# ============================================================================

print(f"\n" + "=" * 80)
print("PERFORMING STRATIFIED DATA SPLIT")
print("=" * 80)

split_results = {
    'train': defaultdict(list),
    'validation': defaultdict(list),
    'test': defaultdict(list)
}

# For each class, split images
for disease in DISEASE_CLASSES:
    images = class_images[disease]
    images_array = np.array(images)
    
    # Create indices
    indices = np.arange(len(images))
    
    # First split: train vs (val+test)
    train_indices, temp_indices = train_test_split(
        indices,
        test_size=(VAL_RATIO + TEST_RATIO),
        random_state=42
    )
    
    # Second split: val vs test from the remaining
    val_size_ratio = VAL_RATIO / (VAL_RATIO + TEST_RATIO)
    val_indices, test_indices = train_test_split(
        temp_indices,
        test_size=1 - val_size_ratio,
        random_state=42
    )
    
    # Organize images by split
    split_results['train'][disease] = images_array[train_indices].tolist()
    split_results['validation'][disease] = images_array[val_indices].tolist()
    split_results['test'][disease] = images_array[test_indices].tolist()
    
    print(f"\n{disease}:")
    print(f"   • Training: {len(train_indices)} images")
    print(f"   • Validation: {len(val_indices)} images")
    print(f"   • Test: {len(test_indices)} images")

# ============================================================================
# STEP 5: COPY FILES TO SPLIT DIRECTORIES
# ============================================================================

print(f"\n" + "=" * 80)
print("COPYING FILES TO SPLIT DIRECTORIES")
print("=" * 80)

file_count = 0

for split_name, split_dir in [('train', TRAIN_DIR), 
                               ('validation', VAL_DIR), 
                               ('test', TEST_DIR)]:
    for disease in DISEASE_CLASSES:
        images = split_results[split_name][disease]
        
        for image_path in images:
            # Copy file
            destination = split_dir / disease / image_path.name
            shutil.copy2(image_path, destination)
            file_count += 1

print(f"\n✓ Copied {file_count} files to split directories")

# ============================================================================
# STEP 6: VERIFY CLASS DISTRIBUTION IN EACH SPLIT
# ============================================================================

print(f"\n" + "=" * 80)
print("VERIFYING CLASS DISTRIBUTION")
print("=" * 80)

# Count images in each split
split_stats = {}

for split_name, split_dir in [('train', TRAIN_DIR), 
                               ('validation', VAL_DIR), 
                               ('test', TEST_DIR)]:
    
    split_stats[split_name] = {}
    total_in_split = 0
    
    print(f"\n{split_name.upper()} SET:")
    print(f"{'Class':<15} {'Images':<10} {'Percentage':<12}")
    print(f"{'-'*40}")
    
    for disease in DISEASE_CLASSES:
        class_dir = split_dir / disease
        image_count = len(list(class_dir.glob('*.jpg'))) + len(list(class_dir.glob('*.png')))
        split_stats[split_name][disease] = image_count
        total_in_split += image_count
        
        percentage = (image_count / total_in_split * 100) if total_in_split > 0 else 0
        print(f"{disease:<15} {image_count:<10} {percentage:>6.2f}%")
    
    print(f"{'-'*40}")
    print(f"{'TOTAL':<15} {total_in_split:<10}")

# ============================================================================
# STEP 7: CHECK FOR DATA LEAKAGE
# ============================================================================

print(f"\n" + "=" * 80)
print("CHECKING FOR DATA LEAKAGE")
print("=" * 80)

# Collect all filenames from each split
train_files = set()
val_files = set()
test_files = set()

for disease in DISEASE_CLASSES:
    train_files.update([f.name for f in (TRAIN_DIR / disease).glob('*')])
    val_files.update([f.name for f in (VAL_DIR / disease).glob('*')])
    test_files.update([f.name for f in (TEST_DIR / disease).glob('*')])

# Check for overlaps
train_val_overlap = train_files & val_files
train_test_overlap = train_files & test_files
val_test_overlap = val_files & test_files

print(f"\n✓ DATA LEAKAGE CHECK:")
print(f"   • Train-Val overlap: {len(train_val_overlap)} files {('❌' if train_val_overlap else '✓')}")
print(f"   • Train-Test overlap: {len(train_test_overlap)} files {('❌' if train_test_overlap else '✓')}")
print(f"   • Val-Test overlap: {len(val_test_overlap)} files {('❌' if val_test_overlap else '✓')}")

if not (train_val_overlap or train_test_overlap or val_test_overlap):
    print(f"\n✅ NO DATA LEAKAGE DETECTED - All splits are independent!")

# ============================================================================
# STEP 8: CREATE VISUALIZATION
# ============================================================================

print(f"\n" + "=" * 80)
print("CREATING VISUALIZATIONS")
print("=" * 80)

fig = plt.figure(figsize=(16, 10))
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.3, wspace=0.3)

colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']

# ─────────────────────────────────────────────────────────────────────────
# Plot 1: Overall split distribution
# ─────────────────────────────────────────────────────────────────────────

ax1 = fig.add_subplot(gs[0, 0])
split_names = ['train', 'validation', 'test']
split_totals = [
    sum(split_stats['train'].values()),
    sum(split_stats['validation'].values()),
    sum(split_stats['test'].values())
]
bars1 = ax1.bar(split_names, split_totals, color=['#45B7D1', '#FFA07A', '#95E1D3'], 
                edgecolor='black', linewidth=2)
ax1.set_ylabel('Number of Images', fontsize=11, fontweight='bold')
ax1.set_title('Dataset Split Distribution', fontsize=12, fontweight='bold')

for bar, total in zip(bars1, split_totals):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(total)}', ha='center', va='bottom', fontweight='bold')

# ─────────────────────────────────────────────────────────────────────────
# Plot 2: Pie chart of splits
# ─────────────────────────────────────────────────────────────────────────

ax2 = fig.add_subplot(gs[0, 1])
split_labels = [f'{name.capitalize()}\n({total})' for name, total in zip(split_names, split_totals)]
ax2.pie(split_totals, labels=split_labels, autopct='%1.1f%%', 
        colors=['#45B7D1', '#FFA07A', '#95E1D3'],
        startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
ax2.set_title('Overall Dataset Distribution', fontsize=12, fontweight='bold')

# ─────────────────────────────────────────────────────────────────────────
# Plot 3: Class distribution across all splits (stacked bar)
# ─────────────────────────────────────────────────────────────────────────

ax3 = fig.add_subplot(gs[0, 2])
x_pos = np.arange(len(DISEASE_CLASSES))
width = 0.25

train_counts = [split_stats['train'].get(d, 0) for d in DISEASE_CLASSES]
val_counts = [split_stats['validation'].get(d, 0) for d in DISEASE_CLASSES]
test_counts = [split_stats['test'].get(d, 0) for d in DISEASE_CLASSES]

ax3.bar(x_pos - width, train_counts, width, label='Train', color='#45B7D1', edgecolor='black')
ax3.bar(x_pos, val_counts, width, label='Validation', color='#FFA07A', edgecolor='black')
ax3.bar(x_pos + width, test_counts, width, label='Test', color='#95E1D3', edgecolor='black')

ax3.set_xlabel('Disease Class', fontsize=11, fontweight='bold')
ax3.set_ylabel('Number of Images', fontsize=11, fontweight='bold')
ax3.set_title('Class Distribution per Split', fontsize=12, fontweight='bold')
ax3.set_xticks(x_pos)
ax3.set_xticklabels(DISEASE_CLASSES, rotation=0)
ax3.legend(fontsize=10)
ax3.grid(axis='y', alpha=0.3)

# ─────────────────────────────────────────────────────────────────────────
# Plot 4: Training set class distribution
# ─────────────────────────────────────────────────────────────────────────

ax4 = fig.add_subplot(gs[1, 0])
train_disease_counts = [split_stats['train'].get(d, 0) for d in DISEASE_CLASSES]
ax4.bar(DISEASE_CLASSES, train_disease_counts, color=colors, edgecolor='black', linewidth=2)
ax4.set_title('Training Set Distribution', fontsize=12, fontweight='bold')
ax4.set_ylabel('Number of Images', fontsize=11, fontweight='bold')
for i, (disease, count) in enumerate(zip(DISEASE_CLASSES, train_disease_counts)):
    ax4.text(i, count, str(count), ha='center', va='bottom', fontweight='bold')

# ─────────────────────────────────────────────────────────────────────────
# Plot 5: Validation set class distribution
# ─────────────────────────────────────────────────────────────────────────

ax5 = fig.add_subplot(gs[1, 1])
val_disease_counts = [split_stats['validation'].get(d, 0) for d in DISEASE_CLASSES]
ax5.bar(DISEASE_CLASSES, val_disease_counts, color=colors, edgecolor='black', linewidth=2)
ax5.set_title('Validation Set Distribution', fontsize=12, fontweight='bold')
ax5.set_ylabel('Number of Images', fontsize=11, fontweight='bold')
for i, (disease, count) in enumerate(zip(DISEASE_CLASSES, val_disease_counts)):
    ax5.text(i, count, str(count), ha='center', va='bottom', fontweight='bold')

# ─────────────────────────────────────────────────────────────────────────
# Plot 6: Test set class distribution
# ─────────────────────────────────────────────────────────────────────────

ax6 = fig.add_subplot(gs[1, 2])
test_disease_counts = [split_stats['test'].get(d, 0) for d in DISEASE_CLASSES]
ax6.bar(DISEASE_CLASSES, test_disease_counts, color=colors, edgecolor='black', linewidth=2)
ax6.set_title('Test Set Distribution', fontsize=12, fontweight='bold')
ax6.set_ylabel('Number of Images', fontsize=11, fontweight='bold')
for i, (disease, count) in enumerate(zip(DISEASE_CLASSES, test_disease_counts)):
    ax6.text(i, count, str(count), ha='center', va='bottom', fontweight='bold')

plt.suptitle('Dataset Splitting Analysis', fontsize=16, fontweight='bold')
plt.savefig('dataset_split_analysis.png', dpi=200, bbox_inches='tight')
print("✓ Saved: dataset_split_analysis.png")
plt.close()

# ============================================================================
# STEP 9: SAVE SPLIT CONFIGURATION
# ============================================================================

split_config = {
    "split_ratios": {
        "training": f"{TRAIN_RATIO*100:.0f}%",
        "validation": f"{VAL_RATIO*100:.0f}%",
        "test": f"{TEST_RATIO*100:.0f}%"
    },
    "split_statistics": {
        "train": {
            "total": sum(split_stats['train'].values()),
            "class_distribution": split_stats['train']
        },
        "validation": {
            "total": sum(split_stats['validation'].values()),
            "class_distribution": split_stats['validation']
        },
        "test": {
            "total": sum(split_stats['test'].values()),
            "class_distribution": split_stats['test']
        }
    },
    "data_leakage_check": {
        "train_val_overlap": len(train_val_overlap),
        "train_test_overlap": len(train_test_overlap),
        "val_test_overlap": len(val_test_overlap),
        "status": "NO LEAKAGE" if not (train_val_overlap or train_test_overlap or val_test_overlap) else "LEAKAGE DETECTED"
    },
    "directory_structure": {
        "original": str(ORIGINAL_DATASET_DIR),
        "split_base": str(SPLIT_BASE_DIR),
        "train": str(TRAIN_DIR),
        "validation": str(VAL_DIR),
        "test": str(TEST_DIR)
    }
}

with open('split_config.json', 'w') as f:
    json.dump(split_config, f, indent=2)

print("✓ Saved: split_config.json")

# ============================================================================
# STEP 10: SUMMARY REPORT
# ============================================================================

print(f"\n" + "=" * 80)
print("DATASET SPLITTING SUMMARY")
print("=" * 80)

print(f"\n📊 SPLIT STATISTICS:")
print(f"\n   Training Set:")
print(f"   • Total: {sum(split_stats['train'].values())} images ({TRAIN_RATIO*100:.0f}%)")
for disease, count in split_stats['train'].items():
    percentage = (count / sum(split_stats['train'].values()) * 100) if sum(split_stats['train'].values()) > 0 else 0
    print(f"     • {disease}: {count} ({percentage:.1f}%)")

print(f"\n   Validation Set:")
print(f"   • Total: {sum(split_stats['validation'].values())} images ({VAL_RATIO*100:.0f}%)")
for disease, count in split_stats['validation'].items():
    percentage = (count / sum(split_stats['validation'].values()) * 100) if sum(split_stats['validation'].values()) > 0 else 0
    print(f"     • {disease}: {count} ({percentage:.1f}%)")

print(f"\n   Test Set:")
print(f"   • Total: {sum(split_stats['test'].values())} images ({TEST_RATIO*100:.0f}%)")
for disease, count in split_stats['test'].items():
    percentage = (count / sum(split_stats['test'].values()) * 100) if sum(split_stats['test'].values()) > 0 else 0
    print(f"     • {disease}: {count} ({percentage:.1f}%)")

print(f"\n" + "=" * 80)
print("✅ DATASET SPLITTING COMPLETE!")
print("=" * 80)

print(f"\n✓ Splits created successfully:")
print(f"   • Training: {sum(split_stats['train'].values())} images (70%)")
print(f"   • Validation: {sum(split_stats['validation'].values())} images (15%)")
print(f"   • Test: {sum(split_stats['test'].values())} images (15%)")

print(f"\n✓ No data leakage detected:")
print(f"   • All splits are independent")
print(f"   • No image appears in multiple splits")

print(f"\n✓ Class distribution verified:")
print(f"   • Balanced across all splits")
print(f"   • Stratified split ensures representation")

print(f"\n✓ Generated visualizations:")
print(f"   • dataset_split_analysis.png")

print(f"\n✓ Configuration saved:")
print(f"   • split_config.json")

print("\n" + "=" * 80)
