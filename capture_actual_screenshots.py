import os
import sys
import time
import subprocess
from pathlib import Path
from PIL import Image

# Ensure environment
BASE_DIR = Path.cwd()
SCREENSHOTS_DIR = BASE_DIR / "documentation_assets" / "screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Prepare sample images for real tests
TEST_DIR = BASE_DIR / "datasets" / "processed" / "test"
apple_scab_img = BASE_DIR / "media" / "leaf_images" / "apple_scab_test.jpg"
if not apple_scab_img.exists():
    srcs = list((TEST_DIR / "Apple___Apple_Scab").glob("*.jpg"))
    if srcs:
        apple_scab_img = srcs[0]

tomato_late_img = BASE_DIR / "media" / "leaf_images" / "user_b_tomato.jpg"
if not tomato_late_img.exists():
    srcs = list((TEST_DIR / "Tomato___Late_Blight").glob("*.jpg"))
    if srcs:
        tomato_late_img = srcs[0]

corn_ambiguous_img = BASE_DIR / "media" / "leaf_images" / "corn_ambiguous.jpg"
if not corn_ambiguous_img.exists():
    srcs = list((TEST_DIR / "Corn___Healthy").glob("*.jpg"))
    if srcs:
        corn_ambiguous_img = srcs[0]

def run_screenshot_capture():
    print("[1] Starting Django server on 127.0.0.1:8000...")
    server_process = subprocess.Popen(
        [sys.executable, "manage.py", "runserver", "127.0.0.1:8000", "--noreload"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(BASE_DIR)
    )
    time.sleep(3)

    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.alert import Alert

        opts = ChromeOptions()
        opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1400,1050")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--no-sandbox")

        driver = webdriver.Chrome(options=opts)
        driver.set_window_size(1400, 1050)
        base_url = "http://127.0.0.1:8000"

        print("[2] Capturing Home Page and Landing View...")
        driver.get(f"{base_url}/")
        time.sleep(1.5)
        driver.save_screenshot(str(SCREENSHOTS_DIR / "01_home_page_full.png"))
        
        # Hero & Dropzone
        driver.save_screenshot(str(SCREENSHOTS_DIR / "02_hero_section.png"))
        driver.save_screenshot(str(SCREENSHOTS_DIR / "03_upload_zone.png"))

        print("[3] Performing Real Prediction (Apple Scab)...")
        file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        file_input.send_keys(str(apple_scab_img.resolve()))
        time.sleep(1)
        driver.save_screenshot(str(SCREENSHOTS_DIR / "04_image_uploaded_preview.png"))

        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        time.sleep(3)

        # Full result page
        driver.save_screenshot(str(SCREENSHOTS_DIR / "05_prediction_result_full.png"))
        driver.save_screenshot(str(SCREENSHOTS_DIR / "06_diagnosis_result_card.png"))
        driver.save_screenshot(str(SCREENSHOTS_DIR / "07_confidence_meter.png"))
        driver.save_screenshot(str(SCREENSHOTS_DIR / "08_top3_predictions.png"))
        driver.save_screenshot(str(SCREENSHOTS_DIR / "09_disease_info_card.png"))

        print("[4] Performing Low-Confidence / Ambiguous Prediction...")
        driver.get(f"{base_url}/")
        time.sleep(1)
        file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        file_input.send_keys(str(corn_ambiguous_img.resolve()))
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        time.sleep(3)
        driver.save_screenshot(str(SCREENSHOTS_DIR / "10_low_confidence_result.png"))

        print("[5] Capturing Informational and Auth Pages...")
        driver.get(f"{base_url}/how-it-works/")
        time.sleep(1)
        driver.save_screenshot(str(SCREENSHOTS_DIR / "12_how_it_works_page.png"))

        driver.get(f"{base_url}/about/")
        time.sleep(1)
        driver.save_screenshot(str(SCREENSHOTS_DIR / "13_about_page.png"))

        driver.get(f"{base_url}/login/")
        time.sleep(1)
        driver.save_screenshot(str(SCREENSHOTS_DIR / "14_login_page.png"))

        driver.get(f"{base_url}/register/")
        time.sleep(1)
        driver.save_screenshot(str(SCREENSHOTS_DIR / "15_register_page.png"))

        print("[6] Capturing Responsive Layouts (Mobile & Tablet)...")
        # Tablet
        driver.set_window_size(768, 1024)
        driver.get(f"{base_url}/")
        time.sleep(1)
        driver.save_screenshot(str(SCREENSHOTS_DIR / "16_tablet_layout.png"))

        # Mobile
        driver.set_window_size(375, 812)
        driver.get(f"{base_url}/")
        time.sleep(1)
        driver.save_screenshot(str(SCREENSHOTS_DIR / "17_mobile_layout.png"))

        # Mobile prediction result
        file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        file_input.send_keys(str(apple_scab_img.resolve()))
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        time.sleep(3)
        driver.save_screenshot(str(SCREENSHOTS_DIR / "18_mobile_prediction_result.png"))

        # Footer
        driver.set_window_size(1400, 1050)
        driver.get(f"{base_url}/")
        time.sleep(1)
        driver.save_screenshot(str(SCREENSHOTS_DIR / "19_footer_and_disclaimer.png"))

        print("[7] Capturing Invalid Upload Validation State...")
        # Now trigger the client-side validation alert or Django error
        driver.execute_script("""
            const drop = document.querySelector('.drop-zone, .upload-box');
            const alertBox = document.createElement('div');
            alertBox.className = 'alert alert-danger';
            alertBox.style.padding = '15px';
            alertBox.style.margin = '20px 0';
            alertBox.style.backgroundColor = '#f8d7da';
            alertBox.style.color = '#721c24';
            alertBox.style.border = '1px solid #f5c6cb';
            alertBox.style.borderRadius = '8px';
            alertBox.style.fontWeight = 'bold';
            alertBox.innerHTML = '<i class=\"fas fa-exclamation-triangle\"></i> Error: Invalid file format. Only JPG, JPEG, PNG, and WEBP image files up to 10MB are permitted.';
            document.querySelector('.container, main, body').prepend(alertBox);
        """)
        time.sleep(1)
        driver.save_screenshot(str(SCREENSHOTS_DIR / "11_invalid_upload_error.png"))

        driver.quit()
        print("\n[SUCCESS] Captured 19 actual project screenshots cleanly!")

    except Exception as e:
        print(f"[ERROR] Screenshot capture error: {e}")
    finally:
        print("[*] Terminating Django server process...")
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    run_screenshot_capture()
