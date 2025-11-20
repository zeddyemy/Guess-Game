"""User profile models for the guessing game application."""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Extended user profile with game statistics."""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    total_games_played = models.IntegerField(default=0)
    total_wins = models.IntegerField(default=0)
    best_score = models.IntegerField(default=0, null=True, blank=True)
    best_score_easy = models.IntegerField(default=0, null=True, blank=True)
    best_score_moderate = models.IntegerField(default=0, null=True, blank=True)
    best_score_expert = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta options for UserProfile."""
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['-best_score']

    def __str__(self) -> str:
        """String representation of UserProfile."""
        return f"{self.user.username}'s Profile"

    @property
    def win_rate(self) -> float:
        """Calculate win rate percentage."""
        if self.total_games_played == 0:
            return 0.0
        return round((self.total_wins / self.total_games_played) * 100, 2)

    def update_best_score(self, score: int, difficulty: str) -> None:
        """Update best score for overall and specific difficulty."""
        if self.best_score is None or score > self.best_score:
            self.best_score = score
        
        difficulty_field = f'best_score_{difficulty.lower()}'
        current_best = getattr(self, difficulty_field)
        if current_best is None or score > current_best:
            setattr(self, difficulty_field, score)
        self.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create UserProfile when a User is created."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save UserProfile when User is saved."""
    if hasattr(instance, 'profile'):
        instance.profile.save()
