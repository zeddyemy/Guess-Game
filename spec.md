# Number Guessing Game - Django Web Application Specification

## Project Overview

Build a full-featured web-based Number Guessing Game using Django. The application provides an engaging gaming experience where users guess randomly generated numbers within defined ranges. The system includes user authentication, multiple difficulty levels, scoring mechanisms, leaderboards, and an admin panel for management.

## Technology Stack

- **Framework**: Django (Python web framework)
- **Package Manager**: UV (for dependency management)
- **Database**: PostgreSQL (recommended) or SQLite for development
- **Frontend**: Django Templates, HTML5, Tailwind CSS, CSS, JavaScript (with responsive design)
- **Authentication**: Django's built-in authentication system with token-based sessions
- **Security**: Django's security features, password hashing, CSRF protection

## Core Features & Requirements

### 1. Home Page
- Engaging landing page with game information
- Visual elements including relevant images
- Clear call-to-action for registration/login
- Brief instructions on how to play
- Navigation menu with all major sections

### 2. User Registration & Authentication
- User registration form with:
  - Username (unique)
  - Email address
  - Password (with confirmation)
  - Password strength validation
- Secure login system
- Password hashing using Django's built-in PBKDF2
- Session management with token-based authentication
- Password reset functionality
- Logout functionality

### 3. Game Mechanics
- Generate random numbers within defined ranges
- Accept user input for guesses
- Provide real-time feedback:
  - "Too high" when guess exceeds target
  - "Too low" when guess is below target
  - "Correct!" when guess matches target
- Track number of attempts per game
- Maximum attempt limit: 10 attempts per game
- Display remaining attempts
- Game over notification when attempts exhausted

### 4. Difficulty Levels
Implement three difficulty levels with distinct ranges:
- **Easy**: 1-99 (2-digit range)
- **Moderate**: 1-999 (3-digit range)
- **Expert**: 1-9999 (4-digit range)

Users select difficulty level before starting each game.

### 5. Hint System
- Display current attempt number (e.g., "Attempt 3 of 10")
- Show all previous guesses with feedback
- Provide contextual hints:
  - Distance indicators (optional enhancement)
  - Range narrowing based on guesses

### 6. Scoring & Leaderboard
- Scoring algorithm based on:
  - Number of attempts used (fewer = higher score)
  - Difficulty level (harder = bonus multiplier)
  - Time taken (optional)
- Calculate and store scores in database
- Global leaderboard displaying:
  - Top 10 or 20 players
  - Username, score, difficulty level, date
  - Filterable by difficulty level
- Personal best tracking

### 7. User Profile
User profile page displaying:
- Username and email
- Total games played
- Total wins
- Best score (overall and per difficulty)
- Win rate percentage
- Recent game history
- Average attempts per win
- Profile edit functionality

### 8. Admin Panel
Django admin interface customized for:
- User management:
  - View all users
  - Activate/deactivate accounts
  - Reset passwords
  - View user statistics
- Game data management:
  - View all game records
  - Delete inappropriate content
  - Monitor for suspicious activity
- Content management:
  - Update home page content
  - Manage difficulty settings
  - Configure game parameters
- Statistics dashboard:
  - Total users
  - Total games played
  - Most active users
  - Popular difficulty levels

### 9. Contact Us Page
Display organizational information:
- Email address
- Physical address
- Contact phone number
- Contact form for direct inquiries
- Social media links (if applicable)

### 10. Feedback System
Feedback submission form with:
- Name (auto-filled for logged-in users)
- Email (auto-filled for logged-in users)
- Subject
- Message/feedback text area
- Rating system (1-5 stars)
- Store feedback in database
- Email notification to admin on new feedback

## Database Models

### AppUser Model
Extend Django's AbstractUser or use default User model with profile extension:
- username
- email
- password (hashed)
- date_joined
- is_active

### UserProfile Model
- user (OneToOne with User)
- total_games_played
- total_wins
- best_score
- best_score_easy
- best_score_moderate
- best_score_expert
- created_at
- updated_at

### Game Model
- user (ForeignKey to User)
- difficulty_level (CharField with choices)
- target_number (IntegerField)
- attempts_made (IntegerField)
- max_attempts (IntegerField, default=10)
- score (IntegerField, nullable)
- is_won (BooleanField)
- started_at (DateTimeField)
- completed_at (DateTimeField, nullable)

### Guess Model
- game (ForeignKey to Game)
- guess_number (IntegerField)
- attempt_number (IntegerField)
- feedback (CharField: "too_high", "too_low", "correct")
- created_at (DateTimeField)

### Feedback Model
- user (ForeignKey to User, nullable for anonymous)
- name (CharField)
- email (EmailField)
- subject (CharField)
- message (TextField)
- rating (IntegerField, 1-5)
- created_at (DateTimeField)
- is_reviewed (BooleanField)

## URL Structure

```
/                           - Home page
/register/                  - User registration
/login/                     - User login
/logout/                    - User logout
/profile/                   - User profile
/profile/edit/              - Edit profile
/game/new/                  - Start new game (select difficulty)
/game/<id>/play/            - Play game
/game/<id>/result/          - Game result page
/leaderboard/               - Global leaderboard
/leaderboard/<difficulty>/  - Filtered leaderboard
/contact/                   - Contact us page
/feedback/                  - Submit feedback
/admin/                     - Admin panel
```

## Views Required

- HomeView (TemplateView)
- RegisterView (CreateView)
- LoginView (Django's LoginView)
- LogoutView (Django's LogoutView)
- ProfileView (DetailView)
- ProfileEditView (UpdateView)
- GameCreateView (CreateView)
- GamePlayView (DetailView + Form handling)
- GameResultView (DetailView)
- LeaderboardView (ListView)
- ContactView (TemplateView)
- FeedbackView (CreateView)

## Forms

- UserRegistrationForm
- UserLoginForm
- ProfileEditForm
- GameDifficultyForm
- GuessForm
- ContactForm
- FeedbackForm

## Non-Functional Requirements

### User Interface
- Clean, modern, and intuitive design
- Responsive layout (mobile, tablet, desktop)
- Consistent navigation across all pages
- Accessible color schemes
- Clear typography and hierarchy
- Loading indicators for async operations
- Toast notifications for user actions

### Performance
- Page load time < 5 seconds
- Optimized database queries (use select_related, prefetch_related)
- Efficient pagination for leaderboards
- Caching for static content and leaderboard data
- Minimized JavaScript and CSS files
- Lazy loading for images

### Security
- CSRF protection on all forms
- SQL injection prevention (Django ORM)
- XSS protection with template escaping
- Secure password storage (PBKDF2/Argon2)
- HTTPS enforcement in production
- Rate limiting on login and registration
- Input validation and sanitization
- Session security (secure cookies, timeout)

### Validation
- Client-side validation for immediate feedback
- Server-side validation for data integrity
- Proper error messages for invalid inputs
- Prevent duplicate submissions
- Range validation for guess inputs based on difficulty

### Scalability
- Support for multiple concurrent users
- Efficient database indexing
- Stateless design for horizontal scaling
- Background task processing (only if needed)

## Development Guidelines & Best Practices

### Project Structure
- Use Django's standard project structure
- Organize apps logically (users, games, feedback, etc.)
- Separate settings for development/production
- Keep templates organized by app
- Use static files properly

### Code Quality
- Follow PEP 8 style guide
- Write descriptive docstrings
- Always Use type hints
- Keep views thin, logic in models/services
- DRY principle - avoid code duplication
- Meaningful variable and function names

### UV Package Manager
- Initialize/run project with UV consistently
- Install dependencies/packages with UV appropriately
- Lock dependencies for reproducibility
- Keep dependencies updated but stable

### Version Control
- Use Git with meaningful yet concise commit messages

### Database
- Use migrations for all schema changes
- Index foreign keys and frequently queried fields
- Use database constraints where appropriate
- Write efficient queries (avoid N+1 problems)

### Templates
- Use Django template inheritance (base.html)
- Keep templates DRY with includes and blocks
- Use template tags for complex logic
- Implement CSRF tokens on all forms

### Static Files
- Organize CSS, JS, images properly
- Use Django's static file system
- Minify CSS/JS for production

### Error Handling
- Implement custom 404 and 500 error pages
- Log errors appropriately
- Provide user-friendly error messages
- Handle database exceptions gracefully

### Documentation
- Include README with setup instructions
- Document complex functions and classes
- Include deployment guide

### Deployment Considerations
- Use environment variables for sensitive data
- Configure allowed hosts properly
- Set DEBUG=False in production
- Use production-ready database (PostgreSQL)
- Configure static file serving
- Set up logging properly
- Use WSGI server (Gunicorn)

## Professional Standards

1. **Mobile First**: Design for mobile devices first
2. **SEO**: Implement basic SEO best practices

## Success Criteria

- All functional requirements implemented and working
- Secure authentication and authorization
- Responsive design across devices
- No critical security vulnerabilities
- Clean, maintainable codebase
- Understandable documentation
- Positive user experience with intuitive interface
- Efficient performance under load
- Admin panel functional for management tasks