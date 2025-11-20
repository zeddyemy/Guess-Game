"""Views for core app."""
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Home page view."""
    template_name = 'core/home.html'


class ContactView(TemplateView):
    """Contact page view."""
    template_name = 'core/contact.html'
