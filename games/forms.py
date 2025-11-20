"""Forms for games app."""
from django import forms
from .models import Game


class GameDifficultyForm(forms.Form):
    """Form for selecting game difficulty."""
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy (1-99)'),
        ('moderate', 'Moderate (1-999)'),
        ('expert', 'Expert (1-9999)'),
    ]
    
    difficulty = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-radio h-4 w-4 text-blue-600 focus:ring-blue-500'
        }),
        label='Select Difficulty Level'
    )


class GuessForm(forms.Form):
    """Form for submitting a guess."""
    guess = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-center text-2xl',
            'placeholder': 'Enter your guess',
            'autofocus': True,
            'min': 1,
        }),
        label='Your Guess'
    )

    def __init__(self, *args, game: Game = None, **kwargs):
        """Initialize form with game context for validation."""
        super().__init__(*args, **kwargs)
        self.game = game
        if game:
            min_val, max_val = game.get_range()
            self.fields['guess'].widget.attrs['min'] = min_val
            self.fields['guess'].widget.attrs['max'] = max_val

    def clean_guess(self) -> int:
        """Validate guess is within range."""
        guess = self.cleaned_data.get('guess')
        if self.game:
            min_val, max_val = self.game.get_range()
            if guess < min_val or guess > max_val:
                raise forms.ValidationError(
                    f"Guess must be between {min_val} and {max_val} for {self.game.get_difficulty_level_display()} difficulty."
                )
        return guess


