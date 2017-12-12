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
# from django.views.generic.edit import FormView
from django.views.generic import ListView, UpdateView

# from django.views.generic import ListView, CreateView, UpdateView
from django_tables2 import SingleTableMixin

from viewflow.flow.views import UpdateProcessView

from .models import DailyTimesheet

from . import tables
from . import forms

from viewflow.models import Process, Task


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


class FillProcessView(UpdateProcessView):
    form_class = forms.FillDailyTimesheetForm
    model = DailyTimesheet

    def get_success_url(self):
        return reverse_lazy('index')

    def get_object(self, queryset=None):
        """Return the process for the task activation."""
        return self.activation.process.sheet

    def form_valid(self, form):
        sheet = form.save(commit=False)
        sheet.for_user = self.request.user
        sheet.save()

        approval = self.activation.process
        approval.sheet = sheet
        approval.save()

        if '_continue' in form.data.keys():
            return super(FillProcessView, self).form_valid(form)
        return super(UpdateView, self).form_valid(form)


class ApproveDailyTimesheetView(UpdateProcessView):
    form_class = forms.ApproveDailyTimesheetForm
    model = DailyTimesheet

    def get_success_url(self):
        return reverse_lazy('index')

    def get_object(self):
        return self.activation.process.sheet

    def form_valid(self, form):
        sheet = form.save(commit=False)
        sheet.approved_by = self.request.user
        sheet.approved_at = datetime.now()
        sheet.save()

        if '_continue' in form.data.keys():
            return super(ApproveDailyTimesheetView, self).form_valid(form)
        return super(UpdateView, self).form_valid(form)


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
        # filters NEW, DONE
        filter_by = self.request.GET.get('filter', '').upper()

        # if user.has_perm('auth.can_approve'):
        #     if filter_by:
        #         return Task.objects.filter(status=filter_by)
        #     return Task.objects.all()
        if filter_by:
            return Task.objects.filter(owner=user, status=filter_by)
        return Task.objects.filter(owner=user)


class ProcessListView(SingleTableMixin, ListView):
    template_name = 'example/process_list.html'
    model = Process
    table_class = tables.ProcessTable
    context_object_name = 'processes'
    context_table_name = 'processes_table'

    def get_queryset(self):
        # filters NEW, DONE
        filter_by = self.request.GET.get('filter', '').upper()

        if filter_by:
            return Process.objects.filter(status=filter_by)
        return Process.objects.all()
