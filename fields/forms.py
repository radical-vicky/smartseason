from django import forms
from .models import Field, FieldUpdate
from django.contrib.auth.models import User

class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ['name', 'crop_type', 'planting_date', 'current_stage', 'assigned_agent', 'image']
        widgets = {
            'planting_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'crop_type': forms.Select(attrs={'class': 'form-input'}),
            'current_stage': forms.Select(attrs={'class': 'form-input'}),
            'assigned_agent': forms.Select(attrs={'class': 'form-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-input', 'accept': 'image/*'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_agent'].queryset = User.objects.filter(groups__name='Field Agent')
        self.fields['assigned_agent'].required = False
        self.fields['assigned_agent'].empty_label = "Unassigned"
        self.fields['image'].required = False

class FieldUpdateForm(forms.ModelForm):
    class Meta:
        model = FieldUpdate
        fields = ['stage', 'notes']
        widgets = {
            'stage': forms.Select(attrs={'class': 'form-input'}),
            'notes': forms.Textarea(attrs={'rows': 4, 'class': 'form-input', 'placeholder': 'Enter your observations here...'}),
        }
        labels = {
            'stage': 'Update Stage',
            'notes': 'Observations/Notes',
        }