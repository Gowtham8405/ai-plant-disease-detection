"""
AI Plant Disease Detection - Dataset Downloader & Inspector
===========================================================
This script automatically downloads the reputable and free public
PlantVillage dataset from Mendeley Data (DOI: 10.17632/tywbtsjrjv.1),
extracts it, verifies image integrity, and inspects class statistics.

Usage:
    python training/download_dataset.py
"""

import os
import sys
import time
import json
import zipfile
import urllib.request
import urllib.error
from pathlib import Path

# Try importing tqdm for interactive progress bar; fallback if unavailable
try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False


# =====================================================================
# Configuration & Constants
# =====================================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_ROOT = PROJECT_ROOT / "dataset"
RAW_ZIP_DIR = DATASET_ROOT / "raw"
EXTRACTED_DIR = DATASET_ROOT / "plantvillage"
ZIP_PATH = RAW_ZIP_DIR / "plantvillage_dataset.zip"

# Official Mendeley Data public repository download link for PlantVillage (unaugmented, CC0 1.0)
DATASET_SOURCE_NAME = "PlantVillage Dataset (Mendeley Data Archive)"
DATASET_DOI = "10.17632/tywbtsjrjv.1"
DATASET_URL = "https://data.mendeley.com/public-files/datasets/tywbtsjrjv/files/d5652a28-c1d8-4b76-97f3-72fb80f94efc/file_downloaded"
DATASET_LICENSE = "Creative Commons CC0 1.0 Public Domain Dedication"
VALID_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".JPG", ".JPEG", ".PNG"}


def check_dataset_exists(target_dir: Path) -> bool:
    """
    Checks if the dataset is already extracted and contains valid class folders with images.
    """
    if not target_dir.exists():
        return False

    # Check for presence of image files in subdirectories
    image_count = 0
    for root, _, files in os.walk(target_dir):
        for f in files:
            if Path(f).suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp"}:
                image_count += 1
                if image_count >= 100:  # Confirmed reasonable volume exists
                    return True
    return False


def download_file_with_progress(url: str, destination: Path):
    """
    Downloads a file from a URL to destination path with progress indicators.
    Handles user-agent headers, timeouts, and chunked writing.
    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp_destination = destination.with_suffix(".tmp")

    print(f"\n[INFO] Connecting to dataset repository: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AI-Plant-Disease-Downloader/1.0"
    }
    request = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            total_size = int(response.headers.get("Content-Length", 0))
            block_size = 1024 * 64  # 64 KB chunk size
            downloaded = 0
            start_time = time.time()

            print(f"[INFO] Download size: {total_size / (1024 * 1024):.2f} MB")
            print("[INFO] Starting download, please wait...")

            if TQDM_AVAILABLE and total_size > 0:
                with tqdm(total=total_size, unit="B", unit_scale=True, desc="Downloading", ncols=80) as pbar:
                    with open(temp_destination, "wb") as f:
                        while True:
                            chunk = response.read(block_size)
                            if not chunk:
                                break
                            f.write(chunk)
                            downloaded += len(chunk)
                            pbar.update(len(chunk))
            else:
                with open(temp_destination, "wb") as f:
                    while True:
                        chunk = response.read(block_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            mb_down = downloaded / (1024 * 1024)
                            mb_tot = total_size / (1024 * 1024)
                            elapsed = time.time() - start_time
                            speed = (mb_down / elapsed) if elapsed > 0 else 0
                            sys.stdout.write(f"\rDownloading: {percent:.1f}% ({mb_down:.1f}/{mb_tot:.1f} MB) [{speed:.2f} MB/s]")
                            sys.stdout.flush()
                print()

        # Rename temp file to final destination once complete
        if temp_destination.exists():
            temp_destination.replace(destination)
        print(f"[SUCCESS] Download completed and saved to: {destination}")

    except urllib.error.HTTPError as e:
        if temp_destination.exists():
            temp_destination.unlink()
        raise RuntimeError(f"HTTP Error {e.code}: {e.reason} when downloading from {url}")
    except urllib.error.URLError as e:
        if temp_destination.exists():
            temp_destination.unlink()
        raise RuntimeError(f"Network Connection Error: {e.reason}. Please check your internet connection.")
    except Exception as e:
        if temp_destination.exists():
            temp_destination.unlink()
        raise RuntimeError(f"Unexpected error during download: {e}")


def extract_zip_archive(zip_path: Path, extract_to: Path):
    """
    Extracts the downloaded ZIP archive into extract_to path safely.
    """
    if not zipfile.is_zipfile(zip_path):
        raise RuntimeError(f"Corrupted or invalid ZIP file at {zip_path}")

    print(f"\n[INFO] Extracting archive: {zip_path.name} -> {extract_to}")
    extract_to.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        # Check archive integrity
        bad_file = zip_ref.testzip()
        if bad_file:
            raise RuntimeError(f"Corrupted file found in ZIP archive: {bad_file}")

        file_list = zip_ref.namelist()
        total_files = len(file_list)
        print(f"[INFO] Archive contains {total_files} files/folders. Unpacking...")

        if TQDM_AVAILABLE:
            for member in tqdm(file_list, desc="Extracting", ncols=80):
                zip_ref.extract(member, extract_to)
        else:
            zip_ref.extractall(extract_to)

    print("[SUCCESS] Extraction completed successfully.")


def find_dataset_classes_dir(base_dir: Path) -> Path:
    """
    Traverses the extracted directory to locate the directory containing the class folders.
    """
    # If base_dir has immediate directories containing images, it's the class root
    candidate_roots = [base_dir]
    for root, dirs, _ in os.walk(base_dir):
        for d in dirs:
            candidate_roots.append(Path(root) / d)

    # Find the folder with the maximum number of subdirectories that contain images
    best_dir = base_dir
    max_class_subdirs = 0

    for candidate in candidate_roots:
        if not candidate.is_dir():
            continue
        subdirs = [p for p in candidate.iterdir() if p.is_dir()]
        # Check if subdirs contain images
        valid_subdirs = 0
        for s in subdirs:
            if any(f.suffix.lower() in VALID_IMAGE_EXTENSIONS for f in s.iterdir() if f.is_file()):
                valid_subdirs += 1
        if valid_subdirs > max_class_subdirs:
            max_class_subdirs = valid_subdirs
            best_dir = candidate

    return best_dir


def inspect_dataset(dataset_dir: Path) -> dict:
    """
    Inspects the dataset directory, detecting:
    - Total number of images
    - Total number of classes
    - Class names
    - Number of images in each class
    """
    class_dir = find_dataset_classes_dir(dataset_dir)
    class_stats = {}
    total_images = 0

    subdirs = sorted([p for p in class_dir.iterdir() if p.is_dir()])
    for subdir in subdirs:
        images = [f for f in subdir.iterdir() if f.is_file() and f.suffix.lower() in VALID_IMAGE_EXTENSIONS]
        count = len(images)
        if count > 0:
            class_stats[subdir.name] = count
            total_images += count

    summary = {
        "dataset_root": str(class_dir.resolve()),
        "total_images": total_images,
        "total_classes": len(class_stats),
        "classes": class_stats
    }
    return summary


def save_metadata(summary: dict, output_dir: Path):
    """
    Writes README.md and metadata.json in the dataset directory for documentation and reproducibility.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    metadata_path = output_dir / "dataset_metadata.json"
    metadata_content = {
        "dataset_name": DATASET_SOURCE_NAME,
        "doi": DATASET_DOI,
        "source_url": DATASET_URL,
        "license": DATASET_LICENSE,
        "total_images": summary["total_images"],
        "total_classes": summary["total_classes"],
        "class_breakdown": summary["classes"]
    }

    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata_content, f, indent=4)

    readme_path = output_dir / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("# PlantVillage Dataset Documentation\n\n")
        f.write("## Overview\n")
        f.write("This directory contains the free, public **PlantVillage Dataset** utilized for AI Plant Disease Detection.\n\n")
        f.write("## Dataset Information\n")
        f.write(f"- **Source**: {DATASET_SOURCE_NAME}\n")
        f.write(f"- **DOI**: [{DATASET_DOI}](https://doi.org/{DATASET_DOI})\n")
        f.write(f"- **License**: {DATASET_LICENSE}\n")
        f.write(f"- **Total Images**: {summary['total_images']}\n")
        f.write(f"- **Total Classes**: {summary['total_classes']}\n\n")
        f.write("## Classes & Image Distribution\n\n")
        f.write("| No. | Class Name | Image Count |\n")
        f.write("|---|---|---|\n")
        for idx, (cls_name, count) in enumerate(summary["classes"].items(), 1):
            f.write(f"| {idx} | `{cls_name}` | {count} |\n")

    print(f"[INFO] Dataset metadata and documentation saved to {metadata_path} and {readme_path}")


def main():
    """
    Main entry point for downloading, unpacking, and inspecting the dataset.
    """
    print("=" * 70)
    print("      AI Plant Disease Detection - Dataset Preparation Tool")
    print("=" * 70)

    try:
        # Step 1: Check if dataset already exists
        if check_dataset_exists(EXTRACTED_DIR):
            print(f"\n[INFO] Dataset already exists locally at: {EXTRACTED_DIR}")
            print("[INFO] Skipping download and extraction. Performing inspection...")
        else:
            # Step 2: Download raw archive if not already downloaded
            if not ZIP_PATH.exists() or not zipfile.is_zipfile(ZIP_PATH):
                download_file_with_progress(DATASET_URL, ZIP_PATH)
            else:
                print(f"\n[INFO] Raw dataset archive already exists at: {ZIP_PATH}")

            # Step 3: Extract ZIP archive
            extract_zip_archive(ZIP_PATH, EXTRACTED_DIR)

        # Step 4: Inspect dataset classes and image distribution
        print("\n[INFO] Inspecting dataset structure and counting images...")
        summary = inspect_dataset(EXTRACTED_DIR)

        if summary["total_images"] == 0 or summary["total_classes"] == 0:
            raise RuntimeError("Inspection detected 0 valid images. The extracted directory might be empty or invalid.")

        # Step 5: Save metadata and documentation
        save_metadata(summary, DATASET_ROOT)

        # Step 6: Print clean final summary as required
        print("\n" + "=" * 70)
        print("Dataset download completed successfully.\n")
        print(f"Dataset location: {summary['dataset_root']}")
        print(f"Total images: {summary['total_images']}")
        print(f"Total classes: {summary['total_classes']}")
        print("Classes:")
        for cls_name, count in summary["classes"].items():
            print(f"* {cls_name}: {count} images")
        print("=" * 70)

    except KeyboardInterrupt:
        print("\n[ABORTED] Dataset download was interrupted by the user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] An error occurred during dataset preparation: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
