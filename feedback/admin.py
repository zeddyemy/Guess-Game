"""Admin configuration for feedback app."""
from django.contrib import admin
from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """Admin configuration for Feedback model."""
    list_display = ('id', 'name', 'email', 'subject', 'rating', 'is_reviewed', 'created_at')
    list_filter = ('rating', 'is_reviewed', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    list_editable = ('is_reviewed',)
    
    fieldsets = (
        ('User Info', {
            'fields': ('user', 'name', 'email')
        }),
        ('Feedback', {
            'fields': ('subject', 'message', 'rating')
        }),
        ('Status', {
            'fields': ('is_reviewed', 'created_at')
        }),
    )
