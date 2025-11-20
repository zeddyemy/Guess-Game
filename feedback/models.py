"""Feedback models for the guessing game application."""
from django.db import models
from django.contrib.auth.models import User


class Feedback(models.Model):
    """User feedback model."""
    
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedbacks')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    is_reviewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta options for Feedback."""
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['is_reviewed', '-created_at']),
            models.Index(fields=['rating', '-created_at']),
        ]

    def __str__(self) -> str:
        """String representation of Feedback."""
        return f"Feedback from {self.name} - {self.subject} ({self.rating} stars)"
