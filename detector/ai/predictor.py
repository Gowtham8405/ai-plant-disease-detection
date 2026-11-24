"""
AI Plant Disease Predictor Service
==================================
Handles image validation, preprocessing, and MobileNetV2 inference
for the Django web application.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Union, Optional
from io import BytesIO

from PIL import Image, UnidentifiedImageError
import numpy as np

# Configure logger
logger = logging.getLogger(__name__)

# Base project paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / "detector" / "ai" / "model" / "plant_disease_model.keras"
CLASS_NAMES_FILE = BASE_DIR / "datasets" / "metadata" / "class_names.json"

# Supported image formats & constraints
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}
IMAGE_SIZE = (224, 224)
DEFAULT_CONFIDENCE_THRESHOLD = 0.70  # 70% threshold


class PlantDiseasePredictor:
    """
    Singleton predictor class to cache the trained MobileNetV2 model
    and class mapping in memory across Django requests.
    """
    _instance: Optional["PlantDiseasePredictor"] = None
    _model = None
    _class_map: Optional[Dict[int, str]] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PlantDiseasePredictor, cls).__new__(cls)
        return cls._instance

    def initialize(self):
        """Load model and class names into memory once."""
        if self._initialized:
            return

        # 1. Load class mapping from JSON
        if not CLASS_NAMES_FILE.exists():
            error_msg = f"Class names file not found at: {CLASS_NAMES_FILE}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        try:
            with open(CLASS_NAMES_FILE, "r", encoding="utf-8") as f:
                raw_map = json.load(f)
                self._class_map = {int(k): v for k, v in raw_map.items()}
        except Exception as e:
            error_msg = f"Failed to parse class mapping from {CLASS_NAMES_FILE}: {e}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        # 2. Load trained Keras model
        if not MODEL_PATH.exists():
            error_msg = f"Trained AI model binary not found at: {MODEL_PATH}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        try:
            import tensorflow as tf
            from tensorflow.keras.models import load_model

            logger.info(f"[AI] Loading trained model from {MODEL_PATH}...")
            self._model = load_model(str(MODEL_PATH))
            
            # Verify class alignment
            num_classes = len(self._class_map)
            model_outputs = self._model.output_shape[-1]
            if model_outputs != num_classes:
                error_msg = (
                    f"Model output mismatch! Model has {model_outputs} outputs, "
                    f"but class mapping has {num_classes} classes."
                )
                logger.error(error_msg)
                raise ValueError(error_msg)

            self._initialized = True
            logger.info(f"[AI] Model successfully initialized with {num_classes} classes. Output shape: {self._model.output_shape}")

        except Exception as e:
            error_msg = f"Failed to load AI model: {e}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

    @property
    def is_ready(self) -> bool:
        return self._initialized and self._model is not None and self._class_map is not None

    def validate_image_file(self, image_file_or_path: Union[str, Path, Any]) -> tuple[bool, Optional[str]]:
        """Validate format, readability, and content of uploaded file."""
        try:
            if hasattr(image_file_or_path, "name"):
                ext = Path(image_file_or_path.name).suffix.lower()
                if ext not in ALLOWED_EXTENSIONS:
                    return False, f"Unsupported file type ({ext}). Allowed formats: JPG, JPEG, PNG, WEBP."

            # Open image via PIL to verify validity
            if hasattr(image_file_or_path, "read"):
                # File-like object (Django UploadedFile or BytesIO)
                pos = image_file_or_path.tell() if hasattr(image_file_or_path, "tell") else None
                try:
                    img = Image.open(image_file_or_path)
                    img.verify()
                finally:
                    if pos is not None and hasattr(image_file_or_path, "seek"):
                        image_file_or_path.seek(pos)
            else:
                # File path string or Path
                img_path = Path(image_file_or_path)
                if not img_path.exists():
                    return False, "Uploaded image file does not exist on disk."
                img = Image.open(img_path)
                img.verify()

            return True, None

        except UnidentifiedImageError:
            return False, "Unsupported or corrupted image file. Please upload a valid image."
        except Exception as e:
            return False, f"Unable to read the uploaded image: {e}"

    def predict(
        self,
        image_file_or_path: Union[str, Path, Any],
        confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD
    ) -> Dict[str, Any]:
        """
        Run end-to-end inference on a plant leaf image.

        Returns:
            Dict containing prediction status, top class, confidence, top 3 predictions,
            and confidence status message.
        """
        # Ensure model is ready
        if not self.is_ready:
            try:
                self.initialize()
            except Exception as e:
                logger.error(f"[AI] Initialization failed on predict call: {e}")
                return {
                    "success": False,
                    "error": "AI model is currently unavailable. Please check model files or contact administrator."
                }

        # Validate image
        is_valid, validation_err = self.validate_image_file(image_file_or_path)
        if not is_valid:
            return {
                "success": False,
                "error": validation_err
            }

        try:
            # 1. Load image and convert to RGB
            if hasattr(image_file_or_path, "read"):
                if hasattr(image_file_or_path, "seek"):
                    image_file_or_path.seek(0)
                img = Image.open(image_file_or_path).convert("RGB")
            else:
                img = Image.open(str(image_file_or_path)).convert("RGB")

            # 2. Resize to 224x224
            img_resized = img.resize(IMAGE_SIZE, Image.Resampling.BILINEAR)

            # 3. Convert to numpy array & batch format [0, 255] float32
            img_array = np.array(img_resized, dtype=np.float32)
            img_batch = np.expand_dims(img_array, axis=0)

            # 4. Model Inference (model internally performs MobileNetV2 preprocessing)
            predictions = self._model.predict(img_batch, verbose=0)[0]

            # 6. Extract Top Prediction & Confidence
            top_idx = int(np.argmax(predictions))
            top_prob = float(predictions[top_idx])
            top_conf_percent = round(top_prob * 100, 2)
            predicted_class_name = self._class_map.get(top_idx, f"Class #{top_idx}")

            # 7. Extract Top 3 Predictions
            top_3_indices = np.argsort(predictions)[-3:][::-1]
            top_3_predictions = [
                {
                    "class_index": int(idx),
                    "class_name": self._class_map.get(int(idx), f"Class #{idx}"),
                    "confidence_percent": round(float(predictions[idx]) * 100, 2),
                    "probability": float(predictions[idx])
                }
                for idx in top_3_indices
            ]

            # 8. Check Confidence Threshold
            is_confident = top_prob >= confidence_threshold
            if is_confident:
                status_message = "Prediction Successful"
            else:
                status_message = (
                    "Unable to confidently identify the plant disease. "
                    "Please upload a clear, focused image of a single plant leaf."
                )

            logger.info(
                f"[AI] Prediction: '{predicted_class_name}' | "
                f"Confidence: {top_conf_percent}% | "
                f"Threshold: {confidence_threshold * 100:.1f}% | "
                f"Status: {'Confident' if is_confident else 'Low Confidence'}"
            )

            return {
                "success": True,
                "predicted_class": predicted_class_name,
                "confidence_percent": top_conf_percent,
                "probability": top_prob,
                "is_confident": is_confident,
                "status_message": status_message,
                "threshold_percent": round(confidence_threshold * 100, 1),
                "top_predictions": top_3_predictions
            }

        except Exception as e:
            logger.exception(f"[AI] Unexpected error during prediction: {e}")
            return {
                "success": False,
                "error": f"An error occurred during AI inference: {str(e)}"
            }


# Global predictor instance
_global_predictor: Optional[PlantDiseasePredictor] = None


def get_predictor() -> PlantDiseasePredictor:
    """Get or initialize the global predictor instance."""
    global _global_predictor
    if _global_predictor is None:
        _global_predictor = PlantDiseasePredictor()
    return _global_predictor


def predict_disease(
    image_file_or_path: Union[str, Path, Any],
    confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD
) -> Dict[str, Any]:
    """Convenience function to predict plant disease from an image."""
    predictor = get_predictor()
    return predictor.predict(image_file_or_path, confidence_threshold=confidence_threshold)
