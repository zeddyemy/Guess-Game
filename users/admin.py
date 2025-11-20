"""Admin configuration for users app."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    """Inline admin for UserProfile."""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('total_games_played', 'total_wins', 'best_score', 
              'best_score_easy', 'best_score_moderate', 'best_score_expert', 
              'win_rate', 'created_at', 'updated_at')
    readonly_fields = ('win_rate', 'created_at', 'updated_at')


class UserAdmin(BaseUserAdmin):
    """Custom User admin with profile inline."""
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'is_active', 'date_joined', 'get_total_games')
    
    def get_total_games(self, obj):
        """Get total games played by user."""
        return obj.profile.total_games_played if hasattr(obj, 'profile') else 0
    get_total_games.short_description = 'Games Played'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
