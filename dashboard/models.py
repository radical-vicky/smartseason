from django.db import models
from django.contrib.auth.models import User
from fields.models import Field, FieldUpdate

class DashboardPreference(models.Model):
    """Store user dashboard preferences and settings"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dashboard_preferences')
    default_view = models.CharField(max_length=20, choices=[
        ('grid', 'Grid View'),
        ('list', 'List View'),
        ('table', 'Table View'),
    ], default='grid')
    show_widgets = models.JSONField(default=dict, blank=True)
    theme = models.CharField(max_length=20, choices=[
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('auto', 'Auto'),
    ], default='light')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Dashboard Preferences"
    
    class Meta:
        verbose_name = 'Dashboard Preference'
        verbose_name_plural = 'Dashboard Preferences'

class DashboardWidget(models.Model):
    """Customizable dashboard widgets"""
    WIDGET_TYPES = [
        ('field_summary', 'Field Summary'),
        ('recent_updates', 'Recent Updates'),
        ('status_chart', 'Status Chart'),
        ('crop_distribution', 'Crop Distribution'),
        ('agent_performance', 'Agent Performance'),
        ('alerts', 'Alerts & Warnings'),
        ('calendar', 'Calendar'),
        ('tasks', 'Tasks'),
    ]
    
    name = models.CharField(max_length=100)
    widget_type = models.CharField(max_length=50, choices=WIDGET_TYPES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboard_widgets')
    position = models.IntegerField(default=0)
    is_visible = models.BooleanField(default=True)
    settings = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"
    
    class Meta:
        ordering = ['position']
        verbose_name = 'Dashboard Widget'
        verbose_name_plural = 'Dashboard Widgets'

class DashboardMetric(models.Model):
    """Track historical dashboard metrics for analytics"""
    METRIC_TYPES = [
        ('total_fields', 'Total Fields'),
        ('active_fields', 'Active Fields'),
        ('at_risk_fields', 'At Risk Fields'),
        ('completed_fields', 'Completed Fields'),
        ('total_updates', 'Total Updates'),
        ('active_agents', 'Active Agents'),
    ]
    
    metric_type = models.CharField(max_length=50, choices=METRIC_TYPES)
    value = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_metric_type_display()}: {self.value} on {self.date}"
    
    class Meta:
        ordering = ['-date']
        verbose_name = 'Dashboard Metric'
        verbose_name_plural = 'Dashboard Metrics'
        unique_together = ['metric_type', 'date']

class Notification(models.Model):
    """System notifications for users"""
    NOTIFICATION_TYPES = [
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('alert', 'Alert'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='info')
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    def mark_as_read(self):
        from django.utils import timezone
        self.is_read = True
        self.read_at = timezone.now()
        self.save()
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

class UserActivity(models.Model):
    """Track user activity for analytics and auditing"""
    ACTIVITY_TYPES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('create_field', 'Create Field'),
        ('update_field', 'Update Field'),
        ('delete_field', 'Delete Field'),
        ('add_update', 'Add Field Update'),
        ('view_dashboard', 'View Dashboard'),
        ('export_data', 'Export Data'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_activity_type_display()} at {self.created_at}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User Activity'
        verbose_name_plural = 'User Activities'

class Report(models.Model):
    """Saved reports and exports"""
    REPORT_TYPES = [
        ('field_summary', 'Field Summary Report'),
        ('agent_performance', 'Agent Performance Report'),
        ('crop_analysis', 'Crop Analysis Report'),
        ('status_report', 'Status Report'),
        ('custom', 'Custom Report'),
    ]
    
    name = models.CharField(max_length=200)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    filters = models.JSONField(default=dict)
    data = models.JSONField(default=dict, blank=True)
    file = models.FileField(upload_to='reports/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.created_by.username}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'