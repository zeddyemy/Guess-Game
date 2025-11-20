"""Game models for the guessing game application."""
import random
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Game(models.Model):
    """Game instance model."""
    
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy (1-99)'),
        ('moderate', 'Moderate (1-999)'),
        ('expert', 'Expert (1-9999)'),
    ]
    
    DIFFICULTY_RANGES = {
        'easy': (1, 99),
        'moderate': (1, 999),
        'expert': (1, 9999),
    }
    
    DIFFICULTY_MULTIPLIERS = {
        'easy': 1,
        'moderate': 2,
        'expert': 3,
    }
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games')
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    target_number = models.IntegerField()
    attempts_made = models.IntegerField(default=0)
    max_attempts = models.IntegerField(default=10)
    score = models.IntegerField(null=True, blank=True)
    is_won = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        """Meta options for Game."""
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['user', '-started_at']),
            models.Index(fields=['difficulty_level', '-score']),
            models.Index(fields=['is_won', '-score']),
        ]

    def __str__(self) -> str:
        """String representation of Game."""
        return f"Game {self.id} - {self.user.username} - {self.difficulty_level}"

    @classmethod
    def create_game(cls, user: User, difficulty: str) -> 'Game':
        """Create a new game with random target number."""
        min_val, max_val = cls.DIFFICULTY_RANGES.get(difficulty, (1, 99))
        target = random.randint(min_val, max_val)
        return cls.objects.create(
            user=user,
            difficulty_level=difficulty,
            target_number=target
        )

    def check_guess(self, guess: int) -> str:
        """Check guess against target number and return feedback."""
        # Increment attempts and persist so subsequent requests see the updated
        # attempts_made value. Previously we only saved when the guess was
        # correct which meant the DB value remained stale and all guesses
        # recorded the same attempt number.
        self.attempts_made += 1

        if guess == self.target_number:
            self.is_won = True
            self.completed_at = timezone.now()
            # Calculate score after marking as won (calculate_score checks is_won)
            self.score = self.calculate_score()

        # Always save the increment (and any updated fields) so the next
        # request will read the correct attempts_made from the database.
        self.save()

        if guess == self.target_number:
            return 'correct'
        elif guess > self.target_number:
            return 'too_high'
        else:
            return 'too_low'

    def calculate_score(self) -> int:
        """Calculate score based on attempts and difficulty."""
        if not self.is_won:
            return 0
        
        base_score = (self.max_attempts - self.attempts_made + 1) * 100
        multiplier = self.DIFFICULTY_MULTIPLIERS.get(self.difficulty_level, 1)
        return base_score * multiplier

    def is_game_over(self) -> bool:
        """Check if game is over (won or attempts exhausted)."""
        return self.is_won or self.attempts_made >= self.max_attempts

    def get_remaining_attempts(self) -> int:
        """Get remaining attempts."""
        return max(0, self.max_attempts - self.attempts_made)

    def get_range(self) -> tuple[int, int]:
        """Get the number range for this difficulty."""
        return self.DIFFICULTY_RANGES.get(self.difficulty_level, (1, 99))


class Guess(models.Model):
    """Individual guess record."""
    
    FEEDBACK_CHOICES = [
        ('too_high', 'Too High'),
        ('too_low', 'Too Low'),
        ('correct', 'Correct'),
    ]
    
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='guesses')
    guess_number = models.IntegerField()
    attempt_number = models.IntegerField()
    feedback = models.CharField(max_length=20, choices=FEEDBACK_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta options for Guess."""
        ordering = ['attempt_number']
        indexes = [
            models.Index(fields=['game', 'attempt_number']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self) -> str:
        """String representation of Guess."""
        return f"Guess {self.guess_number} (Attempt {self.attempt_number}) - {self.feedback}"
