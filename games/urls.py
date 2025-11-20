"""URL configuration for games app."""
from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('game/new/', views.game_create_view, name='game_new'),
    path('game/<int:pk>/play/', views.game_play_view, name='game_play'),
    path('game/<int:pk>/result/', views.GameResultView.as_view(), name='game_result'),
    path('leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
    path('leaderboard/<str:difficulty>/', views.LeaderboardView.as_view(), name='leaderboard_filtered'),
]

