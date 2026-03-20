import requests
import json
from pathlib import Path

# Get first test image
test_dir = Path('dataset/Acne')
test_images = list(test_dir.glob('*.jpg'))

if not test_images:
    print("ERROR: No test images found!")
    exit(1)

test_image = test_images[0]

print(f"Testing with image: {test_image.name}")
print(f"Expected class: Acne\n")

# Send prediction request
files = {'image': open(test_image, 'rb')}
response = requests.post('http://127.0.0.1:5000/predict', files=files)

result = response.json()
print("PREDICTION RESULT:")
print(json.dumps(result, indent=2))

# Check if prediction is correct
predicted = result['disease']
confidence = result['confidence']
print(f"\n✓ Predicted: {predicted}")
print(f"✓ Confidence: {confidence:.2%}")

if predicted == 'Acne':
    print("✓ CORRECT PREDICTION!")
else:
    print("✗ Incorrect prediction")

# Test with other classes
print("\n" + "="*60)
print("Testing with other disease classes...")
print("="*60)

for disease in ['Eczema', 'Melanoma', 'Psoriasis']:
    disease_dir = Path(f'dataset/{disease}')
    disease_images = list(disease_dir.glob('*.jpg'))
    if disease_images:
        test_img = disease_images[0]
        files = {'image': open(test_img, 'rb')}
        response = requests.post('http://127.0.0.1:5000/predict', files=files)
        result = response.json()
        pred = result['disease']
        conf = result['confidence']
        status = "✓" if pred == disease else "✗"
        print(f"{status} {disease:15s} -> Predicted: {pred:15s} ({conf:.2%})")
