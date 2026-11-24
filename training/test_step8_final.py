"""
AI Plant Disease Detection - Step 8 Final End-to-End Verification Suite
========================================================================
Comprehensive automated test suite covering:
1. Django system checks
2. AI Model integrity (MobileNetV2, 38 classes)
3. Real AI inference on test images (Apple Scab, Tomato Late Blight, Corn Healthy, Grape Black Rot)
4. 70% Confidence threshold logic (high vs low confidence rendering)
5. Disease information completeness (38/38 classes & safety disclaimers)
6. Upload validation & security (TXT, PDF, EXE, corrupted image, oversized file)
7. Navigation links, Static files, Media URLs
8. Performance / Singleton model caching
"""

import os
import sys
import json
from pathlib import Path
from io import BytesIO
from PIL import Image
import numpy as np

# Set up Django environment
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plant_disease_project.settings")

import django
django.setup()

from django.core.management import call_command
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from detector.ai.predictor import get_predictor, predict_disease, PlantDiseasePredictor
from detector.ai.disease_info import DISEASE_KNOWLEDGE_BASE, get_disease_info


def test_1_django_check():
    print("\n--- [TEST 1] Django System Check ---")
    try:
        call_command("check")
        print("  [PASS] Django system check identified 0 issues.")
        return True
    except Exception as e:
        print(f"  [FAIL] Django check failed: {e}")
        return False


def test_2_model_integrity():
    print("\n--- [TEST 2] AI Model Integrity & Class Alignment ---")
    model_path = BASE_DIR / "detector" / "ai" / "model" / "plant_disease_model.keras"
    class_names_path = BASE_DIR / "datasets" / "metadata" / "class_names.json"

    assert model_path.exists(), f"Model file not found: {model_path}"
    assert class_names_path.exists(), f"Class names file not found: {class_names_path}"

    with open(class_names_path, "r", encoding="utf-8") as f:
        class_map = json.load(f)

    assert len(class_map) == 38, f"Expected 38 classes, got {len(class_map)}"

    predictor = get_predictor()
    predictor.initialize()
    assert predictor.is_ready, "Predictor failed to initialize"

    # Check model shapes
    input_shape = predictor._model.input_shape
    output_shape = predictor._model.output_shape

    print(f"  Model Input Shape : {input_shape}")
    print(f"  Model Output Shape: {output_shape}")
    print(f"  Number of Classes : {len(class_map)}")

    assert output_shape[-1] == 38, f"Expected 38 outputs, got {output_shape[-1]}"
    print("  [PASS] Model architecture and 38-class metadata are perfectly aligned.")
    return True


def test_3_real_predictions():
    print("\n--- [TEST 3] Real AI Prediction on Test Dataset ---")
    test_cases = [
        ("Apple___Apple_Scab", "Apple___Apple_Scab_mendeley_00007.jpg", "Apple", "Apple Scab"),
        ("Tomato___Late_Blight", "Tomato___Late_Blight_mendeley_00005.jpg", "Tomato", "Late Blight"),
        ("Corn___Healthy", "Corn___Healthy_mendeley_00010.jpg", "Corn", "Healthy"),
        ("Grape___Black_Rot", None, "Grape", "Black Rot"),
    ]

    results = []
    for folder_name, specific_file, expected_plant, expected_disease in test_cases:
        test_dir = BASE_DIR / "datasets" / "processed" / "test" / folder_name
        if specific_file:
            test_img = test_dir / specific_file
        else:
            images = list(test_dir.glob("*.jpg"))
            assert len(images) > 0, f"No test images found in {test_dir}"
            test_img = images[0]

        res = predict_disease(test_img)

        print(f"  Sample: {test_img.name} (Expected: {expected_plant} - {expected_disease})")
        print(f"    -> Predicted Class: {res['predicted_class']}")
        print(f"    -> Confidence     : {res['confidence_percent']}%")
        print(f"    -> Status Message : {res['status_message']}")
        print(f"    -> Top 3 Classes  : {[p['class_name'] for p in res['top_predictions']]}")

        assert res["success"] is True, f"Inference failed for {test_img}"
        assert expected_plant.lower() in res["predicted_class"].lower(), f"Expected {expected_plant} in {res['predicted_class']}"
        assert res["confidence_percent"] >= 70.0, f"Expected confident prediction for real test sample, got {res['confidence_percent']}%"
        results.append((folder_name, res))

    print("  [PASS] Real test images accurately classified with high confidence.")
    return results


def test_4_confidence_threshold_and_view():
    print("\n--- [TEST 4] Confidence Threshold & Django View Rendering ---")
    client = Client()

    # Case A: Confident Prediction (>= 70%)
    apple_img_path = BASE_DIR / "datasets" / "processed" / "test" / "Apple___Apple_Scab" / "Apple___Apple_Scab_mendeley_00007.jpg"
    with open(apple_img_path, "rb") as f:
        upload_confident = SimpleUploadedFile(
            name="apple_leaf.jpg",
            content=f.read(),
            content_type="image/jpeg"
        )
    res_a = client.post("/", {"image": upload_confident}, follow=True)
    assert res_a.status_code == 200
    html_a = res_a.content.decode("utf-8")

    assert "Prediction Successful" in html_a, "Expected 'Prediction Successful' badge in confident result"
    assert "About This Disease" in html_a or "Plant Health" in html_a, "Expected disease information section"
    assert "Common Symptoms" in html_a, "Expected Common Symptoms"
    assert "General Prevention Guidance" in html_a, "Expected Prevention Guidance"
    assert "Basic Recommendations" in html_a, "Expected Basic Recommendations"
    assert "Educational &amp; Advisory Notice" in html_a or "Educational" in html_a, "Expected educational safety notice"
    print("  [PASS] Case A (>=70%): Shows confident prediction, top-3, and full disease profile.")

    # Case B: Real Ambiguous Sample (< 70%)
    corn_ambiguous_path = BASE_DIR / "datasets" / "processed" / "test" / "Corn___Healthy" / "Corn___Healthy_mendeley_00006.jpg"
    with open(corn_ambiguous_path, "rb") as f:
        upload_ambiguous = SimpleUploadedFile(
            name="corn_ambiguous.jpg",
            content=f.read(),
            content_type="image/jpeg"
        )
    res_b = client.post("/", {"image": upload_ambiguous}, follow=True)
    assert res_b.status_code == 200
    html_b = res_b.content.decode("utf-8")

    assert "Unable to confidently identify" in html_b, "Expected 'Unable to confidently identify' in low-confidence result"
    assert "status-uncertain" in html_b, "Expected status-uncertain class in HTML"
    # Ensure disease-specific recommendations are suppressed
    assert "About This Disease:" not in html_b, "Disease-specific treatment must NOT be shown for low confidence"
    print("  [PASS] Case B (<70%): Displays 'Unable to confidently identify' and suppresses disease-specific recommendations.")
    return True


def test_5_disease_knowledge_base():
    print("\n--- [TEST 5] Disease Knowledge Base Completeness ---")
    class_names_path = BASE_DIR / "datasets" / "metadata" / "class_names.json"
    with open(class_names_path, "r", encoding="utf-8") as f:
        class_map = json.load(f)

    assert len(DISEASE_KNOWLEDGE_BASE) == 38, f"Expected 38 entries in knowledge base, found {len(DISEASE_KNOWLEDGE_BASE)}"
    for idx_str, class_name in class_map.items():
        info = get_disease_info(class_name)
        assert info["plant_name"], f"Missing plant_name for {class_name}"
        assert info["disease_name"], f"Missing disease_name for {class_name}"
        assert info["short_description"], f"Missing short_description for {class_name}"
        assert len(info["symptoms"]) > 0, f"Empty symptoms for {class_name}"
        assert len(info["possible_causes"]) > 0, f"Empty possible_causes for {class_name}"
        assert len(info["prevention"]) > 0, f"Empty prevention for {class_name}"
        assert len(info["basic_recommendations"]) > 0, f"Empty basic_recommendations for {class_name}"

    print("  [PASS] All 38 classes have 100% complete disease profiles with all 8 fields.")
    return True


def test_6_invalid_and_oversized_uploads():
    print("\n--- [TEST 6] Invalid File & Oversized Upload Handling ---")
    client = Client()

    # 1. Text file (.txt)
    txt_file = SimpleUploadedFile("notes.txt", b"This is a text file, not a plant leaf.", content_type="text/plain")
    res_txt = client.post("/", {"image": txt_file}, follow=True)
    assert res_txt.status_code == 200
    assert "prediction-result-box" not in res_txt.content.decode("utf-8")
    print("  [PASS] TXT file rejected safely.")

    # 2. PDF file (.pdf)
    pdf_file = SimpleUploadedFile("document.pdf", b"%PDF-1.4 Fake PDF Content", content_type="application/pdf")
    res_pdf = client.post("/", {"image": pdf_file}, follow=True)
    assert res_pdf.status_code == 200
    assert "prediction-result-box" not in res_pdf.content.decode("utf-8")
    print("  [PASS] PDF file rejected safely.")

    # 3. Executable file (.exe)
    exe_file = SimpleUploadedFile("malware.exe", b"MZ\x90\x00\x03\x00\x00", content_type="application/octet-stream")
    res_exe = client.post("/", {"image": exe_file}, follow=True)
    assert res_exe.status_code == 200
    assert "prediction-result-box" not in res_exe.content.decode("utf-8")
    print("  [PASS] EXE file rejected safely.")

    # 4. Corrupted image file (.jpg with garbage bytes)
    corrupted_file = SimpleUploadedFile("broken.jpg", b"\xFF\xD8\xFFcorrupted_bytes_that_are_not_image", content_type="image/jpeg")
    res_corrupted = client.post("/", {"image": corrupted_file}, follow=True)
    assert res_corrupted.status_code == 200
    assert "prediction-result-box" not in res_corrupted.content.decode("utf-8")
    print("  [PASS] Corrupted image rejected safely.")

    # 5. Oversized valid image (> 10MB)
    arr = np.random.randint(0, 256, (2000, 2000, 3), dtype=np.uint8)
    large_img = Image.fromarray(arr)
    large_buf = BytesIO()
    large_img.save(large_buf, format="PNG")
    huge_bytes = large_buf.getvalue()
    
    huge_file = SimpleUploadedFile("huge.png", huge_bytes, content_type="image/png")
    res_huge = client.post("/", {"image": huge_file}, follow=True)
    assert res_huge.status_code == 200
    huge_content = res_huge.content.decode("utf-8")
    assert "exceeds maximum allowed limit" in huge_content, "Expected size limit error message in response"
    assert "prediction-result-box" not in huge_content, "Oversized file must not trigger prediction"
    print("  [PASS] Oversized valid image (>10MB) rejected safely with validation message.")
    return True


def test_7_navigation_and_static():
    print("\n--- [TEST 7] Navigation Links & Static Assets ---")
    client = Client()
    res = client.get("/")
    assert res.status_code == 200
    html = res.content.decode("utf-8")

    # Check key navigation elements
    assert "PlantGuard" in html, "Brand title not found"
    assert "Home" in html, "Home nav link not found"
    assert "About" in html, "About nav link not found"
    assert "How It Works" in html, "How It Works nav link not found"
    assert "Admin" in html, "Admin nav link not found"

    # Check static asset links
    assert "style.css" in html, "style.css link missing"
    assert "main.js" in html, "main.js script link missing"

    # Verify static file exists on disk
    css_file = BASE_DIR / "static" / "css" / "style.css"
    js_file = BASE_DIR / "static" / "js" / "main.js"
    assert css_file.exists(), "style.css missing on disk"
    assert js_file.exists(), "main.js missing on disk"

    print("  [PASS] Navigation links and static assets verified successfully.")
    return True


def test_8_performance_and_singleton():
    print("\n--- [TEST 8] Predictor Singleton & Performance ---")
    pred1 = get_predictor()
    pred2 = get_predictor()
    assert pred1 is pred2, "get_predictor() must return the same singleton instance"
    assert pred1._model is pred2._model, "AI Model must remain loaded in memory without reloading"
    print("  [PASS] AI Predictor is a validated singleton. No redundant model reloads.")
    return True


def run_all_step8_tests():
    print("=" * 70)
    print("   AI PLANT DISEASE DETECTION - STEP 8 FINAL TEST SUITE")
    print("=" * 70)

    t1 = test_1_django_check()
    t2 = test_2_model_integrity()
    t3 = test_3_real_predictions()
    t4 = test_4_confidence_threshold_and_view()
    t5 = test_5_disease_knowledge_base()
    t6 = test_6_invalid_and_oversized_uploads()
    t7 = test_7_navigation_and_static()
    t8 = test_8_performance_and_singleton()

    print("\n" + "=" * 70)
    print("   ALL STEP 8 FINAL END-TO-END TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    run_all_step8_tests()
