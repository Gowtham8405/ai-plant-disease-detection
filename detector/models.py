from django.db import models
from django.contrib.auth.models import User


class PlantLeafUpload(models.Model):
    """
    Model to store uploaded plant leaf images for disease detection.
    This model holds the uploaded image and metadata, ready for future AI inference integration.
    """
    image = models.ImageField(
        upload_to='leaf_images/',
        help_text="Upload a clear image of the plant leaf."
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the image was uploaded."
    )

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Plant Leaf Upload"
        verbose_name_plural = "Plant Leaf Uploads"

    def __str__(self):
        return f"Leaf Image #{self.id} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"


class PredictionHistory(models.Model):
    """
    Stores prediction history for authenticated users.
    Provides complete record isolation per user.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='predictions',
        help_text="The authenticated user who requested this prediction."
    )
    image = models.ImageField(
        upload_to='prediction_history/',
        help_text="Copy or reference of the diagnosed leaf image."
    )
    plant_name = models.CharField(
        max_length=100,
        help_text="Identified crop or plant species."
    )
    disease_name = models.CharField(
        max_length=150,
        help_text="Identified disease name or Healthy status."
    )
    full_class_name = models.CharField(
        max_length=200,
        help_text="Normalized model class label."
    )
    confidence_percent = models.FloatField(
        help_text="Prediction confidence percentage (0-100%)."
    )
    is_confident = models.BooleanField(
        default=True,
        help_text="Whether prediction met or exceeded confidence threshold."
    )
    is_healthy = models.BooleanField(
        default=False,
        help_text="True if the identified class is healthy."
    )
    status_message = models.CharField(
        max_length=255,
        help_text="Status or warning message from AI predictor."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the prediction was performed."
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Prediction History"
        verbose_name_plural = "Prediction Histories"

    def __str__(self):
        return f"{self.user.username} - {self.full_class_name} ({self.confidence_percent}%)"

