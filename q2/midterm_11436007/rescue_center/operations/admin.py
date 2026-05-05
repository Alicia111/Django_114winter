from django.contrib import admin
from .models import Incident, ResourceRequest, ActionLog


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'category', 'priority', 'location', 'reporter', 'is_active', 'created_at']
    list_filter = ['category', 'priority', 'is_active']
    search_fields = ['title', 'location', 'description']


@admin.register(ResourceRequest)
class ResourceRequestAdmin(admin.ModelAdmin):
    list_display = ['pk', 'incident', 'item_name', 'quantity', 'status', 'is_urgent', 'requested_by']
    list_filter = ['status', 'is_urgent']
    search_fields = ['item_name']


@admin.register(ActionLog)
class ActionLogAdmin(admin.ModelAdmin):
    list_display = ['pk', 'incident', 'actor', 'note', 'created_at']
    list_filter = ['incident']
    search_fields = ['note']
