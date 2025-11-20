"""Views for games app."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.utils import timezone
from .models import Game, Guess
from .forms import GameDifficultyForm, GuessForm
from users.models import UserProfile


@login_required
def game_create_view(request):
    """View for creating a new game."""
    if request.method == 'POST':
        form = GameDifficultyForm(request.POST)
        if form.is_valid():
            difficulty = form.cleaned_data['difficulty']
            game = Game.create_game(request.user, difficulty)
            messages.success(request, f'Game started! Difficulty: {game.get_difficulty_level_display()}')
            return redirect('games:game_play', pk=game.pk)
    else:
        form = GameDifficultyForm()
    
    return render(request, 'games/game_new.html', {'form': form})


@login_required
def game_play_view(request, pk):
    """View for playing a game."""
    game = get_object_or_404(Game, pk=pk, user=request.user)
    
    # Check if game is already over
    if game.is_game_over():
        return redirect('games:game_result', pk=game.pk)
    
    if request.method == 'POST':
        form = GuessForm(request.POST, game=game)
        if form.is_valid():
            guess_value = form.cleaned_data['guess']
            feedback = game.check_guess(guess_value)
            
            # Create guess record
            Guess.objects.create(
                game=game,
                guess_number=guess_value,
                attempt_number=game.attempts_made,
                feedback=feedback
            )
            
            if feedback == 'correct':
                # Update user profile stats
                profile = request.user.profile
                profile.total_games_played += 1
                profile.total_wins += 1
                profile.update_best_score(game.score, game.difficulty_level)
                profile.save()
                
                messages.success(request, f'Congratulations! You won with a score of {game.score}!')
                return redirect('games:game_result', pk=game.pk)
            elif game.is_game_over():
                # Game over - no more attempts
                profile = request.user.profile
                profile.total_games_played += 1
                profile.save()
                
                messages.warning(request, 'Game over! You ran out of attempts.')
                return redirect('games:game_result', pk=game.pk)
            else:
                # Continue game
                feedback_msg = 'Too high!' if feedback == 'too_high' else 'Too low!'
                messages.info(request, f'{feedback_msg} Try again.')
                return redirect('games:game_play', pk=game.pk)
    else:
        form = GuessForm(game=game)
    
    # Get previous guesses
    guesses = game.guesses.all().order_by('attempt_number')
    
    min_val, max_val = game.get_range()
    
    context = {
        'game': game,
        'form': form,
        'guesses': guesses,
        'remaining_attempts': game.get_remaining_attempts(),
        'min_val': min_val,
        'max_val': max_val,
    }
    
    return render(request, 'games/game_play.html', context)


class GameResultView(DetailView):
    """View for displaying game results."""
    model = Game
    template_name = 'games/game_result.html'
    context_object_name = 'game'

    def dispatch(self, request, *args, **kwargs):
        """Ensure user owns the game."""
        game = self.get_object()
        if game.user != request.user:
            messages.error(request, 'You do not have permission to view this game.')
            return redirect('core:home')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Add additional context data."""
        context = super().get_context_data(**kwargs)
        game = self.get_object()
        context['guesses'] = game.guesses.all().order_by('attempt_number')
        return context


class LeaderboardView(ListView):
    """Leaderboard view."""
    model = Game
    template_name = 'games/leaderboard.html'
    context_object_name = 'games'
    paginate_by = 20

    def get_queryset(self):
        """Get queryset filtered by difficulty if provided."""
        queryset = Game.objects.filter(
            is_won=True,
            score__isnull=False
        ).select_related('user').order_by('-score', 'attempts_made', 'started_at')
        
        difficulty = self.kwargs.get('difficulty')
        if difficulty and difficulty in dict(Game.DIFFICULTY_CHOICES):
            queryset = queryset.filter(difficulty_level=difficulty)
        
        return queryset

    def get_context_data(self, **kwargs):
        """Add additional context data."""
        context = super().get_context_data(**kwargs)
        context['difficulty'] = self.kwargs.get('difficulty')
        context['difficulty_choices'] = Game.DIFFICULTY_CHOICES
        
        # Add rank numbers
        for idx, game in enumerate(context['games'], start=1):
            game.rank = (context['page_obj'].number - 1) * self.paginate_by + idx
        
        return context
