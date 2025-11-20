"""Views for feedback app."""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import CreateView
from .models import Feedback
from .forms import FeedbackForm, ContactForm


class FeedbackCreateView(CreateView):
    """View for creating feedback."""
    model = Feedback
    form_class = FeedbackForm
    template_name = 'feedback/feedback.html'
    success_url = '/feedback/'

    def get_form_kwargs(self):
        """Pass user to form."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Handle valid form submission."""
        feedback = form.save(commit=False)
        if self.request.user.is_authenticated:
            feedback.user = self.request.user
        feedback.save()
        
        # Send email notification to admin
        try:
            send_mail(
                subject=f'New Feedback: {feedback.subject}',
                message=f'''
New feedback received:

From: {feedback.name} ({feedback.email})
Rating: {feedback.rating} stars
Subject: {feedback.subject}

Message:
{feedback.message}

---
This is an automated message from the Number Guessing Game.
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@example.com',
                recipient_list=[settings.ADMINS[0][1]] if hasattr(settings, 'ADMINS') and settings.ADMINS else ['admin@example.com'],
                fail_silently=True,
            )
        except Exception:
            pass  # Fail silently if email can't be sent
        
        messages.success(self.request, 'Thank you for your feedback!')
        return redirect(self.success_url)
