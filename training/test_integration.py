"""
AI Plant Disease Detection - Step 6 Integration Verification Script
Tests Django view, upload pipeline, AI predictor, and HTML response rendering.
"""

import os
import sys
import django
from pathlib import Path
from io import BytesIO
from PIL import Image

# Setup Django Environment
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plant_disease_project.settings")
django.setup()

from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from detector.ai.predictor import get_predictor, predict_disease


def run_integration_tests():
    print("=" * 60)
    print("   AI PLANT DISEASE DETECTION - STEP 6 INTEGRATION TESTS")
    print("=" * 60)

    # 1. Test Predictor Initialization
    print("\n[Test 1] Testing Predictor Service Initialization...")
    predictor = get_predictor()
    predictor.initialize()
    assert predictor.is_ready, "Predictor should be ready after initialization"
    print("  -> Predictor initialized successfully (Model + Class Mapping ready).")

    # 2. Test Real Disease Sample: Apple Scab
    print("\n[Test 2] Testing Inference on Real Test Image (Apple Scab)...")
    apple_scab_files = list((BASE_DIR / "datasets" / "processed" / "test" / "Apple___Apple_Scab").glob("*.jpg"))
    assert len(apple_scab_files) > 0, "Apple Scab test images must exist"
    res1 = predict_disease(apple_scab_files[0])
    print(f"  -> File: {apple_scab_files[0].name}")
    print(f"  -> Predicted Disease : {res1['predicted_class']}")
    print(f"  -> Confidence        : {res1['confidence_percent']}%")
    print(f"  -> Status            : {res1['status_message']}")
    assert res1["success"] is True, "Inference should succeed"
    assert "Apple" in res1["predicted_class"], "Should detect Apple class"

    # 3. Test Real Disease Sample: Tomato Late Blight / Early Blight
    print("\n[Test 3] Testing Inference on Different Disease Class (Tomato Late Blight)...")
    tomato_lb_files = list((BASE_DIR / "datasets" / "processed" / "test" / "Tomato___Late_Blight").glob("*.jpg"))
    assert len(tomato_lb_files) > 0, "Tomato Late Blight test images must exist"
    res2 = predict_disease(tomato_lb_files[0])
    print(f"  -> File: {tomato_lb_files[0].name}")
    print(f"  -> Predicted Disease : {res2['predicted_class']}")
    print(f"  -> Confidence        : {res2['confidence_percent']}%")
    print(f"  -> Status            : {res2['status_message']}")
    assert res2["success"] is True
    assert "Tomato" in res2["predicted_class"], "Should detect Tomato class"

    # 4. Test Healthy Leaf Sample: Corn Healthy
    print("\n[Test 4] Testing Inference on Healthy Leaf Sample (Corn Healthy)...")
    corn_healthy_files = list((BASE_DIR / "datasets" / "processed" / "test" / "Corn___Healthy").glob("*.jpg"))
    assert len(corn_healthy_files) > 0, "Corn Healthy test images must exist"
    res3 = predict_disease(corn_healthy_files[0])
    print(f"  -> File: {corn_healthy_files[0].name}")
    print(f"  -> Predicted Disease : {res3['predicted_class']}")
    print(f"  -> Confidence        : {res3['confidence_percent']}%")
    print(f"  -> Status            : {res3['status_message']}")
    assert res3["success"] is True
    assert "Corn" in res3["predicted_class"], "Should detect Corn class"

    # 5. Test Django Web View POST Upload Flow
    print("\n[Test 5] Testing End-To-End Django Client HTTP POST Upload...")
    client = Client()
    
    with open(apple_scab_files[0], "rb") as f:
        uploaded_file = SimpleUploadedFile(
            name="test_leaf_upload.jpg",
            content=f.read(),
            content_type="image/jpeg"
        )
    
    response = client.post("/", {"image": uploaded_file}, follow=True)
    print(f"  -> HTTP Response Status: {response.status_code}")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    
    response_content = response.content.decode("utf-8")
    assert "prediction-result-box" in response_content, "Response HTML must contain prediction-result-box"
    assert "Detected Disease" in response_content, "Response HTML must contain Detected Disease label"
    assert "Model Confidence" in response_content, "Response HTML must contain Model Confidence"
    print("  -> Prediction UI HTML successfully rendered in Django response.")

    # 6. Test Invalid / Corrupted File Handling
    print("\n[Test 6] Testing Invalid/Corrupted File Rejection...")
    invalid_file = SimpleUploadedFile(
        name="malicious_payload.exe",
        content=b"MZ\x90\x00\x03\x00\x00\x00Not an image",
        content_type="application/octet-stream"
    )
    res_invalid = client.post("/", {"image": invalid_file}, follow=True)
    assert res_invalid.status_code == 200
    invalid_content = res_invalid.content.decode("utf-8")
    assert "prediction-result-box" not in invalid_content, "Invalid file must not trigger prediction result"
    print("  -> Invalid file safely rejected with validation error message.")

    print("\n" + "=" * 60)
    print("      ALL STEP 6 INTEGRATION TESTS PASSED SUCCESSFULLY")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_integration_tests()
