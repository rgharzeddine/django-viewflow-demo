# from django.shortcuts import render
from datetime import date, datetime

from django.conf import settings
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required

# from django.contrib.auth.mixins import (
#     # PermissionRequiredMixin,
#     LoginRequiredMixin,
# )
from django.views.generic.edit import FormView
from django.views.generic import ListView

# from django.views.generic import ListView, CreateView, UpdateView
from django_tables2 import SingleTableMixin

from viewflow.flow.views import UpdateProcessView, CreateProcessView

from .models import DailyTimesheet, DailyTimesheetApproval

from . import tables
from . import forms

from viewflow.models import Process, Task
#  coerce_to_related_instance

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


class FillProcessView(CreateProcessView):
    form_class = forms.FillDailyTimesheetForm
    model = DailyTimesheet

    def get_success_url(self):
        return reverse_lazy('index')

    def get_object(self):
        """Return the process for the task activation."""
        return self.activation.process

    def form_valid(self, form):
        approval = form.save(commit=False)
        timesheetform = forms.FillDailyTimesheetForm(
            form.data,
        )
        sheet = timesheetform.save(commit=False)
        sheet.for_user = self.request.user
        sheet.save()

        approval.sheet = sheet
        approval.save()

        return super(FillProcessView, self).form_valid(form)

        # return redirect(self.get_success_url())


class DailyTimesheetListView(SingleTableMixin, ListView):
    template_name = 'example/dailytimesheet_list.html'
    model = DailyTimesheet
    table_class = tables.DailyTimesheetTable
    context_object_name = 'sheets'
    context_table_name = 'sheets_table'

    def get_queryset(self):
        user = self.request.user
        return DailyTimesheet.objects.filter(for_user=user)


class TaskListView(SingleTableMixin, ListView):
    template_name = 'example/task_list.html'
    model = Task
    table_class = tables.TaskTable
    context_object_name = 'tasks'
    context_table_name = 'tasks_table'

    def get_queryset(self):
        user = self.request.user
        if user.has_perm('auth.can_approve'):
            return Task.objects.all()
        return Task.objects.filter(owner=user)

    # implement filter by started ,completed
