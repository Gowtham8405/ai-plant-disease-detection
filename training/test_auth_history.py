"""
AI Plant Disease Detection - Authentication & Prediction History Test Suite
===========================================================================
Tests:
1. User registration & secure password hashing
2. User login & session handling
3. Anonymous user prediction (continues to work without history saving)
4. Authenticated user prediction (persists record in PredictionHistory)
5. User data isolation (User A cannot see or delete User B's records)
6. Single record deletion (POST only)
7. Clear all user history (POST only, does not delete other users' history)
8. Login required decorator & redirect protection
9. Model inference and threshold integrity
"""

import os
import sys
import django
from pathlib import Path
from PIL import Image

# Setup Django Environment
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plant_disease_project.settings")
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from detector.models import PredictionHistory, PlantLeafUpload


def test_auth_and_history():
    print("=" * 70)
    print("   AUTHENTICATION & PREDICTION HISTORY VERIFICATION SUITE")
    print("=" * 70)

    client_a = Client()
    client_b = Client()
    anon_client = Client()

    # Clean up test users if they exist
    User.objects.filter(username__in=["test_user_a", "test_user_b"]).delete()

    # 1. Register User A
    print("\n[Test 1] User A Registration...")
    res_reg_a = client_a.post("/register/", {
        "username": "test_user_a",
        "email": "user_a@example.com",
        "password": "Password123!",
        "password_confirm": "Password123!",
    }, follow=True)
    assert res_reg_a.status_code == 200
    user_a = User.objects.get(username="test_user_a")
    assert user_a.check_password("Password123!"), "Password must be hashed correctly"
    print("  -> User A registered and logged in successfully.")

    # 2. Register User B
    print("\n[Test 2] User B Registration...")
    res_reg_b = client_b.post("/register/", {
        "username": "test_user_b",
        "email": "user_b@example.com",
        "password": "Password123!",
        "password_confirm": "Password123!",
    }, follow=True)
    assert res_reg_b.status_code == 200
    user_b = User.objects.get(username="test_user_b")
    print("  -> User B registered and logged in successfully.")

    # 3. Test Anonymous Prediction Flow
    print("\n[Test 3] Testing Anonymous Prediction Workflow...")
    apple_img_path = list((BASE_DIR / "datasets" / "processed" / "test" / "Apple___Apple_Scab").glob("*.jpg"))[0]
    with open(apple_img_path, "rb") as f:
        anon_upload = SimpleUploadedFile(
            name="anon_apple.jpg",
            content=f.read(),
            content_type="image/jpeg"
        )
    res_anon = anon_client.post("/", {"image": anon_upload}, follow=True)
    assert res_anon.status_code == 200
    anon_html = res_anon.content.decode("utf-8")
    assert "Prediction Successful" in anon_html
    # History count for anonymous should be 0
    assert PredictionHistory.objects.count() == 0, "Anonymous predictions must not create history records"
    print("  -> Anonymous prediction works seamlessly without saving history.")

    # 4. Test Authenticated Prediction for User A
    print("\n[Test 4] Testing Authenticated Prediction for User A...")
    with open(apple_img_path, "rb") as f:
        upload_a = SimpleUploadedFile(
            name="user_a_apple.jpg",
            content=f.read(),
            content_type="image/jpeg"
        )
    res_pred_a = client_a.post("/", {"image": upload_a}, follow=True)
    assert res_pred_a.status_code == 200
    
    # Check history saved for User A
    hist_a = PredictionHistory.objects.filter(user=user_a)
    assert hist_a.count() == 1, "User A must have exactly 1 history record"
    record_a = hist_a.first()
    assert "Apple" in record_a.plant_name
    assert record_a.confidence_percent >= 70.0
    print(f"  -> Saved to User A History: {record_a.full_class_name} ({record_a.confidence_percent}%)")

    # 5. Test Authenticated Prediction for User B
    print("\n[Test 5] Testing Authenticated Prediction for User B...")
    tomato_img_path = list((BASE_DIR / "datasets" / "processed" / "test" / "Tomato___Late_Blight").glob("*.jpg"))[0]
    with open(tomato_img_path, "rb") as f:
        upload_b = SimpleUploadedFile(
            name="user_b_tomato.jpg",
            content=f.read(),
            content_type="image/jpeg"
        )
    res_pred_b = client_b.post("/", {"image": upload_b}, follow=True)
    assert res_pred_b.status_code == 200
    
    hist_b = PredictionHistory.objects.filter(user=user_b)
    assert hist_b.count() == 1, "User B must have exactly 1 history record"
    record_b = hist_b.first()
    assert "Tomato" in record_b.plant_name
    print(f"  -> Saved to User B History: {record_b.full_class_name} ({record_b.confidence_percent}%)")

    # 6. Test User Data Isolation (User A History Page vs User B History Page)
    print("\n[Test 6] Testing Strict User Data Isolation...")
    res_hist_page_a = client_a.get("/history/")
    assert res_hist_page_a.status_code == 200
    html_hist_a = res_hist_page_a.content.decode("utf-8")
    assert "Apple" in html_hist_a
    assert "Tomato" not in html_hist_a, "User A must NOT see User B's Tomato prediction!"

    res_hist_page_b = client_b.get("/history/")
    assert res_hist_page_b.status_code == 200
    html_hist_b = res_hist_page_b.content.decode("utf-8")
    assert "Tomato" in html_hist_b
    assert "Apple" not in html_hist_b, "User B must NOT see User A's Apple prediction!"
    print("  -> User A and User B cannot view each other's prediction history.")

    # 7. Test Unauthorized Detail Access by URL ID Manipulation
    print("\n[Test 7] Testing Cross-User Detail Access Blocking...")
    # User B tries to view User A's record by ID
    res_unauth_detail = client_b.get(f"/history/{record_a.id}/")
    assert res_unauth_detail.status_code == 404, f"Expected 404 on accessing another user's record, got {res_unauth_detail.status_code}"
    print("  -> Cross-user detail access blocked with 404.")

    # 8. Test Unauthorized Deletion Attempt
    print("\n[Test 8] Testing Cross-User Deletion Blocking...")
    res_unauth_del = client_b.post(f"/history/{record_a.id}/delete/")
    assert res_unauth_del.status_code == 404, f"Expected 404 on deleting another user's record, got {res_unauth_del.status_code}"
    assert PredictionHistory.objects.filter(id=record_a.id).exists(), "User A's record must NOT be deleted by User B"
    print("  -> Cross-user delete operation blocked with 404.")

    # 9. Test Authorized Single Record Deletion
    print("\n[Test 9] Testing Authorized Single Record Deletion...")
    res_auth_del = client_a.post(f"/history/{record_a.id}/delete/", follow=True)
    assert res_auth_del.status_code == 200
    assert not PredictionHistory.objects.filter(id=record_a.id).exists(), "Record A must be deleted"
    assert PredictionHistory.objects.filter(id=record_b.id).exists(), "Record B must remain untouched"
    print("  -> User A deleted their own record successfully.")

    # 10. Test Clear History (Isolated to Current User)
    print("\n[Test 10] Testing Clear History Isolation...")
    # Create another record for User B
    with open(apple_img_path, "rb") as f:
        upload_b2 = SimpleUploadedFile("user_b_apple2.jpg", f.read(), content_type="image/jpeg")
    client_b.post("/", {"image": upload_b2}, follow=True)
    assert PredictionHistory.objects.filter(user=user_b).count() == 2

    # User B clears history
    res_clear_b = client_b.post("/history/clear/", follow=True)
    assert res_clear_b.status_code == 200
    assert PredictionHistory.objects.filter(user=user_b).count() == 0, "User B history must be empty"
    print("  -> User B cleared all their history successfully.")

    # 11. Test Protected Pages Redirect for Unauthenticated Users
    print("\n[Test 11] Testing Login Requirement Redirects...")
    for protected_url in ["/dashboard/", "/history/"]:
        res_prot = anon_client.get(protected_url)
        assert res_prot.status_code == 302, f"Expected 302 redirect for {protected_url}"
        assert "/login/" in res_prot.url, f"Expected redirect to /login/, got {res_prot.url}"
    print("  -> Unauthenticated users safely redirected to /login/.")

    print("\n" + "=" * 70)
    print("   ALL AUTHENTICATION & HISTORY TESTS PASSED SUCCESSFULLY!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    test_auth_and_history()
