from django.urls import path
from . import views

app_name = 'fields'

urlpatterns = [
    path('', views.field_list, name='field_list'),
    path('create/', views.field_create, name='field_create'),
    path('<int:pk>/', views.field_detail, name='field_detail'),
    path('<int:pk>/edit/', views.field_edit, name='field_edit'),
    path('<int:pk>/delete/', views.field_delete, name='field_delete'),
    path('assign-agent/', views.assign_agent, name='assign_agent'),
    path('<int:field_id>/unassign/', views.unassign_agent, name='unassign_agent'),  # Add this
]