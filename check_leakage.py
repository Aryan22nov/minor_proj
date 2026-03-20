"""
Check for duplicate or similar images between splits
"""
import numpy as np
from PIL import Image
from pathlib import Path
import hashlib

print("\n" + "=" * 80)
print("CHECKING FOR DATA LEAKAGE")
print("=" * 80)

def get_file_hash(filepath):
    """Get MD5 hash of file"""
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

dataset_dir = Path("dataset_split")

# Get all image paths
train_dir = dataset_dir / "train"
val_dir = dataset_dir / "validation"
test_dir = dataset_dir / "test"

train_images = {}
val_images = {}
test_images = {}

print("\n[1] Computing file hashes...")

for class_name in ['Acne', 'Eczema', 'Melanoma', 'Psoriasis']:
    for img_path in (train_dir / class_name).glob("*.jpg"):
        img_hash = get_file_hash(img_path)
        train_images[img_path.name] = img_hash
    
    for img_path in (val_dir / class_name).glob("*.jpg"):
        img_hash = get_file_hash(img_path)
        val_images[img_path.name] = img_hash
    
    for img_path in (test_dir / class_name).glob("*.jpg"):
        img_hash = get_file_hash(img_path)
        test_images[img_path.name] = img_hash

print(f"    Train: {len(train_images)} images")
print(f"    Val: {len(val_images)} images")
print(f"    Test: {len(test_images)} images")

print("\n[2] Checking for duplicates...")

def check_overlap(set1, set2, name1, name2):
    """Check if any files are identical"""
    hashes1 = set(set1.values())
    hashes2 = set(set2.values())
    overlap_hashes = hashes1 & hashes2
    
    if overlap_hashes:
        # Find which files have overlapping hashes
        for hash_val in overlap_hashes:
            file1 = [k for k, v in set1.items() if v == hash_val][0]
            file2 = [k for k, v in set2.items() if v == hash_val][0]
            print(f"  DUPLICATE FOUND: {name1}/{file1} == {name2}/{file2}")
        return len(overlap_hashes)
    else:
        print(f"  {name1} vs {name2}: No duplicates")
        return 0

train_val_dup = check_overlap(train_images, val_images, "TRAIN", "VAL")
train_test_dup = check_overlap(train_images, test_images, "TRAIN", "TEST")
val_test_dup = check_overlap(val_images, test_images, "VAL", "TEST")

print(f"\n[RESULTS]")
print(f"  Train-Val duplicates: {train_val_dup}")
print(f"  Train-Test duplicates: {train_test_dup}")
print(f"  Val-Test duplicates: {val_test_dup}")

if train_val_dup + train_test_dup + val_test_dup == 0:
    print(f"\n[OK] No data leakage detected!")
else:
    print(f"\n[WARNING] Data leakage detected!")

# Check class distribution
print("\n[3] Class distribution check...")
for class_name in ['Acne', 'Eczema', 'Melanoma', 'Psoriasis']:
    train_count = len(list((train_dir / class_name).glob("*.jpg")))
    val_count = len(list((val_dir / class_name).glob("*.jpg")))
    test_count = len(list((test_dir / class_name).glob("*.jpg")))
    print(f"  {class_name}: Train={train_count}, Val={val_count}, Test={test_count}")
