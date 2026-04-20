from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from cloudinary.models import CloudinaryField  # Add this import

class Field(models.Model):
    CROP_TYPES = [
        ('corn', 'Corn'),
        ('wheat', 'Wheat'),
        ('soybean', 'Soybean'),
        ('rice', 'Rice'),
        ('cotton', 'Cotton'),
        ('other', 'Other'),
    ]
    
    STAGE_CHOICES = [
        ('planted', 'Planted'),
        ('growing', 'Growing'),
        ('ready', 'Ready'),
        ('harvested', 'Harvested'),
    ]
    
    name = models.CharField(max_length=100)
    crop_type = models.CharField(max_length=20, choices=CROP_TYPES)
    planting_date = models.DateField()
    current_stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='planted')
    assigned_agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_fields')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_fields')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Use CloudinaryField instead of ImageField
    image = CloudinaryField(
        'image',
        folder='field_images/',
        blank=True,
        null=True,
        help_text="Upload a photo of the field"
    )
    
    def calculate_status(self):
        """Calculate field status based on stage and planting date"""
        days_since_planting = (timezone.now().date() - self.planting_date).days
        
        if self.current_stage == 'harvested':
            return 'completed'
        
        if self.current_stage == 'planted' and days_since_planting > 30:
            return 'at_risk'
        elif self.current_stage == 'growing' and days_since_planting > 90:
            return 'at_risk'
        elif self.current_stage == 'ready' and days_since_planting > 120:
            return 'at_risk'
        
        return 'active'
    
    def __str__(self):
        return self.name

class FieldUpdate(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='updates')
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    stage = models.CharField(max_length=20, choices=Field.STAGE_CHOICES)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.field.name} - {self.stage} by {self.agent.username}"