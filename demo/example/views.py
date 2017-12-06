# from django.shortcuts import render
from datetime import date, datetime

from django.conf import settings
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import (
    # PermissionRequiredMixin,
    LoginRequiredMixin,
)

from django.views.generic import ListView, CreateView
from django_tables2 import SingleTableMixin

from viewflow.flow.views import UpdateProcessView, CreateProcessView

from .models import DailyTimesheet
from .tables import DailyTimesheetTable


def fast_login(request):
    """Provides the ability to quickly switch between test users"""
    if request.method == 'POST':
        if request.user:
            logout(request)
        username = request.POST.get('username')
        user = authenticate(
            username=username,
            password=settings.USER_PASSWORD,
            backend='django.contrib.auth.backends.ModelBackend',
        )
        if user:
            login(request, user)
    return redirect(reverse_lazy('index'))


def fast_logout(request):
    """Provides the ability to quickly switch between test users"""
    if request.user:
        logout(request)
    return redirect(reverse_lazy('index'))


def home(request):
    """Home view with dashboard actions"""

    context = dict(
        users=User.objects.all(),
        today=date.today(),
        # tasks=DailyTimesheet.objects.filter(
        #     user=request.user
        # )
    )

    return render(request, 'index.html', context)


class ApproveDailyTimesheetView(UpdateProcessView):
    form_class = DailyTimesheet

    def __init__(self, *args, **kwargs):
        super(ApproveDailyTimesheetView, self).__init__(*args, **kwargs)
        if self.form_class is None and self.fields is None:
            self.fields = []

    @property
    def model(self):
        """Process class."""
        return DailyTimesheet
        # return self.activation.flow_class.process_class

    def get_object(self, queryset=None):
        """Return the process for the task activation."""
        return self.activation.process.sheet


class CreateDailyTimesheetView(CreateProcessView):
    form_class = DailyTimesheet

    def __init__(self, *args, **kwargs):
        super(CreateDailyTimesheetView, self).__init__(*args, **kwargs)
        if self.form_class is None and self.fields is None:
            self.fields = []

    @property
    def model(self):
        """Process class."""
        return DailyTimesheet
        # return self.activation.flow_class.process_class

    def get_object(self, queryset=None):
        """Return the process for the task activation."""
        return self.activation.process.sheet


class DailyTimesheetListView(SingleTableMixin, LoginRequiredMixin, ListView):
    model = DailyTimesheet
    table_class = DailyTimesheetTable
    context_table_name = 'sheets_table'
    context_object_name = 'sheets'

    def get_queryset(self):
        return DailyTimesheet.objects.filter(
            for_user__username=self.request.user.username)

    def get_context_data(self, **kwargs):
        context = super(
            DailyTimesheetListView, self).get_context_data(**kwargs)

        context['users'] = User.objects.all()
        return context


class DailyTimesheetCreateView(LoginRequiredMixin, CreateView):
    model = DailyTimesheet
    fields = ['date', 'code']
    success_url = reverse_lazy('timesheets')

    def form_valid(self, form):
        sheet = form.save(commit=False)
        sheet.for_user = self.request.user
        sheet.save()
        return redirect(self.success_url)
