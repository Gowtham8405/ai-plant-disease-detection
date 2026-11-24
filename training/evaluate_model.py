"""
AI Plant Disease Detection - Step 5: Model Evaluation & Verification Script
Architecture: MobileNetV2 Transfer Learning
Target Model: detector/ai/model/plant_disease_model.keras
Test Dataset: datasets/processed/test/
"""

import os
import sys
import json
import time
from pathlib import Path

# Set non-interactive backend for matplotlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# Project root paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATASETS_DIR = BASE_DIR / "datasets"
PROCESSED_DIR = DATASETS_DIR / "processed"
TEST_DIR = PROCESSED_DIR / "test"
METADATA_DIR = DATASETS_DIR / "metadata"
CLASS_NAMES_FILE = METADATA_DIR / "class_names.json"

MODEL_OUTPUT_DIR = BASE_DIR / "detector" / "ai" / "model"
MODEL_FILE_PATH = MODEL_OUTPUT_DIR / "plant_disease_model.keras"

EVAL_REPORT_JSON = MODEL_OUTPUT_DIR / "evaluation_report.json"
EVAL_REPORT_TXT = MODEL_OUTPUT_DIR / "evaluation_report.txt"
EVAL_CONF_MATRIX_PNG = MODEL_OUTPUT_DIR / "evaluation_confusion_matrix.png"
CONFIDENCE_ANALYSIS_JSON = MODEL_OUTPUT_DIR / "confidence_analysis.json"
SAMPLE_PREDICTIONS_JSON = MODEL_OUTPUT_DIR / "sample_predictions.json"
EVAL_SUMMARY_JSON = MODEL_OUTPUT_DIR / "evaluation_summary.json"


def load_class_mapping():
    """Load class index to display name mapping."""
    if not CLASS_NAMES_FILE.exists():
        print(f"[ERROR] Class names metadata file not found at: {CLASS_NAMES_FILE}")
        sys.exit(1)

    with open(CLASS_NAMES_FILE, "r", encoding="utf-8") as f:
        raw_map = json.load(f)
        return {int(k): v for k, v in raw_map.items()}


def plot_confusion_matrix(cm, class_names, output_path):
    """Plot and save confusion matrix with high-resolution labels."""
    fig, ax = plt.subplots(figsize=(18, 15), dpi=150)
    im = ax.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    ax.set(
        xticks=np.arange(cm.shape[1]),
        yticks=np.arange(cm.shape[0]),
        xticklabels=class_names,
        yticklabels=class_names,
        title="Plant Disease Classification - Test Evaluation Confusion Matrix",
        ylabel="True Disease Class",
        xlabel="Predicted Disease Class"
    )

    plt.setp(ax.get_xticklabels(), rotation=90, ha="right", rotation_mode="anchor", fontsize=8)
    plt.setp(ax.get_yticklabels(), fontsize=8)

    thresh = cm.max() / 2.0
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            val = cm[i, j]
            if val > 0:
                ax.text(
                    j, i, format(val, "d"),
                    ha="center", va="center",
                    color="white" if val > thresh else "black",
                    fontsize=6
                )

    plt.title("Plant Disease Model - Test Confusion Matrix (38 Classes)", fontsize=14, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def evaluate_model():
    """Execute complete Step 5 Model Evaluation & Verification."""
    print("\n" + "=" * 50)
    print("      AI PLANT DISEASE MODEL EVALUATION")
    print("=" * 50)

    # 1. Verify Model Existence & Load Model
    if not MODEL_FILE_PATH.exists():
        print(f"\n[ERROR] Model binary not found at: {MODEL_FILE_PATH}")
        sys.exit(1)

    try:
        import tensorflow as tf
        from tensorflow.keras.models import load_model
        from sklearn.metrics import classification_report, confusion_matrix, precision_recall_fscore_support
    except ImportError as e:
        print(f"\n[ERROR] Missing ML package: {e}")
        sys.exit(1)

    print(f"\n[1/7] Loading trained model from {MODEL_FILE_PATH}...")
    model = load_model(str(MODEL_FILE_PATH))
    output_shape = list(model.output_shape)
    num_model_classes = output_shape[-1]
    print(f"Model output shape verified: {output_shape} ({num_model_classes} classes)")

    # 2. Verify Class Mapping
    class_map = load_class_mapping()
    num_mapped_classes = len(class_map)
    print(f"Class mapping loaded: {num_mapped_classes} classes from {CLASS_NAMES_FILE.name}")

    if num_model_classes != num_mapped_classes or num_model_classes != 38:
        print(f"[ERROR] Class count mismatch! Model output classes ({num_model_classes}) != Mapping classes ({num_mapped_classes}).")
        sys.exit(1)

    # 3. Verify Test Dataset
    if not TEST_DIR.exists():
        print(f"[ERROR] Test dataset directory not found at: {TEST_DIR}")
        sys.exit(1)

    test_class_dirs = sorted([d.name for d in TEST_DIR.iterdir() if d.is_dir()])
    if len(test_class_dirs) != 38:
        print(f"[ERROR] Test folder class count mismatch: found {len(test_class_dirs)}, expected 38.")
        sys.exit(1)

    display_names = [class_map.get(i, name) for i, name in enumerate(test_class_dirs)]

    # 4. Load Test Dataset Pipeline
    print("\n[2/7] Loading unseen test dataset...")
    test_ds = tf.keras.utils.image_dataset_from_directory(
        TEST_DIR,
        labels="inferred",
        label_mode="categorical",
        image_size=(224, 224),
        batch_size=32,
        shuffle=False
    )
    total_test_images = len(test_ds.file_paths)
    print(f"Total unseen test images: {total_test_images}")

    # 5. Evaluate Test Loss and Accuracy
    print("\n[3/7] Evaluating test dataset loss and accuracy...")
    eval_results = model.evaluate(test_ds, verbose=1)
    test_loss = float(eval_results[0])
    test_accuracy = float(eval_results[1])

    # 6. Predict Batch-by-Batch
    print("\n[4/7] Generating batch predictions and softmax probabilities...")
    all_probs = model.predict(test_ds, verbose=1)
    y_pred = np.argmax(all_probs, axis=1)
    max_confidences = np.max(all_probs, axis=1)

    # Gather ground truth labels
    y_true = []
    for _, labels in test_ds:
        y_true.extend(np.argmax(labels.numpy(), axis=1))
    y_true = np.array(y_true)

    # 7. Calculate Per-Class Metrics & Reports
    print("\n[5/7] Calculating per-class classification metrics...")
    clf_report_dict = classification_report(
        y_true,
        y_pred,
        target_names=display_names,
        output_dict=True,
        zero_division=0
    )
    clf_report_text = classification_report(
        y_true,
        y_pred,
        target_names=display_names,
        digits=4,
        zero_division=0
    )

    # Save JSON and TXT reports
    with open(EVAL_REPORT_JSON, "w", encoding="utf-8") as f:
        json.dump(clf_report_dict, f, indent=4)
    print(f"Saved evaluation report JSON -> {EVAL_REPORT_JSON}")

    with open(EVAL_REPORT_TXT, "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write("      AI PLANT DISEASE MODEL - TEST SET EVALUATION REPORT\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Model Architecture  : MobileNetV2\n")
        f.write(f"Total Test Images   : {total_test_images}\n")
        f.write(f"Test Accuracy       : {test_accuracy * 100:.2f}%\n")
        f.write(f"Test Loss           : {test_loss:.4f}\n\n")
        f.write(clf_report_text)
        f.write("\n" + "=" * 80 + "\n")
    print(f"Saved evaluation report TXT  -> {EVAL_REPORT_TXT}")

    # Generate Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    plot_confusion_matrix(cm, display_names, EVAL_CONF_MATRIX_PNG)
    print(f"Saved confusion matrix plot  -> {EVAL_CONF_MATRIX_PNG}")

    # Calculate Macro and Weighted Metrics
    macro_p, macro_r, macro_f1, _ = precision_recall_fscore_support(y_true, y_pred, average="macro", zero_division=0)
    weighted_p, weighted_r, weighted_f1, _ = precision_recall_fscore_support(y_true, y_pred, average="weighted", zero_division=0)

    # 8. Identify Difficult Classes
    per_class_scores = []
    for i, name in enumerate(display_names):
        metrics = clf_report_dict.get(name, {})
        per_class_scores.append({
            "class_name": name,
            "precision": round(metrics.get("precision", 0) * 100, 2),
            "recall": round(metrics.get("recall", 0) * 100, 2),
            "f1_score": round(metrics.get("f1-score", 0) * 100, 2),
            "support": int(metrics.get("support", 0))
        })

    lowest_precision = sorted(per_class_scores, key=lambda x: x["precision"])[:5]
    lowest_recall = sorted(per_class_scores, key=lambda x: x["recall"])[:5]
    lowest_f1 = sorted(per_class_scores, key=lambda x: x["f1_score"])[:5]

    # 9. Prediction Confidence Analysis
    print("\n[6/7] Analyzing prediction confidence distribution...")
    conf_below_50 = int(np.sum(max_confidences < 0.50))
    conf_below_60 = int(np.sum(max_confidences < 0.60))
    conf_below_70 = int(np.sum(max_confidences < 0.70))
    conf_below_80 = int(np.sum(max_confidences < 0.80))
    conf_below_90 = int(np.sum(max_confidences < 0.90))

    confidence_stats = {
        "total_predictions": int(len(max_confidences)),
        "average_max_confidence": round(float(np.mean(max_confidences)) * 100, 2),
        "median_max_confidence": round(float(np.median(max_confidences)) * 100, 2),
        "min_max_confidence": round(float(np.min(max_confidences)) * 100, 2),
        "max_max_confidence": round(float(np.max(max_confidences)) * 100, 2),
        "distribution": {
            "below_50_percent": {"count": conf_below_50, "percentage": round(conf_below_50 / total_test_images * 100, 2)},
            "below_60_percent": {"count": conf_below_60, "percentage": round(conf_below_60 / total_test_images * 100, 2)},
            "below_70_percent": {"count": conf_below_70, "percentage": round(conf_below_70 / total_test_images * 100, 2)},
            "below_80_percent": {"count": conf_below_80, "percentage": round(conf_below_80 / total_test_images * 100, 2)},
            "below_90_percent": {"count": conf_below_90, "percentage": round(conf_below_90 / total_test_images * 100, 2)}
        },
        "lowest_precision_classes": lowest_precision,
        "lowest_recall_classes": lowest_recall,
        "lowest_f1_classes": lowest_f1
    }

    with open(CONFIDENCE_ANALYSIS_JSON, "w", encoding="utf-8") as f:
        json.dump(confidence_stats, f, indent=4)
    print(f"Saved confidence analysis    -> {CONFIDENCE_ANALYSIS_JSON}")

    # 10. Sample Individual Predictions
    file_paths = test_ds.file_paths
    correct_samples = []
    incorrect_samples = []

    for idx, (path_str, true_lbl, pred_lbl, conf) in enumerate(zip(file_paths, y_true, y_pred, max_confidences)):
        rel_path = os.path.relpath(path_str, str(BASE_DIR)).replace("\\", "/")
        sample_entry = {
            "image_path": rel_path,
            "actual_class": display_names[true_lbl],
            "predicted_class": display_names[pred_lbl],
            "confidence_percent": round(float(conf) * 100, 2),
            "is_correct": bool(true_lbl == pred_lbl)
        }
        if true_lbl == pred_lbl and len(correct_samples) < 10:
            correct_samples.append(sample_entry)
        elif true_lbl != pred_lbl and len(incorrect_samples) < 10:
            incorrect_samples.append(sample_entry)

    sample_predictions_data = {
        "correct_samples": correct_samples,
        "incorrect_samples": incorrect_samples
    }

    with open(SAMPLE_PREDICTIONS_JSON, "w", encoding="utf-8") as f:
        json.dump(sample_predictions_data, f, indent=4)
    print(f"Saved sample predictions     -> {SAMPLE_PREDICTIONS_JSON}")

    # 11. Test Invalid / Non-Plant Image Behavior (Sanity Check)
    print("\n[7/7] Testing Out-Of-Distribution / Non-Plant Image Sanity Behavior...")
    # Generate deterministic non-plant baseline patterns (pure noise, uniform gray) to analyze softmax response
    ood_tests = []
    noise_img = np.random.RandomState(42).randint(0, 256, (224, 224, 3), dtype=np.uint8)
    gray_img = np.full((224, 224, 3), 128, dtype=np.uint8)
    black_img = np.zeros((224, 224, 3), dtype=np.uint8)

    test_inputs = [
        ("Random Gaussian/Uniform Noise", noise_img),
        ("Uniform Neutral Gray (128)", gray_img),
        ("Uniform Black (0)", black_img)
    ]

    for name, img_arr in test_inputs:
        input_tensor = tf.expand_dims(tf.convert_to_tensor(img_arr, dtype=tf.float32), 0)
        probs = model.predict(input_tensor, verbose=0)[0]
        pred_idx = int(np.argmax(probs))
        max_prob = float(np.max(probs))
        ood_tests.append({
            "test_type": name,
            "assigned_class": display_names[pred_idx],
            "confidence_percent": round(max_prob * 100, 2),
            "observation": "Standard softmax forces output probabilities across known classes even for non-plant inputs."
        })

    # 12. Save Evaluation Summary JSON
    summary_data = {
        "model": "MobileNetV2",
        "num_classes": num_model_classes,
        "test_images": total_test_images,
        "test_accuracy": round(test_accuracy * 100, 2),
        "test_loss": round(test_loss, 4),
        "macro_precision": round(macro_p * 100, 2),
        "macro_recall": round(macro_r * 100, 2),
        "macro_f1": round(macro_f1 * 100, 2),
        "weighted_precision": round(weighted_p * 100, 2),
        "weighted_recall": round(weighted_r * 100, 2),
        "weighted_f1": round(weighted_f1 * 100, 2),
        "model_output_shape": output_shape,
        "class_mapping_verified": True,
        "out_of_distribution_tests": ood_tests
    }

    with open(EVAL_SUMMARY_JSON, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=4)
    print(f"Saved evaluation summary     -> {EVAL_SUMMARY_JSON}")

    # 13. End-To-End Single Image Inference Pipeline Verification
    print("\nVerifying end-to-end inference on single sample test image...")
    sample_img_path = Path(file_paths[0])
    pil_img = Image.open(sample_img_path).convert("RGB").resize((224, 224))
    img_array = np.array(pil_img, dtype=np.float32)
    img_batch = np.expand_dims(img_array, axis=0)
    single_pred_probs = model.predict(img_batch, verbose=0)[0]
    single_pred_idx = int(np.argmax(single_pred_probs))
    single_pred_conf = float(single_pred_probs[single_pred_idx])

    print(f"Input image         : {sample_img_path.name}")
    print(f"Preprocessed shape  : {img_batch.shape}")
    print(f"Output vector shape : {single_pred_probs.shape} (38 class probabilities)")
    print(f"Top prediction      : {display_names[single_pred_idx]} ({single_pred_conf * 100:.2f}%)")

    # 14. Final Verification Output Banner
    print("\n" + "=" * 50)
    print("           MODEL EVALUATION COMPLETE")
    print("=" * 50)
    print(f"Model                 : MobileNetV2")
    print(f"Classes               : {num_model_classes}")
    print(f"Test Images           : {total_test_images}")
    print(f"\nTest Accuracy         : {test_accuracy * 100:.2f}%")
    print(f"Test Loss             : {test_loss:.4f}")
    print(f"\nMacro Precision       : {macro_p * 100:.2f}%")
    print(f"Macro Recall          : {macro_r * 100:.2f}%")
    print(f"Macro F1              : {macro_f1 * 100:.2f}%")
    print(f"\nWeighted Precision    : {weighted_p * 100:.2f}%")
    print(f"Weighted Recall       : {weighted_r * 100:.2f}%")
    print(f"Weighted F1           : {weighted_f1 * 100:.2f}%")
    print(f"\nModel Output          : {tuple(output_shape)}")
    print(f"Class Mapping         : VERIFIED")
    print(f"\nEvaluation Status     : PASSED")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    evaluate_model()
