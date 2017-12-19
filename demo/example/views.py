# from django.shortcuts import render
from datetime import date, datetime

from django.conf import settings
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# from django.contrib.auth.mixins import (
#     # PermissionRequiredMixin,
#     LoginRequiredMixin,
# )

from django.views.generic import ListView, UpdateView, TemplateView

from viewflow.flow.views import UpdateProcessView, CreateProcessView
from viewflow.models import Process, Task

from .models import DailyTimesheet, Vacation
from . import forms


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
    return redirect(reverse_lazy('example:index'))


def fast_logout(request):
    """Provides the ability to quickly switch between test users"""
    if request.user:
        logout(request)
    return redirect(reverse_lazy('example:index'))


def home(request):
    """Home view with dashboard actions"""

    context = dict(
        users=User.objects.all(),
        today=date.today(),
    )

    return render(request, 'index.html', context)


# daily timesheet flow views
class StartDailyTimesheetProcessView(CreateProcessView):
    form_class = forms.FillDailyTimesheetForm
    model = DailyTimesheet

    def get_success_url(self):
        return reverse_lazy('example:tasks_in_progress')

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

        if '_continue' in form.data:
            return super(StartDailyTimesheetProcessView, self).form_valid(form)
        return super(UpdateView, self).form_valid(form)


class FillDailyTimesheetView(UpdateProcessView):
    form_class = forms.FillDailyTimesheetForm
    model = DailyTimesheet

    def get_success_url(self):
        return reverse_lazy('example:tasks_in_progress')

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

        if '_continue' in form.data:
            return super(FillDailyTimesheetView, self).form_valid(form)
        return super(UpdateView, self).form_valid(form)


class ApproveDailyTimesheetView(UpdateProcessView):
    form_class = forms.ApproveDailyTimesheetForm
    model = DailyTimesheet

    def get_success_url(self):
        return reverse_lazy('example:tasks_in_progress')

    def get_object(self):
        return self.activation.process.sheet

    def form_valid(self, form):
        sheet = form.save(commit=False)
        sheet.approved_by = self.request.user
        sheet.approved_at = datetime.now()
        sheet.save()

        if '_continue' in form.data:
            return super(ApproveDailyTimesheetView, self).form_valid(form)
        return super(UpdateView, self).form_valid(form)


class DailyTimesheetListView(ListView):
    template_name = 'example/dailytimesheet_list.html'
    model = DailyTimesheet
    context_object_name = 'sheets'

    def get_queryset(self):
        user = self.request.user
        if user.has_perm('auth.can_approve'):
            return DailyTimesheet.objects.all()
        return DailyTimesheet.objects.filter(for_user=user)


class VacationListView(ListView):
    template_name = 'example/vacation_list.html'
    model = Vacation
    context_object_name = 'vacations'

    def get_queryset(self):
        user = self.request.user
        if user.has_perm('auth.can_approve'):
            return Vacation.objects.all().order_by('-start_date')
        return Vacation.objects.filter(for_user=user).order_by('-start_date')


# vacation flow views
class StartVacationProcessView(CreateProcessView):
    form_class = forms.FillVacationForm
    model = Vacation

    def get_success_url(self):
        return reverse_lazy('example:tasks_in_progress')

    def get_object(self, queryset=None):
        """Return the process for the task activation."""
        return self.activation.process.vacation

    def form_valid(self, form):
        vacation = form.save(commit=False)
        vacation.for_user = self.request.user
        vacation.save()

        approval = self.activation.process
        approval.vacation = vacation
        approval.save()

        if '_continue' in form.data:
            return super(StartVacationProcessView, self).form_valid(form)
        return super(UpdateView, self).form_valid(form)


class FillVacationView(UpdateProcessView):
    form_class = forms.FillVacationForm
    model = Vacation

    def get_success_url(self):
        return reverse_lazy('example:tasks_in_progress')

    def get_object(self, queryset=None):
        """Return the process for the task activation."""
        return self.activation.process.vacation

    def form_valid(self, form):
        vacation = form.save(commit=False)
        vacation.for_user = self.request.user
        vacation.save()

        approval = self.activation.process
        approval.vacation = vacation
        approval.save()

        if '_continue' in form.data:
            return super(FillVacationView, self).form_valid(form)
        return super(UpdateView, self).form_valid(form)


class ApproveVacationView(UpdateProcessView):
    form_class = forms.ApproveVacationForm
    model = Vacation

    def get_success_url(self):
        return reverse_lazy('example:tasks_in_progress')

    def get_object(self):
        return self.activation.process.vacation

    def form_valid(self, form):
        vacation = form.save(commit=False)
        vacation.approved_by = self.request.user
        vacation.approved_at = datetime.now()
        vacation.save()

        if '_continue' in form.data:
            return super(ApproveVacationView, self).form_valid(form)
        return super(UpdateView, self).form_valid(form)


# Flow tasks and processes
class BaseTaskListView(ListView):
    template_name = 'example/task_list.html'
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['header'] = self.header
        return context


class UnassignedTaskListView(BaseTaskListView):
    header = 'Unassigned Tasks'

    def get_queryset(self):
        return Task.objects.filter(status='NEW', owner=None)


class CompletedTaskListView(BaseTaskListView):
    header = 'Completed Tasks'

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(status='DONE', owner=user)


class InProgressTaskListView(BaseTaskListView):
    header = 'Tasks In Progress'

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(owner=user).exclude(status='DONE')


class ProcessListView(ListView):
    template_name = 'example/process_list.html'
    model = Process
    context_object_name = 'processes'

    def get_queryset(self):
        filter_by = self.request.GET.get('filter', '').upper()

        if filter_by.startswith('-'):
            exclude = True
            filter_by = filter_by[1:]
        else:
            exclude = False

        if filter_by:
            if exclude:
                return Process.objects.exclude(
                    status=filter_by)
            return Process.objects.filter(status=filter_by)
        return Process.objects.all()


class ProcessClassesListView(TemplateView):
    template_name = 'example/process_class_list.html'


class AssignTaskView(UpdateProcessView):
    model = Task

    def form_valid(self, form):
        task = form.save(commit=False)
        task.owner = self.request.user
        task.save()

        if '_continue' in form.data:
            return super(AssignTaskView, self).form_valid(form)
        return super(UpdateView, self).form_valid(form)


# class UnassignTaskView(UpdateProcessView):
#     model = Task

#     def form_valid(self, form):
#         task = form.save(commit=False)
#         task.owner = None
#         task.save()

#         if '_continue' in form.data:
#             return super(UnassignTaskView, self).form_valid(form)
#         return super(UpdateView, self).form_valid(form)
