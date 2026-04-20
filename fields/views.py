from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Count
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Field, FieldUpdate
from .forms import FieldForm, FieldUpdateForm

def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Admin').exists()

def is_agent(user):
    return user.groups.filter(name='Field Agent').exists()

@login_required
def field_list(request):
    if is_admin(request.user):
        fields = Field.objects.all().select_related('assigned_agent', 'created_by')
    else:
        fields = Field.objects.filter(assigned_agent=request.user)
    
    for field in fields:
        field.status = field.calculate_status()
    
    return render(request, 'fields/list.html', {'fields': fields})

@login_required
@user_passes_test(is_admin)
def field_create(request):
    if request.method == 'POST':
        form = FieldForm(request.POST, request.FILES)
        if form.is_valid():
            field = form.save(commit=False)
            field.created_by = request.user
            field.save()
            messages.success(request, 'Field created successfully!')
            return redirect('fields:field_list')
    else:
        form = FieldForm()
    
    return render(request, 'fields/form.html', {'form': form, 'title': 'Create Field'})

@login_required
def field_detail(request, pk):
    field = get_object_or_404(Field, pk=pk)
    
    if not (is_admin(request.user) or field.assigned_agent == request.user):
        messages.error(request, 'You do not have permission to view this field.')
        return redirect('dashboard')
    
    field.status = field.calculate_status()
    updates = field.updates.all()[:10]
    
    available_agents = []
    if is_admin(request.user):
        available_agents = User.objects.filter(groups__name='Field Agent').annotate(
            assigned_fields_count=Count('assigned_fields')
        )
    
    if request.method == 'POST' and not is_admin(request.user):
        form = FieldUpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.field = field
            update.agent = request.user
            update.save()
            
            field.current_stage = update.stage
            field.save()
            
            messages.success(request, 'Field update added successfully!')
            return redirect('fields:field_detail', pk=field.pk)
    else:
        form = FieldUpdateForm() if not is_admin(request.user) else None
    
    return render(request, 'fields/detail.html', {
        'field': field,
        'updates': updates,
        'form': form,
        'available_agents': available_agents,
    })

@login_required
@user_passes_test(is_admin)
def field_edit(request, pk):
    field = get_object_or_404(Field, pk=pk)
    
    if request.method == 'POST':
        form = FieldForm(request.POST, request.FILES, instance=field)
        if form.is_valid():
            form.save()
            messages.success(request, 'Field updated successfully!')
            return redirect('fields:field_detail', pk=field.pk)
    else:
        form = FieldForm(instance=field)
    
    return render(request, 'fields/form.html', {'form': form, 'title': 'Edit Field'})

@login_required
@user_passes_test(is_admin)
def field_delete(request, pk):
    field = get_object_or_404(Field, pk=pk)
    
    if request.method == 'POST':
        field.delete()
        messages.success(request, 'Field deleted successfully!')
        return redirect('fields:field_list')
    
    return render(request, 'fields/confirm_delete.html', {'field': field})

@login_required
@user_passes_test(is_admin)
def assign_agent(request):
    if request.method == 'POST':
        agent_id = request.POST.get('agent_id')
        field_id = request.POST.get('field_id')
        
        try:
            agent = User.objects.get(id=agent_id)
            field = Field.objects.get(id=field_id)
            previous_agent = field.assigned_agent
            
            field.assigned_agent = agent
            field.save()
            
            if previous_agent:
                messages.success(request, f'Field "{field.name}" has been reassigned from {previous_agent.username} to {agent.username}!')
            else:
                messages.success(request, f'Field "{field.name}" has been assigned to {agent.username}!')
                
        except User.DoesNotExist:
            messages.error(request, 'Agent not found.')
        except Field.DoesNotExist:
            messages.error(request, 'Field not found.')
        
        next_url = request.POST.get('next', reverse('dashboard'))
        return redirect(next_url)

@login_required
@user_passes_test(is_admin)
def unassign_agent(request, field_id):
    try:
        field = Field.objects.get(id=field_id)
        previous_agent = field.assigned_agent
        
        if previous_agent:
            field.assigned_agent = None
            field.save()
            messages.success(request, f'Agent "{previous_agent.username}" has been unassigned from field "{field.name}".')
        else:
            messages.warning(request, f'Field "{field.name}" already has no agent assigned.')
            
    except Field.DoesNotExist:
        messages.error(request, 'Field not found.')
    
    return redirect('fields:field_detail', pk=field_id)