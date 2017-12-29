from viewflow import flow, lock
from viewflow.base import this, Flow
from viewflow.flow.views import CreateProcessView

from django.contrib.auth.models import User

from .models import DailyTimesheetApproval, VacationApproval

from .views import (
    FillDailyTimesheetView,
    ApproveDailyTimesheetView,
    RenewPassportView,
    FillVacationView,
    UpdateVacationView,
    ApproveVacationView,
)

from .tasks import calculate_sheet_payroll
from flowutils import activities


class DailyTimesheetApprovalFlow(Flow):
    process_class = DailyTimesheetApproval
    lock_impl = lock.no_lock

    process_description = 'Daily Timesheet Approval'

    label = 'daily'
    flow_label = 'daily'

    start = (
        flow.Start(
            CreateProcessView,
            task_title='Create a new daily timesheet')
        .Permission('auth.no_permission')
        .Next(this.fill)
    )

    fill = (
        flow.View(
            FillDailyTimesheetView,
            task_title='Fill your daily timesheet')
        .Permission('auth.no_permission')
        .Assign(lambda a: a.process.created_by)
        .Next(this.calculate_payroll)
    )

    calculate_payroll = (
        activities.Job(calculate_sheet_payroll)
        .Next(this.approve)
    )

    approve = (
        flow.View(
            ApproveDailyTimesheetView,
            task_title='Approve this daily timesheet',
        )
        .Permission('auth.can_approve')
        .Next(this.check_approval)
    )

    check_approval = (
        flow.If(lambda a: a.task.process.sheet.is_approved())
        .Then(this.end)
        .Else(this.fill)
    )

    end = flow.End()


class VacationApprovalFlow(Flow):
    process_class = VacationApproval
    lock_impl = lock.no_lock

    process_description = 'Vacation Approval Request'

    label = 'vacation'
    flow_label = 'vacation'

    start = (
        flow.Start(
            CreateProcessView,
            task_title='Request a vacation')
        .Permission('auth.no_permission')
        .Next(this.fill)
    )

    fill = (
        flow.View(
            FillVacationView,
            task_title='Fill your vacation details')
        .Permission('auth.no_permission')
        .Assign(lambda a: a.process.created_by)
        .Next(this.split)
    )

    split = (
        flow.Split()
        .Next(
            this.renew,
            cond=lambda act: act.process.vacation.requires_renewal())
        .Always(this.approve)
    )

    renew = (
        flow.View(
            RenewPassportView,
            task_title='Renew this passport expiry date',
        )
        .Permission('auth.can_renew_passport')
        .Assign(lambda a: User.objects.get(username='operator'))
        .Next(this.join_)
    )

    update = (
        flow.View(
            UpdateVacationView,
            task_title='Update your vacation details')
        .Permission('auth.no_permission')
        .Assign(lambda a: a.process.created_by)
        .Next(this.approve)
    )

    approve = (
        flow.View(
            ApproveVacationView,
            task_title='Approve this vacation request',
        )
        .Permission('auth.can_approve')
        .Next(this.check_approval)
    )
    check_approval = (
        flow.If(lambda a: a.task.process.vacation.is_approved())
        .Then(this.join_)
        .Else(this.update)
    )

    join_ = (
        flow.Join()
        .Next(this.end)
    )
    end = flow.End()
