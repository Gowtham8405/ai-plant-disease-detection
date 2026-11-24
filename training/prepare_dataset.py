"""
AI Plant Disease Detection - Dataset Preprocessing & Train/Val/Test Splitting (Step 3)
======================================================================================
This script prepares the combined plant disease image dataset for AI model training:
1. Reads all standardized class folders from datasets/combined/.
2. Validates image readability and file formats (JPG, JPEG, PNG, WEBP).
3. Detects and eliminates exact duplicate images using SHA-256 to prevent data leakage.
4. Performs a strictly isolated 70% Train / 15% Validation / 15% Test split with a fixed random seed.
5. Verifies zero data leakage between train, validation, and test partitions.
6. Generates class_names.json and prepared_dataset_summary.json metadata.
7. Populates datasets/processed/{train, validation, test}/.

Usage:
    python training/prepare_dataset.py
"""

import os
import sys
import json
import shutil
import hashlib
import random
from pathlib import Path
from PIL import Image

# =====================================================================
# Configuration Parameters
# =====================================================================
RANDOM_SEED = 42
TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASETS_DIR = PROJECT_ROOT / "datasets"
COMBINED_DIR = DATASETS_DIR / "combined"
PROCESSED_DIR = DATASETS_DIR / "processed"
METADATA_DIR = DATASETS_DIR / "metadata"

TRAIN_DIR = PROCESSED_DIR / "train"
VAL_DIR = PROCESSED_DIR / "validation"
TEST_DIR = PROCESSED_DIR / "test"

VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".JPG", ".JPEG", ".PNG", ".WEBP"}


def format_display_name(raw_class_name: str) -> str:
    """
    Converts a folder name like 'Apple___Apple_Scab' or 'Tomato___Late_Blight'
    into a clean human-readable name like 'Apple - Apple Scab' or 'Tomato - Late Blight'.
    """
    if "___" in raw_class_name:
        parts = raw_class_name.split("___", 1)
        species = parts[0].replace("_", " ").strip().title()
        disease = parts[1].replace("_", " ").strip().title()
        return f"{species} - {disease}"
    return raw_class_name.replace("_", " ").strip().title()


def get_file_sha256(file_path: Path) -> str:
    """Computes SHA-256 hash of a file for exact duplicate detection."""
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            sha.update(chunk)
    return sha.hexdigest()


def validate_image_file(file_path: Path) -> tuple:
    """
    Validates that the image file can be opened and verified by PIL.
    Returns (is_valid: bool, format_name: str).
    """
    try:
        with Image.open(file_path) as img:
            img.verify()
            fmt = img.format if img.format else file_path.suffix.upper().replace(".", "")
            return True, fmt
    except Exception:
        return False, ""


def prepare_dataset():
    """
    Executes the dataset validation, deduplication, train/val/test splitting,
    and metadata generation.
    """
    print("========================================", flush=True)
    print("AI PLANT DISEASE DATASET PREPARATION", flush=True)
    print("Checking combined dataset...", flush=True)

    if not COMBINED_DIR.exists():
        print(f"[ERROR] Combined dataset directory not found at: {COMBINED_DIR}", file=sys.stderr)
        print("Please ensure Step 2 has created datasets/combined/ first.", file=sys.stderr)
        sys.exit(1)

    # Discover valid class folders
    class_folders = sorted([d for d in COMBINED_DIR.iterdir() if d.is_dir()])
    if not class_folders:
        print(f"[ERROR] No class directories found in: {COMBINED_DIR}", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(class_folders)} class directories in combined dataset.", flush=True)
    print("Validating images and checking for duplicates...", flush=True)

    rng = random.Random(RANDOM_SEED)

    # Tracking metrics
    total_original_images = 0
    total_valid_images = 0
    total_corrupt_images = 0
    total_duplicates_removed = 0
    detected_formats = set()

    # Global hash tracker to prevent cross-class/split duplicate leakage
    seen_hashes = {}  # sha256 -> (class_name, file_path)
    
    # Class-wise validated unique images list: class_name -> list of (file_path, sha256)
    class_unique_images = {}

    for class_folder in class_folders:
        class_name = class_folder.name
        class_unique_images[class_name] = []

        files = [class_folder / f for f in os.listdir(class_folder) if Path(f).suffix.lower() in VALID_EXTENSIONS]

        for fpath in files:
            total_original_images += 1

            # 1. Validation check
            is_valid, fmt = validate_image_file(fpath)
            if not is_valid:
                total_corrupt_images += 1
                continue

            if fmt:
                detected_formats.add(fmt)

            # 2. Exact Duplicate Check (SHA-256)
            try:
                img_hash = get_file_sha256(fpath)
            except Exception:
                total_corrupt_images += 1
                continue

            if img_hash in seen_hashes:
                total_duplicates_removed += 1
                continue

            # Valid unique image
            seen_hashes[img_hash] = (class_name, fpath)
            class_unique_images[class_name].append((fpath, img_hash))
            total_valid_images += 1

    # Clean existing processed directory if any
    if PROCESSED_DIR.exists():
        for split_dir in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
            if split_dir.exists():
                shutil.rmtree(split_dir)

    TRAIN_DIR.mkdir(parents=True, exist_ok=True)
    VAL_DIR.mkdir(parents=True, exist_ok=True)
    TEST_DIR.mkdir(parents=True, exist_ok=True)

    print("Splitting dataset into Train (70%), Validation (15%), Test (15%)...", flush=True)

    # Class metadata dictionary
    class_names_map = {}
    class_summary_stats = {}
    
    total_train = 0
    total_val = 0
    total_test = 0

    # Split hash sets for zero-leakage verification
    train_hashes = set()
    val_hashes = set()
    test_hashes = set()

    low_count_classes = []

    for idx, (class_name, img_items) in enumerate(class_unique_images.items()):
        display_name = format_display_name(class_name)
        class_names_map[str(idx)] = display_name

        n_images = len(img_items)
        if n_images < 50:
            low_count_classes.append((display_name, n_images))

        # Shuffle deterministically
        items = list(img_items)
        rng.shuffle(items)

        # Compute split partitions
        n_train = int(n_images * TRAIN_RATIO)
        n_val = int(n_images * VAL_RATIO)
        n_test = n_images - n_train - n_val

        # Edge case adjustment for tiny classes
        if n_images >= 3 and n_val == 0:
            n_val = 1
            n_train -= 1
        if n_images >= 3 and n_test == 0:
            n_test = 1
            n_train -= 1

        train_items = items[:n_train]
        val_items = items[n_train:n_train + n_val]
        test_items = items[n_train + n_val:]

        # Create target directories for this class
        (TRAIN_DIR / class_name).mkdir(parents=True, exist_ok=True)
        (VAL_DIR / class_name).mkdir(parents=True, exist_ok=True)
        (TEST_DIR / class_name).mkdir(parents=True, exist_ok=True)

        # Copy train files
        for src_path, h in train_items:
            dst = TRAIN_DIR / class_name / src_path.name
            shutil.copy2(src_path, dst)
            train_hashes.add(h)

        # Copy val files
        for src_path, h in val_items:
            dst = VAL_DIR / class_name / src_path.name
            shutil.copy2(src_path, dst)
            val_hashes.add(h)

        # Copy test files
        for src_path, h in test_items:
            dst = TEST_DIR / class_name / src_path.name
            shutil.copy2(src_path, dst)
            test_hashes.add(h)

        total_train += len(train_items)
        total_val += len(val_items)
        total_test += len(test_items)

        class_summary_stats[class_name] = {
            "class_index": idx,
            "display_name": display_name,
            "total_images": n_images,
            "train": len(train_items),
            "validation": len(val_items),
            "test": len(test_items)
        }

    # Data Leakage Assertion Check
    train_val_overlap = train_hashes.intersection(val_hashes)
    train_test_overlap = train_hashes.intersection(test_hashes)
    val_test_overlap = val_hashes.intersection(test_hashes)

    if train_val_overlap or train_test_overlap or val_test_overlap:
        print("[CRITICAL ERROR] Data leakage detected between splits!", file=sys.stderr)
        sys.exit(1)

    # Save metadata files
    METADATA_DIR.mkdir(parents=True, exist_ok=True)

    # 1. class_names.json
    class_names_path = METADATA_DIR / "class_names.json"
    with open(class_names_path, "w", encoding="utf-8") as f:
        json.dump(class_names_map, f, indent=4)

    # 2. prepared_dataset_summary.json
    summary_data = {
        "project": "AI Plant Disease Detection",
        "step": "Step 3 - Dataset Preparation & Train/Val/Test Split",
        "total_classes": len(class_folders),
        "total_images": total_valid_images,
        "original_raw_images": total_original_images,
        "train_images": total_train,
        "validation_images": total_val,
        "test_images": total_test,
        "corrupt_images": total_corrupt_images,
        "duplicate_images_removed": total_duplicates_removed,
        "split_ratio": {
            "train": TRAIN_RATIO,
            "validation": VAL_RATIO,
            "test": TEST_RATIO
        },
        "random_seed": RANDOM_SEED,
        "detected_formats": sorted(list(detected_formats)),
        "data_leakage_verified": True,
        "classes": class_summary_stats
    }

    summary_path = METADATA_DIR / "prepared_dataset_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=4)

    # Terminal Output strictly matching specified requirements
    print("\n========================================")
    print("DATASET PREPARATION COMPLETE")
    print("========================================\n")
    print(f"Classes              : {len(class_folders)}")
    print(f"Total images         : {total_valid_images}")
    print(f"Training images      : {total_train}")
    print(f"Validation images    : {total_val}")
    print(f"Testing images       : {total_test}")
    print(f"Corrupt images       : {total_corrupt_images}")
    print(f"Duplicates removed   : {total_duplicates_removed}\n")
    print(f"Train directory      : {TRAIN_DIR.as_posix()}")
    print(f"Validation directory : {VAL_DIR.as_posix()}")
    print(f"Test directory       : {TEST_DIR.as_posix()}")
    print(f"Class file           : {class_names_path.as_posix()}")
    print("========================================")

    if low_count_classes:
        print("\nNote: Classes with lower representation:")
        for name, count in low_count_classes:
            print(f"- {name}: {count} images")


if __name__ == "__main__":
    prepare_dataset()
