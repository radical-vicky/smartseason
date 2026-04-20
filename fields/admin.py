from django.contrib import admin
from .models import Field, FieldUpdate

@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ['name', 'crop_type', 'current_stage', 'assigned_agent', 'get_status', 'created_at']
    list_filter = ['crop_type', 'current_stage', 'assigned_agent', 'created_at']
    search_fields = ['name', 'assigned_agent__username']
    date_hierarchy = 'created_at'
    
    def get_status(self, obj):
        status = obj.calculate_status()
        if status == 'active':
            return '🟢 Active'
        elif status == 'at_risk':
            return '🔴 At Risk'
        else:
            return '⚫ Completed'
    get_status.short_description = 'Status'

@admin.register(FieldUpdate)
class FieldUpdateAdmin(admin.ModelAdmin):
    list_display = ['field', 'agent', 'stage', 'created_at']
    list_filter = ['stage', 'created_at', 'agent']
    search_fields = ['field__name', 'agent__username', 'notes']
    date_hierarchy = 'created_at'