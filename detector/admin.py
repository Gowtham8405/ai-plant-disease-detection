from django.contrib import admin
from .models import PlantLeafUpload, PredictionHistory


@admin.register(PlantLeafUpload)
class PlantLeafUploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'uploaded_at')
    list_filter = ('uploaded_at',)
    ordering = ('-uploaded_at',)


@admin.register(PredictionHistory)
class PredictionHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'plant_name', 'disease_name', 'confidence_percent', 'is_confident', 'created_at')
    list_filter = ('is_confident', 'is_healthy', 'plant_name', 'created_at')
    search_fields = ('user__username', 'plant_name', 'disease_name', 'full_class_name')
    ordering = ('-created_at',)

