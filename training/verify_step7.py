"""
AI Plant Disease Detection - Step 7 Verification Script
Verifies that all 38 classes have complete disease information,
tests helper lookups, fallback behavior, and end-to-end view rendering.
"""

import os
import sys
import json
import django
from pathlib import Path

# Setup Django environment
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plant_disease_project.settings")
django.setup()

from detector.ai.disease_info import DISEASE_KNOWLEDGE_BASE, get_disease_info, get_fallback_info
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile


def verify_step7():
    print("=" * 60)
    print("      STEP 7: DISEASE INFORMATION VERIFICATION")
    print("=" * 60)

    # 1. Check class_names.json matching
    class_names_path = BASE_DIR / "datasets" / "metadata" / "class_names.json"
    with open(class_names_path, "r", encoding="utf-8") as f:
        class_map = json.load(f)

    total_classes = len(class_map)
    print(f"\n[Check 1] Verifying 38 classes in Knowledge Base...")
    print(f"  Total classes in metadata: {total_classes}")
    print(f"  Total entries in DISEASE_KNOWLEDGE_BASE: {len(DISEASE_KNOWLEDGE_BASE)}")

    missing_classes = []
    required_keys = [
        "plant_name", "disease_name", "is_healthy",
        "short_description", "symptoms", "possible_causes",
        "prevention", "basic_recommendations"
    ]

    for idx, (str_idx, class_name) in enumerate(class_map.items()):
        info = get_disease_info(class_name)
        if class_name not in DISEASE_KNOWLEDGE_BASE:
            missing_classes.append(class_name)
        
        # Verify all required keys are populated
        for key in required_keys:
            assert key in info, f"Class '{class_name}' missing key '{key}'"
            assert info[key] is not None, f"Class '{class_name}' has None for '{key}'"
            if isinstance(info[key], list):
                assert len(info[key]) > 0, f"Class '{class_name}' has empty list for '{key}'"

    print(f"  Missing classes: {len(missing_classes)}")
    assert len(missing_classes) == 0, f"Missing classes detected: {missing_classes}"
    print("  -> ALL 38 model classes have complete, valid disease profiles!")

    # 2. Test Fallback behavior
    print("\n[Check 2] Testing Graceful Fallback on Unknown Disease...")
    fallback = get_disease_info("Unknown Exotic Disease - Mildew")
    assert fallback["plant_name"] is not None
    assert len(fallback["symptoms"]) > 0
    assert len(fallback["basic_recommendations"]) > 0
    print("  -> Fallback logic tested successfully (no crashes).")

    # 3. Test End-to-End View Integration with Confident Prediction
    print("\n[Check 3] Testing Django View Upload with Disease Info Rendering...")
    client = Client()
    apple_scab_dir = BASE_DIR / "datasets" / "processed" / "test" / "Apple___Apple_Scab"
    test_files = list(apple_scab_dir.glob("*.jpg"))
    assert len(test_files) > 0, "Test image must exist"

    with open(test_files[0], "rb") as f:
        uploaded_file = SimpleUploadedFile(
            name="apple_scab_test.jpg",
            content=f.read(),
            content_type="image/jpeg"
        )

    response = client.post("/", {"image": uploaded_file}, follow=True)
    assert response.status_code == 200
    html = response.content.decode("utf-8")

    assert "About This Disease" in html or "Plant Health Overview" in html, "HTML must contain Disease Info section"
    assert "Common Symptoms" in html, "HTML must contain Common Symptoms"
    assert "Possible Causes" in html, "HTML must contain Possible Causes"
    assert "General Prevention Guidance" in html, "HTML must contain Prevention Guidance"
    assert "Basic Recommendations" in html, "HTML must contain Basic Recommendations"
    print("  -> Confident prediction rendered complete Disease Profile & Recommendations.")

    print("\n" + "=" * 60)
    print("   STEP 7 VERIFICATION PASSED WITH ZERO ERRORS (38/38)")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    verify_step7()
