"""
STEP 2: LOAD AND EXPLORE DATASET
═════════════════════════════════════════════════════════════════════════

This script explores the skin disease dataset:
1. Sets paths to dataset directories
2. Defines disease class names
3. Counts images in each class
4. Displays sample images
5. Checks image dimensions and color channels

Output:
- Dataset statistics visualization
- Sample images grid from each category
- Detailed image information report
"""

import os
from pathlib import Path
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from collections import defaultdict

# ============================================================================
# STEP 1: DATASET CONFIGURATION
# ============================================================================

print("\n" + "="*80)
print("STEP 1: DATASET CONFIGURATION")
print("="*80)

# Define paths
BASE_DIR = Path.cwd()
DATASET_DIR = BASE_DIR / "dataset"

# Disease class names
DISEASE_CLASSES = ['Acne', 'Eczema', 'Melanoma', 'Psoriasis']

# Create directory paths for each class
CLASS_DIRS = {
    disease: DATASET_DIR / disease 
    for disease in DISEASE_CLASSES
}

print(f"\nBase Directory: {BASE_DIR}")
print(f"Dataset Directory: {DATASET_DIR}")
print(f"\nDisease Classes: {DISEASE_CLASSES}")
print(f"Number of Classes: {len(DISEASE_CLASSES)}")

# ============================================================================
# STEP 2: COUNT IMAGES IN EACH CLASS
# ============================================================================

print("\n" + "="*80)
print("STEP 2: IMAGE COUNT BY CLASS")
print("="*80)

image_counts = {}
total_images = 0

for disease in DISEASE_CLASSES:
    class_dir = CLASS_DIRS[disease]
    
    if class_dir.exists():
        # Count images (.jpg, .jpeg, .png)
        image_files = list(class_dir.glob('*.jpg')) + \
                      list(class_dir.glob('*.jpeg')) + \
                      list(class_dir.glob('*.png')) + \
                      list(class_dir.glob('*.JPG'))
        
        count = len(image_files)
        image_counts[disease] = count
        total_images += count
        
        print(f"\n✓ {disease:12} | Images: {count:4} | Path: {class_dir}")
    else:
        print(f"\n✗ {disease:12} | DIRECTORY NOT FOUND")
        image_counts[disease] = 0

print(f"\n{'-'*80}")
print(f"{'TOTAL IMAGES':12} | {total_images:4}")
print("="*80)

# ============================================================================
# STEP 3: LOAD SAMPLE IMAGES AND CHECK PROPERTIES
# ============================================================================

print("\n" + "="*80)
print("STEP 3: IMAGE PROPERTIES ANALYSIS")
print("="*80)

image_properties = {}

for disease in DISEASE_CLASSES:
    class_dir = CLASS_DIRS[disease]
    image_files = list(class_dir.glob('*.jpg')) + list(class_dir.glob('*.png'))
    
    if image_files:
        # Analyze first image
        first_image_path = image_files[0]
        img = Image.open(first_image_path)
        
        # Get properties
        width, height = img.size
        mode = img.mode
        channels = len(img.getbands())
        
        image_properties[disease] = {
            'width': width,
            'height': height,
            'mode': mode,
            'channels': channels,
            'first_image': first_image_path.name
        }
        
        print(f"\n{'Disease':<15} {disease}")
        print(f"{'  Dimensions':<15} {width} × {height} pixels")
        print(f"{'  Color Mode':<15} {mode} ({channels} channels)")
        print(f"{'  Sample File':<15} {first_image_path.name}")

# ============================================================================
# STEP 4: CREATE VISUALIZATION
# ============================================================================

print("\n" + "="*80)
print("STEP 4: CREATING VISUALIZATIONS")
print("="*80)

# Create figure with multiple subplots
fig = plt.figure(figsize=(16, 12))
gs = gridspec.GridSpec(3, 4, figure=fig, hspace=0.4, wspace=0.3)

# ─────────────────────────────────────────────────────────────────────────
# Subplot 1: Bar chart of image counts
# ─────────────────────────────────────────────────────────────────────────

ax_counts = fig.add_subplot(gs[0, :2])
diseases = list(image_counts.keys())
counts = list(image_counts.values())
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']

bars = ax_counts.bar(diseases, counts, color=colors, edgecolor='black', linewidth=2)
ax_counts.set_ylabel('Number of Images', fontsize=12, fontweight='bold')
ax_counts.set_title('Images per Disease Class', fontsize=14, fontweight='bold')
ax_counts.set_ylim(0, max(counts) * 1.2)

# Add value labels on bars
for bar, count in zip(bars, counts):
    height = bar.get_height()
    ax_counts.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(count)}',
                   ha='center', va='bottom', fontweight='bold', fontsize=11)

# ─────────────────────────────────────────────────────────────────────────
# Subplot 2: Pie chart of dataset distribution
# ─────────────────────────────────────────────────────────────────────────

ax_pie = fig.add_subplot(gs[0, 2:])
percentages = [c / total_images * 100 for c in counts]
wedges, texts, autotexts = ax_pie.pie(
    counts, 
    labels=diseases, 
    autopct='%1.1f%%',
    colors=colors,
    startangle=90,
    textprops={'fontsize': 11, 'fontweight': 'bold'}
)

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')

ax_pie.set_title('Dataset Distribution', fontsize=14, fontweight='bold')

# ─────────────────────────────────────────────────────────────────────────
# Subplots 3-6: Sample images from each class
# ─────────────────────────────────────────────────────────────────────────

for idx, disease in enumerate(DISEASE_CLASSES):
    ax = fig.add_subplot(gs[1:, idx])
    
    class_dir = CLASS_DIRS[disease]
    image_files = list(class_dir.glob('*.jpg')) + list(class_dir.glob('*.png'))
    
    if image_files:
        # Load and display first image
        sample_image_path = image_files[0]
        sample_image = Image.open(sample_image_path)
        
        ax.imshow(sample_image)
        ax.axis('off')
        
        # Get image info
        width, height = sample_image.size
        mode = sample_image.mode
        
        title = f'{disease}\n'
        title += f'Size: {width}×{height}\n'
        title += f'Mode: {mode}\n'
        title += f'Sample: {sample_image_path.name}'
        
        ax.set_title(title, fontsize=11, fontweight='bold', pad=10)
    else:
        ax.text(0.5, 0.5, 'No images found', 
                ha='center', va='center', fontsize=12)
        ax.axis('off')

plt.suptitle('Skin Disease Dataset Exploration', 
             fontsize=16, fontweight='bold', y=0.995)

print("\n✓ Saving visualization to 'dataset_exploration.png'...")
plt.savefig('dataset_exploration.png', dpi=300, bbox_inches='tight')
print("✓ Visualization saved successfully!")

plt.show()

# ============================================================================
# STEP 5: DETAILED SUMMARY REPORT
# ============================================================================

print("\n" + "="*80)
print("STEP 5: DATASET SUMMARY REPORT")
print("="*80)

print("\n📊 DATASET STATISTICS:")
print(f"   • Total Images: {total_images}")
print(f"   • Total Classes: {len(DISEASE_CLASSES)}")
print(f"   • Images per Class: {total_images / len(DISEASE_CLASSES):.0f} (average)")
print(f"   • Training/Test Split Suggestion: 80/20 or 70/30")

print("\n🏥 DISEASE CLASSES:")
for i, disease in enumerate(DISEASE_CLASSES, 1):
    count = image_counts[disease]
    percentage = (count / total_images * 100) if total_images > 0 else 0
    print(f"   {i}. {disease:12} - {count:3} images ({percentage:.1f}%)")

print("\n🖼️  IMAGE SPECIFICATIONS:")
for disease, props in image_properties.items():
    print(f"   {disease}:")
    print(f"      - Dimensions: {props['width']} × {props['height']} pixels")
    print(f"      - Color Mode: {props['mode']} ({props['channels']} channels)")

print("\n✅ DATASET READY FOR:")
print("   • Model training with ImageDataGenerator")
print("   • Train/validation/test splits")
print("   • Preprocessing and augmentation")

print("\n" + "="*80)
print("Dataset exploration complete! ✓")
print("="*80 + "\n")

# ============================================================================
# STEP 6: ADVANCED STATISTICS (Optional)
# ============================================================================

print("\n" + "="*80)
print("BONUS: DETAILED STATISTICS")
print("="*80)

for disease in DISEASE_CLASSES:
    class_dir = CLASS_DIRS[disease]
    image_files = list(class_dir.glob('*.jpg')) + list(class_dir.glob('*.png'))
    
    if image_files:
        print(f"\n{disease} Folder Analysis:")
        print(f"   • Total files: {len(image_files)}")
        
        # Get file sizes
        file_sizes = [img_file.stat().st_size / 1024 for img_file in image_files]
        avg_size = np.mean(file_sizes)
        
        print(f"   • Avg file size: {avg_size:.1f} KB")
        print(f"   • Min file size: {min(file_sizes):.1f} KB")
        print(f"   • Max file size: {max(file_sizes):.1f} KB")
        
        # Analyze image dimensions consistency
        dimensions = []
        for img_file in image_files[:min(10, len(image_files))]:  # Check first 10
            try:
                img = Image.open(img_file)
                dimensions.append(img.size)
            except:
                pass
        
        if dimensions:
            all_same = len(set(dimensions)) == 1
            consistency = "✓ Consistent" if all_same else "⚠ Varied"
            print(f"   • Dimension consistency: {consistency}")

print("\n" + "="*80)
