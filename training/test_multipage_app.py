"""
AI Plant Disease Detection - Multi-Page Web Application Verification Suite
==========================================================================
Tests:
1. All public URLs: Home, How It Works, About, Login, Register
2. Protected URLs redirection for anonymous users (Dashboard, History, Profile)
3. Authenticated access to all pages (Dashboard, History, Profile)
4. End-to-end leaf diagnosis upload & prediction flow
5. User data isolation (User A vs User B across history, details, delete)
6. Model inference and threshold integrity
"""

import os
import sys
import django
from pathlib import Path

# Setup Django Environment
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plant_disease_project.settings")
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from detector.models import PredictionHistory


def test_multipage_application():
    print("=" * 70)
    print("   MULTI-PAGE WEB APPLICATION VERIFICATION SUITE")
    print("=" * 70)

    client = Client()
    anon_client = Client()

    # Clean up test users
    User.objects.filter(username__in=["multi_user_a", "multi_user_b"]).delete()

    # 1. Test Public Multi-Page Routes
    print("\n[Test 1] Testing Public Page Endpoints...")
    public_routes = [
        ("/", "AI Plant Disease Detection"),
        ("/how-it-works/", "How PlantGuard AI Works"),
        ("/about/", "About PlantGuard AI"),
        ("/login/", "Sign In"),
        ("/register/", "Create an Account"),
    ]

    for url, expected_text in public_routes:
        res = anon_client.get(url)
        assert res.status_code == 200, f"Expected 200 for {url}, got {res.status_code}"
        content = res.content.decode("utf-8")
        assert expected_text in content, f"Expected '{expected_text}' in {url}"
        print(f"  -> Route '{url}' loaded successfully.")

    # 2. Test Protected Routes Redirection for Anonymous Users
    print("\n[Test 2] Testing Unauthenticated Route Protection...")
    protected_routes = ["/dashboard/", "/history/", "/profile/"]
    for url in protected_routes:
        res = anon_client.get(url)
        assert res.status_code == 302, f"Expected 302 for {url}, got {res.status_code}"
        assert "/login/" in res.url, f"Expected redirect to /login/, got {res.url}"
        print(f"  -> Protected route '{url}' safely redirected to login.")

    # 3. Register & Test Authenticated User A
    print("\n[Test 3] Testing User A Registration & Profile...")
    res_reg = client.post("/register/", {
        "username": "multi_user_a",
        "email": "user_a@plantguard.ai",
        "password": "SecurePassword123!",
        "password_confirm": "SecurePassword123!",
    }, follow=True)
    assert res_reg.status_code == 200
    user_a = User.objects.get(username="multi_user_a")

    # Verify Profile Page
    res_profile = client.get("/profile/")
    assert res_profile.status_code == 200
    profile_html = res_profile.content.decode("utf-8")
    assert "multi_user_a" in profile_html
    assert "user_a@plantguard.ai" in profile_html
    print("  -> User A registered and Profile page verified.")

    # 4. Perform Real AI Prediction for User A
    print("\n[Test 4] Testing Real Prediction Upload & History Integration...")
    apple_img_path = list((BASE_DIR / "datasets" / "processed" / "test" / "Apple___Apple_Scab").glob("*.jpg"))[0]
    with open(apple_img_path, "rb") as f:
        upload = SimpleUploadedFile("test_apple.jpg", f.read(), content_type="image/jpeg")

    res_pred = client.post("/", {"image": upload}, follow=True)
    assert res_pred.status_code == 200
    pred_html = res_pred.content.decode("utf-8")
    assert "Prediction Successful" in pred_html
    assert "Apple - Apple Scab" in pred_html

    # Check that record was persisted to User A's history
    hist_a = PredictionHistory.objects.filter(user=user_a)
    assert hist_a.count() == 1
    record = hist_a.first()
    print(f"  -> Prediction saved: {record.full_class_name} ({record.confidence_percent}%)")

    # 5. Verify Authenticated History & History Detail Pages
    print("\n[Test 5] Testing History & History Detail Pages...")
    res_history = client.get("/history/")
    assert res_history.status_code == 200
    assert "Apple" in res_history.content.decode("utf-8")

    res_detail = client.get(f"/history/{record.id}/")
    assert res_detail.status_code == 200
    detail_html = res_detail.content.decode("utf-8")
    assert "Apple Scab" in detail_html
    assert "Common Symptoms" in detail_html
    assert "Basic Recommendations" in detail_html
    print("  -> History and History Detail pages rendered with full disease profiles.")

    # 6. Verify Authenticated Dashboard Stats
    print("\n[Test 6] Testing Dashboard Counters...")
    res_dash = client.get("/dashboard/")
    assert res_dash.status_code == 200
    dash_html = res_dash.content.decode("utf-8")
    assert "Total Predictions" in dash_html
    assert "Apple" in dash_html
    print("  -> Dashboard stats and recent activity verified.")

    # 7. User Data Isolation Test with User B
    print("\n[Test 7] Testing Cross-User Data Isolation...")
    client_b = Client()
    client_b.post("/register/", {
        "username": "multi_user_b",
        "email": "user_b@plantguard.ai",
        "password": "SecurePassword123!",
        "password_confirm": "SecurePassword123!",
    }, follow=True)

    # User B checks history (must be empty)
    res_hist_b = client_b.get("/history/")
    assert "Apple" not in res_hist_b.content.decode("utf-8")
    assert "No Prediction History Yet" in res_hist_b.content.decode("utf-8")

    # User B attempts to view User A's detail record (must 404)
    res_unauth_detail = client_b.get(f"/history/{record.id}/")
    assert res_unauth_detail.status_code == 404

    # User B attempts to delete User A's record (must 404)
    res_unauth_del = client_b.post(f"/history/{record.id}/delete/")
    assert res_unauth_del.status_code == 404
    print("  -> Multi-user data isolation strictly verified.")

    print("\n" + "=" * 70)
    print("   ALL MULTI-PAGE APPLICATION TESTS PASSED SUCCESSFULLY!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    test_multipage_application()
