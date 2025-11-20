"""Views for users app."""
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, ProfileEditForm
from .models import UserProfile
from games.models import Game


class CustomLoginView(LoginView):
    """Custom login view."""
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        """Handle successful login."""
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    """Custom logout view."""
    next_page = '/'
    
    def dispatch(self, request, *args, **kwargs):
        """Handle logout."""
        messages.success(request, 'You have been logged out successfully.')
        return super().dispatch(request, *args, **kwargs)


def register_view(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('users:login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})


class ProfileView(DetailView):
    """User profile view."""
    model = UserProfile
    template_name = 'users/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        """Get user's profile."""
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        """Add additional context data."""
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        
        # Get recent games
        recent_games = Game.objects.filter(user=self.request.user).select_related('user')[:10]
        context['recent_games'] = recent_games
        
        # Calculate average attempts per win
        won_games = Game.objects.filter(user=self.request.user, is_won=True)
        if won_games.exists():
            total_attempts = sum(game.attempts_made for game in won_games)
            context['avg_attempts_per_win'] = round(total_attempts / won_games.count(), 2)
        else:
            context['avg_attempts_per_win'] = 0
        
        return context


class ProfileEditView(UpdateView):
    """Profile edit view."""
    form_class = ProfileEditForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        """Get user object."""
        return self.request.user

    def form_valid(self, form):
        """Handle successful form submission."""
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)
