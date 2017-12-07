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

from django.views.generic import ListView, CreateView, UpdateView
from django_tables2 import SingleTableMixin

from viewflow.flow.views import UpdateProcessView, CreateProcessView

from .models import DailyTimesheet
from .tables import DailyTimesheetTable
from .forms import (
    DailyTimesheetForm, DailyTimesheetApprovalForm, DailyTimesheetUpdateForm)


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
        user = self.request.user
        if user.has_perm('auth.can_approve'):
            return DailyTimesheet.objects.all()

        return DailyTimesheet.objects.filter(
            for_user__username=self.request.user.username)

    def get_context_data(self, **kwargs):
        context = super(
            DailyTimesheetListView, self).get_context_data(**kwargs)

        context['users'] = User.objects.all()
        context['approving'] = self.request.user.has_perm('auth.can_approve')
        return context


class DailyTimesheetCreateView(LoginRequiredMixin, CreateView):
    model = DailyTimesheet
    success_url = reverse_lazy('timesheets')
    form_class = DailyTimesheetForm

    def form_valid(self, form):
        sheet = form.save(commit=False)
        sheet.for_user = self.request.user
        sheet.save()
        return redirect(self.success_url)


class DailyTimesheetUpdateView(LoginRequiredMixin, UpdateView):
    model = DailyTimesheet
    template_name = 'example/dailytimesheetapproval_form.html'
    success_url = reverse_lazy('timesheets')

    def get_form_class(self):
        if self.request.user.has_perm('auth.can_approve'):
            return DailyTimesheetApprovalForm
        return DailyTimesheetUpdateForm

    def form_valid(self, form):
        sheet = form.save(commit=False)
        if self.request.user.has_perm('auth.can_approve'):
            sheet.approved_by = self.request.user
            sheet.approved_at = datetime.now()
        else:
            sheet.approved_by = None
            sheet.approved_at = None
            sheet.approval_status = 'pending'

        sheet.save()
        return redirect(self.success_url)
