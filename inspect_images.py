"""
Inspect actual images from the dataset
"""
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
from PIL import Image

print("\n" + "=" * 80)
print("INSPECTING DATASET IMAGES")
print("=" * 80)

dataset_dir = Path("dataset_split")

for set_name in ["train", "validation", "test"]:
    set_path = dataset_dir / set_name
    print(f"\n[{set_name.upper()}]")
    
    # Sample one image from each class
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    fig.suptitle(f"{set_name.upper()} Set - Sample Images")
    axes = axes.ravel()
    
    for class_idx, (class_name, ax) in enumerate(zip(['Acne', 'Eczema', 'Melanoma', 'Psoriasis'], axes)):
        class_dir = set_path / class_name
        images = list(class_dir.glob("*.jpg"))
        
        if images:
            # Load first image
            img_path = images[0]
            img = Image.open(img_path)
            img_array = np.array(img)
            
            ax.imshow(img_array)
            ax.set_title(f"{class_name} ({len(images)} imgs, size: {img.size})")
            ax.axis("off")
            
            print(f"  {class_name}: {len(images)} images")
            print(f"    First image: {img_path.name}, Size: {img.size}, Mode: {img.mode}")
            print(f"    Array shape: {img_array.shape}, dtype: {img_array.dtype}")
            print(f"    Pixel range: [{img_array.min()}, {img_array.max()}]")
        else:
            print(f"  {class_name}: NO IMAGES FOUND!")
    
    plt.tight_layout()
    plt.savefig(f"inspect_{set_name}_images.png", dpi=100, bbox_inches='tight')
    print(f"  Saved: inspect_{set_name}_images.png\n")

print("\n[OK] Inspection complete!")
