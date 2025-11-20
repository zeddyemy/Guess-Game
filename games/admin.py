"""Admin configuration for games app."""
from django.contrib import admin
from .models import Game, Guess


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """Admin configuration for Game model."""
    list_display = ('id', 'user', 'difficulty_level', 'target_number', 
                    'attempts_made', 'max_attempts', 'score', 'is_won', 'started_at')
    list_filter = ('difficulty_level', 'is_won', 'started_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('started_at', 'completed_at', 'score')
    date_hierarchy = 'started_at'
    
    fieldsets = (
        ('Game Info', {
            'fields': ('user', 'difficulty_level', 'target_number')
        }),
        ('Progress', {
            'fields': ('attempts_made', 'max_attempts', 'is_won')
        }),
        ('Results', {
            'fields': ('score', 'started_at', 'completed_at')
        }),
    )


@admin.register(Guess)
class GuessAdmin(admin.ModelAdmin):
    """Admin configuration for Guess model."""
    list_display = ('id', 'game', 'guess_number', 'attempt_number', 'feedback', 'created_at')
    list_filter = ('feedback', 'created_at')
    search_fields = ('game__user__username', 'guess_number')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
