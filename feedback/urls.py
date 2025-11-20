"""URL configuration for feedback app."""
from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('feedback/', views.FeedbackCreateView.as_view(), name='feedback'),
]


