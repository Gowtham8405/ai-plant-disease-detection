"""
AI Plant Disease Detection - Step 4: Model Training Script
Architecture: MobileNetV2 Transfer Learning
Dataset: datasets/processed/{train, validation, test}
Target Model: detector/ai/model/plant_disease_model.keras
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path

# Set non-interactive backend for matplotlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Project root paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATASETS_DIR = BASE_DIR / "datasets"
PROCESSED_DIR = DATASETS_DIR / "processed"
TRAIN_DIR = PROCESSED_DIR / "train"
VAL_DIR = PROCESSED_DIR / "validation"
TEST_DIR = PROCESSED_DIR / "test"
METADATA_DIR = DATASETS_DIR / "metadata"
CLASS_NAMES_FILE = METADATA_DIR / "class_names.json"

MODEL_OUTPUT_DIR = BASE_DIR / "detector" / "ai" / "model"
MODEL_FILE_PATH = MODEL_OUTPUT_DIR / "plant_disease_model.keras"
METADATA_OUTPUT_FILE = MODEL_OUTPUT_DIR / "training_metadata.json"
HISTORY_OUTPUT_FILE = MODEL_OUTPUT_DIR / "training_history.json"
REPORT_OUTPUT_FILE = MODEL_OUTPUT_DIR / "classification_report.json"
ACC_PLOT_FILE = MODEL_OUTPUT_DIR / "training_accuracy.png"
LOSS_PLOT_FILE = MODEL_OUTPUT_DIR / "training_loss.png"
CONF_MATRIX_FILE = MODEL_OUTPUT_DIR / "confusion_matrix.png"


def load_class_mapping():
    """Load class index to display name mapping from metadata if available."""
    if CLASS_NAMES_FILE.exists():
        with open(CLASS_NAMES_FILE, "r", encoding="utf-8") as f:
            raw_map = json.load(f)
            # Keys might be strings "0", "1", ...
            return {int(k): v for k, v in raw_map.items()}
    return None


def count_images_in_dir(directory: Path):
    """Count image files in directory subfolders."""
    if not directory.exists():
        return 0
    valid_exts = {".jpg", ".jpeg", ".png", ".webp"}
    count = 0
    for root, _, files in os.walk(directory):
        for f in files:
            if Path(f).suffix.lower() in valid_exts:
                count += 1
    return count


def plot_and_save_graphs(history_dict, acc_path, loss_path):
    """Generate and save training/validation accuracy and loss graphs."""
    epochs_range = range(1, len(history_dict["accuracy"]) + 1)

    # 1. Accuracy Plot
    plt.figure(figsize=(9, 6), dpi=150)
    plt.plot(epochs_range, [acc * 100 for acc in history_dict["accuracy"]], label="Training Accuracy", color="#2E7D32", linewidth=2.5, marker='o')
    plt.plot(epochs_range, [acc * 100 for acc in history_dict["val_accuracy"]], label="Validation Accuracy", color="#1565C0", linewidth=2.5, marker='s')
    plt.title("Model Accuracy: Training vs Validation", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Epoch", fontsize=12, labelpad=8)
    plt.ylabel("Accuracy (%)", fontsize=12, labelpad=8)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(loc="lower right", fontsize=11, frameon=True)
    plt.tight_layout()
    plt.savefig(acc_path)
    plt.close()

    # 2. Loss Plot
    plt.figure(figsize=(9, 6), dpi=150)
    plt.plot(epochs_range, history_dict["loss"], label="Training Loss", color="#D32F2F", linewidth=2.5, marker='o')
    plt.plot(epochs_range, history_dict["val_loss"], label="Validation Loss", color="#E65100", linewidth=2.5, marker='s')
    plt.title("Model Loss: Training vs Validation", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Epoch", fontsize=12, labelpad=8)
    plt.ylabel("Crossentropy Loss", fontsize=12, labelpad=8)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(loc="upper right", fontsize=11, frameon=True)
    plt.tight_layout()
    plt.savefig(loss_path)
    plt.close()


def plot_confusion_matrix(cm, class_names, output_path):
    """Plot and save confusion matrix with matplotlib."""
    fig, ax = plt.subplots(figsize=(16, 14), dpi=150)
    im = ax.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    # Format ticks
    ax.set(
        xticks=np.arange(cm.shape[1]),
        yticks=np.arange(cm.shape[0]),
        xticklabels=class_names,
        yticklabels=class_names,
        title="Confusion Matrix - Test Set Evaluation",
        ylabel="True Label",
        xlabel="Predicted Label"
    )

    plt.setp(ax.get_xticklabels(), rotation=90, ha="right", rotation_mode="anchor", fontsize=8)
    plt.setp(ax.get_yticklabels(), fontsize=8)

    # Loop over data dimensions and create text annotations if matrix is not too dense
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

    plt.title("Plant Disease Classification Confusion Matrix", fontsize=14, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def train_plant_disease_model(
    epochs: int = 20,
    batch_size: int = 32,
    fine_tune: bool = True,
    fine_tune_epochs: int = 8,
    learning_rate: float = 1e-3,
    fine_tune_lr: float = 1e-5,
    img_size: int = 224
):
    """Main training workflow using MobileNetV2 transfer learning."""
    MODEL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Import TensorFlow & Scikit-Learn
    try:
        import tensorflow as tf
        from tensorflow.keras import layers, models
        from tensorflow.keras.applications import MobileNetV2
        from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
        from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
        from sklearn.metrics import classification_report, confusion_matrix
    except ImportError as e:
        print(f"\n[ERROR] Required ML package is missing: {e}")
        print("Please install requirements using: pip install tensorflow matplotlib scikit-learn pillow\n")
        sys.exit(1)

    # Hardware Detection
    gpus = tf.config.list_physical_devices("GPU")
    if gpus:
        device_str = f"GPU ({gpus[0].name})"
    else:
        device_str = "CPU (Standard Multi-Core)"

    # Dataset verification
    if not (TRAIN_DIR.exists() and VAL_DIR.exists() and TEST_DIR.exists()):
        print(f"\n[ERROR] Processed datasets directory not found at: {PROCESSED_DIR}")
        print("Please ensure Step 3 (prepare_dataset.py) has run successfully.\n")
        sys.exit(1)

    train_count = count_images_in_dir(TRAIN_DIR)
    val_count = count_images_in_dir(VAL_DIR)
    test_count = count_images_in_dir(TEST_DIR)

    # Discover classes
    train_class_dirs = sorted([d.name for d in TRAIN_DIR.iterdir() if d.is_dir()])
    num_classes = len(train_class_dirs)

    if num_classes == 0:
        print("\n[ERROR] No class directories found in training directory.")
        sys.exit(1)

    # Load display names mapping
    display_names_map = load_class_mapping()
    display_names = [
        display_names_map.get(i, name) if display_names_map else name
        for i, name in enumerate(train_class_dirs)
    ]

    print("\n" + "=" * 50)
    print("      AI PLANT DISEASE MODEL TRAINING")
    print("=" * 50)
    print(f"Model Architecture : MobileNetV2 (Transfer Learning)")
    print(f"Compute Device     : {device_str}")
    print(f"Image Resolution   : {img_size}x{img_size}")
    print(f"Number of Classes  : {num_classes}")
    print(f"Training Images    : {train_count}")
    print(f"Validation Images  : {val_count}")
    print(f"Test Images        : {test_count}")
    print(f"Initial Batch Size : {batch_size}")
    print(f"Initial Epochs     : {epochs}")
    print("=" * 50 + "\n")

    # Load datasets using tf.keras.utils.image_dataset_from_directory
    print("[1/5] Loading datasets into tf.data pipelines...")
    
    def create_datasets(bs):
        ds_train = tf.keras.utils.image_dataset_from_directory(
            TRAIN_DIR,
            labels="inferred",
            label_mode="categorical",
            image_size=(img_size, img_size),
            batch_size=bs,
            shuffle=True,
            seed=42,
        )
        ds_val = tf.keras.utils.image_dataset_from_directory(
            VAL_DIR,
            labels="inferred",
            label_mode="categorical",
            image_size=(img_size, img_size),
            batch_size=bs,
            shuffle=False,
        )
        ds_test = tf.keras.utils.image_dataset_from_directory(
            TEST_DIR,
            labels="inferred",
            label_mode="categorical",
            image_size=(img_size, img_size),
            batch_size=bs,
            shuffle=False,
        )
        return ds_train, ds_val, ds_test

    try:
        train_ds, val_ds, test_ds = create_datasets(batch_size)
    except Exception as e:
        print(f"[WARN] Batch size {batch_size} failed: {e}. Falling back to batch size 16.")
        batch_size = 16
        train_ds, val_ds, test_ds = create_datasets(batch_size)

    # Prefetch for performance
    autotune = tf.data.AUTOTUNE
    train_ds = train_ds.prefetch(buffer_size=autotune)
    val_ds = val_ds.prefetch(buffer_size=autotune)
    test_ds = test_ds.prefetch(buffer_size=autotune)

    # 2. Build MobileNetV2 Transfer Learning Architecture
    print("\n[2/5] Building MobileNetV2 Transfer Learning Model...")

    data_augmentation = tf.keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.1),
        layers.RandomTranslation(0.08, 0.08),
    ], name="data_augmentation")

    base_model = MobileNetV2(
        input_shape=(img_size, img_size, 3),
        include_top=False,
        weights="imagenet"
    )
    base_model.trainable = False  # Freeze pretrained weights initially

    inputs = layers.Input(shape=(img_size, img_size, 3), name="input_leaf_image")
    x = data_augmentation(inputs)
    x = preprocess_input(x)
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D(name="global_avg_pool")(x)
    x = layers.Dropout(0.25, name="dropout")(x)
    outputs = layers.Dense(num_classes, activation="softmax", name="disease_prediction")(x)

    model = models.Model(inputs=inputs, outputs=outputs, name="plant_disease_mobilenetv2")

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    model.summary(line_length=80)

    # Callbacks
    checkpoint_cb = ModelCheckpoint(
        filepath=str(MODEL_FILE_PATH),
        monitor="val_accuracy",
        mode="max",
        save_best_only=True,
        verbose=1
    )
    early_stopping_cb = EarlyStopping(
        monitor="val_loss",
        mode="min",
        patience=4,
        restore_best_weights=True,
        verbose=1
    )
    reduce_lr_cb = ReduceLROnPlateau(
        monitor="val_loss",
        mode="min",
        factor=0.2,
        patience=2,
        min_lr=1e-6,
        verbose=1
    )

    callbacks = [checkpoint_cb, early_stopping_cb, reduce_lr_cb]

    # 3. Phase 1 Training (Feature Extraction)
    print("\n[3/5] Starting Phase 1: Feature Extraction Training (Frozen Base)...")
    start_time = time.time()
    
    history_phase1 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=callbacks,
        verbose=1
    )

    combined_history = {
        "accuracy": [float(v) for v in history_phase1.history.get("accuracy", [])],
        "val_accuracy": [float(v) for v in history_phase1.history.get("val_accuracy", [])],
        "loss": [float(v) for v in history_phase1.history.get("loss", [])],
        "val_loss": [float(v) for v in history_phase1.history.get("val_loss", [])],
    }
    epochs_completed = len(combined_history["accuracy"])

    # 4. Phase 2: Optional Fine-Tuning
    phase_used = "Phase 1 (Frozen Base)"
    if fine_tune and epochs_completed >= 2:
        print("\n[4/5] Starting Phase 2: Fine-Tuning Upper Layers...")
        base_model.trainable = True
        
        # Freeze all layers before the 100th layer
        fine_tune_at = 100
        for layer in base_model.layers[:fine_tune_at]:
            layer.trainable = False

        # Ensure BatchNorm stays frozen during fine-tuning for numerical stability
        for layer in base_model.layers:
            if isinstance(layer, layers.BatchNormalization):
                layer.trainable = False

        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=fine_tune_lr),
            loss="categorical_crossentropy",
            metrics=["accuracy"]
        )

        ft_early_stopping = EarlyStopping(
            monitor="val_loss",
            mode="min",
            patience=3,
            restore_best_weights=True,
            verbose=1
        )

        total_target_epochs = epochs_completed + fine_tune_epochs
        history_phase2 = model.fit(
            train_ds,
            validation_data=val_ds,
            initial_epoch=epochs_completed,
            epochs=total_target_epochs,
            callbacks=[checkpoint_cb, ft_early_stopping, reduce_lr_cb],
            verbose=1
        )

        for key in ["accuracy", "val_accuracy", "loss", "val_loss"]:
            if key in history_phase2.history:
                combined_history[key].extend([float(v) for v in history_phase2.history[key]])

        epochs_completed = len(combined_history["accuracy"])
        phase_used = f"Phase 1 + Phase 2 (Fine-tuned from layer {fine_tune_at})"

    training_time_sec = round(time.time() - start_time, 2)
    print(f"\nTraining finished in {training_time_sec} seconds ({epochs_completed} total epochs).")

    # Load best checkpointed model for final evaluation
    print(f"\nLoading best checkpointed model from {MODEL_FILE_PATH}...")
    best_model = models.load_model(str(MODEL_FILE_PATH))

    # 5. Test Set Evaluation & Metrics
    print("\n[5/5] Evaluating Best Model on Unseen Test Dataset...")
    eval_results = best_model.evaluate(test_ds, verbose=1)
    test_loss = float(eval_results[0])
    test_acc = float(eval_results[1])

    # Predict test samples for Confusion Matrix & Classification Report
    print("Generating predictions on test set for detailed metrics...")
    y_true_all = []
    y_pred_all = []

    for images, labels in test_ds:
        preds = best_model.predict(images, verbose=0)
        y_true_all.extend(np.argmax(labels.numpy(), axis=1))
        y_pred_all.extend(np.argmax(preds, axis=1))

    y_true_all = np.array(y_true_all)
    y_pred_all = np.array(y_pred_all)

    # Classification Report
    clf_report_dict = classification_report(
        y_true_all,
        y_pred_all,
        target_names=display_names,
        output_dict=True,
        zero_division=0
    )

    with open(REPORT_OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(clf_report_dict, f, indent=4)
    print(f"Saved classification report -> {REPORT_OUTPUT_FILE}")

    # Confusion Matrix
    cm = confusion_matrix(y_true_all, y_pred_all)
    plot_confusion_matrix(cm, display_names, CONF_MATRIX_FILE)
    print(f"Saved confusion matrix plot -> {CONF_MATRIX_FILE}")

    # Training Graphs
    plot_and_save_graphs(combined_history, ACC_PLOT_FILE, LOSS_PLOT_FILE)
    print(f"Saved training accuracy plot -> {ACC_PLOT_FILE}")
    print(f"Saved training loss plot -> {LOSS_PLOT_FILE}")

    # History JSON
    with open(HISTORY_OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(combined_history, f, indent=4)
    print(f"Saved training history -> {HISTORY_OUTPUT_FILE}")

    best_val_acc = max(combined_history["val_accuracy"]) if combined_history["val_accuracy"] else 0.0

    # Training Metadata JSON
    metadata = {
        "model": "MobileNetV2",
        "image_size": [img_size, img_size],
        "num_classes": num_classes,
        "classes": train_class_dirs,
        "display_names": display_names,
        "epochs_requested": epochs + (fine_tune_epochs if fine_tune else 0),
        "epochs_completed": epochs_completed,
        "batch_size": batch_size,
        "optimizer": "Adam",
        "learning_rate": learning_rate,
        "fine_tune_learning_rate": fine_tune_lr if fine_tune else None,
        "training_phase": phase_used,
        "device": device_str,
        "dataset_split": {
            "train": train_count,
            "validation": val_count,
            "test": test_count
        },
        "training_duration_seconds": training_time_sec,
        "best_validation_accuracy": round(best_val_acc * 100, 2),
        "test_accuracy": round(test_acc * 100, 2),
        "test_loss": round(test_loss, 4),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    with open(METADATA_OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)
    print(f"Saved training metadata -> {METADATA_OUTPUT_FILE}")

    # Final summary banner
    print("\n" + "=" * 50)
    print("             TRAINING COMPLETE")
    print("=" * 50)
    print(f"Training Strategy        : {phase_used}")
    print(f"Total Epochs Run         : {epochs_completed}")
    print(f"Best Validation Accuracy : {best_val_acc * 100:.2f}%")
    print(f"Test Accuracy            : {test_acc * 100:.2f}%")
    print(f"Test Loss                : {test_loss:.4f}")
    print(f"\nModel File Path:")
    print(f"  {MODEL_FILE_PATH}")
    print(f"\nClass Names Mapping:")
    print(f"  {CLASS_NAMES_FILE}")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train MobileNetV2 Plant Disease Detection Model")
    parser.add_argument("--epochs", type=int, default=15, help="Number of initial training epochs (default: 15)")
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size for training (default: 32)")
    parser.add_argument("--no-fine-tune", action="store_true", help="Disable fine-tuning phase")
    parser.add_argument("--fine-tune-epochs", type=int, default=5, help="Number of fine-tuning epochs (default: 5)")
    parser.add_argument("--lr", type=float, default=1e-3, help="Learning rate (default: 0.001)")
    
    args = parser.parse_args()

    train_plant_disease_model(
        epochs=args.epochs,
        batch_size=args.batch_size,
        fine_tune=not args.no_fine_tune,
        fine_tune_epochs=args.fine_tune_epochs,
        learning_rate=args.lr
    )
