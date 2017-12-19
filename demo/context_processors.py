"""context processor for timesheet project"""

from datetime import date

from django.conf import settings

from django.contrib.auth.models import User


def app_related_context(request):
    """Returns app related context variables"""
    context = {}
    context['users'] = User.objects.all()
    return context
