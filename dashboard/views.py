from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from fields.models import Field, FieldUpdate

@login_required
def dashboard(request):
    context = {}
    
    # Check if user is admin
    is_admin_user = request.user.is_superuser or request.user.groups.filter(name='Admin').exists()
    is_agent_user = request.user.groups.filter(name='Field Agent').exists()
    
    if is_admin_user:
        fields = Field.objects.all()
        total_fields = fields.count()
        
        status_counts = {'active': 0, 'at_risk': 0, 'completed': 0}
        for field in fields:
            status = field.calculate_status()
            status_counts[status] = status_counts.get(status, 0) + 1
        
        recent_updates = FieldUpdate.objects.select_related('field', 'agent').all()[:10]
        crop_counts = fields.values('crop_type').annotate(count=Count('id'))
        at_risk_fields = [field for field in fields if field.calculate_status() == 'at_risk']
        available_agents = User.objects.filter(groups__name='Field Agent').annotate(
            assigned_fields_count=Count('assigned_fields')
        )
        unassigned_fields = Field.objects.filter(assigned_agent__isnull=True)
        
        context.update({
            'total_fields': total_fields,
            'status_counts': status_counts,
            'recent_updates': recent_updates,
            'crop_counts': crop_counts,
            'fields': fields[:10],
            'at_risk_count': len(at_risk_fields),
            'at_risk_fields': at_risk_fields[:5],
            'available_agents': available_agents,
            'unassigned_count': unassigned_fields.count(),
            'is_admin': True,
        })
    else:
        assigned_fields = Field.objects.filter(assigned_agent=request.user)
        total_fields = assigned_fields.count()
        
        status_counts = {'active': 0, 'at_risk': 0, 'completed': 0}
        for field in assigned_fields:
            status = field.calculate_status()
            status_counts[status] = status_counts.get(status, 0) + 1
        
        recent_updates = FieldUpdate.objects.filter(agent=request.user).select_related('field')[:10]
        at_risk_fields = [field for field in assigned_fields if field.calculate_status() == 'at_risk']
        
        needs_update = []
        for field in assigned_fields:
            last_update = field.updates.first()
            if not last_update or last_update.created_at.date() < datetime.now().date() - timedelta(days=14):
                needs_update.append(field)
        
        context.update({
            'total_fields': total_fields,
            'status_counts': status_counts,
            'assigned_fields': assigned_fields,
            'recent_updates': recent_updates,
            'at_risk_count': len(at_risk_fields),
            'at_risk_fields': at_risk_fields[:5],
            'needs_update_count': len(needs_update),
            'needs_update_fields': needs_update[:5],
            'is_agent': True,
        })
    
    return render(request, 'dashboard/index.html', context)


def home_page(request):
    # Fetch dynamic data from database
    total_fields = Field.objects.count()
    total_agents = User.objects.filter(groups__name='Field Agent').count()
    active_fields = 0
    at_risk_fields = 0
    completed_fields = 0
    
    for field in Field.objects.all():
        status = field.calculate_status()
        if status == 'active':
            active_fields += 1
        elif status == 'at_risk':
            at_risk_fields += 1
        elif status == 'completed':
            completed_fields += 1
    
    # Get recent fields
    recent_fields = Field.objects.order_by('-created_at')[:3]
    
    context = {
        'total_fields': total_fields,
        'total_agents': total_agents,
        'active_fields': active_fields,
        'at_risk_fields': at_risk_fields,
        'completed_fields': completed_fields,
        'recent_fields': recent_fields,
    }
    return render(request, 'home.html', context)