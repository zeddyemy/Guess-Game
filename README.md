# Number Guessing Game - Django Web Application

A full-featured web-based Number Guessing Game built with Django. Players guess randomly generated numbers within defined ranges, compete on leaderboards, and track their progress.

## Features

- **User Authentication**: Secure registration, login, and profile management
- **Multiple Difficulty Levels**: Easy (1-99), Moderate (1-999), Expert (1-9999)
- **Scoring System**: Points based on attempts used and difficulty level
- **Leaderboard**: Global rankings filtered by difficulty
- **User Profiles**: Track games played, wins, best scores, and statistics
- **Feedback System**: Submit feedback and ratings
- **Admin Panel**: Comprehensive management interface
- **Responsive Design**: Mobile-first design with Tailwind CSS

## Technology Stack

- **Framework**: Django 5.2.8+
- **Package Manager**: UV
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: Django Templates, HTML5, Tailwind CSS, JavaScript
- **Authentication**: Django's built-in session-based authentication

## Prerequisites

- Python 3.12+
- UV package manager

## Installation

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd the_guess_game
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Run migrations**:
   ```bash
   uv run python manage.py migrate
   ```

4. **Create a superuser** (optional, for admin access):
   ```bash
   uv run python manage.py createsuperuser
   ```

5. **Run the development server**:
   ```bash
   uv run python manage.py runserver
   ```

6. **Access the application**:
   - Home: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## Project Structure

```
the_guess_game/
├── core/           # Core app (home, contact pages)
├── users/          # User authentication and profiles
├── games/          # Game logic, models, views
├── feedback/       # Feedback submission system
├── templates/      # HTML templates
├── static/         # Static files (CSS, JS, images)
├── the_guess_game/ # Project settings
└── manage.py       # Django management script
```

## Usage

1. **Register an account** or **login** if you already have one
2. **Start a new game** by selecting a difficulty level
3. **Make guesses** and receive feedback (Too High, Too Low, or Correct!)
4. **Win games** to earn points and climb the leaderboard
5. **View your profile** to see statistics and game history
6. **Check the leaderboard** to see top players

## Scoring Algorithm

- Base Score: `(Max Attempts - Attempts Used + 1) × 100`
- Difficulty Multipliers:
  - Easy: 1x
  - Moderate: 2x
  - Expert: 3x
- Final Score: `Base Score × Difficulty Multiplier`

## Development

### Running Tests
```bash
uv run python manage.py test
```

### Creating Migrations
```bash
uv run python manage.py makemigrations
```

### Applying Migrations
```bash
uv run python manage.py migrate
```

### Collecting Static Files
```bash
uv run python manage.py collectstatic
```

## Configuration

### Environment Variables

For production, set these environment variables:

- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: Database connection string (for PostgreSQL)

### Email Configuration

Update `settings.py` to configure email backend for production:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

## Deployment

1. Set `DEBUG = False` in `settings.py`
2. Configure `ALLOWED_HOSTS`
3. Set up a production database (PostgreSQL recommended)
4. Configure static file serving
5. Set up a WSGI server (Gunicorn recommended)
6. Configure environment variables
7. Run `collectstatic` to gather static files

## License

This project is part of a semester assignment.

## Contributing

This is an educational project. Feel free to fork and modify for learning purposes.


