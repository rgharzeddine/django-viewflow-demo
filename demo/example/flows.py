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

def assign_operator(activation):
    # assign same user
    return User.objects.get(username='operator')


def assign_user(activation):
    # assign same user
    return activation.process.created_by


def check_daily_timesheet_approved(this_flow):
    return this_flow.task.process.sheet.is_approved()


def check_vacation_approved(this_flow):
    return this_flow.task.process.vacation.is_approved()


# daily timesheet approval flow
class DailyTimesheetApprovalFlow(Flow):
    process_class = DailyTimesheetApproval
    # lock_impl = lock.select_for_update_lock
    lock_impl = lock.no_lock

    label = 'daily'
    flow_label = 'daily'

    start = (
        flow.Start(
            CreateProcessView,
            task_title='Fill a timesheet')
        .Permission('auth.no_permission')

        .Next(this.fill)
    )
    fill = (
        flow.View(
            FillDailyTimesheetView,
            task_title='Update your timesheet')
        .Permission('auth.no_permission')
        .Assign(assign_user)
        .Next(this.approve)
    )

    approve = (
        flow.View(
            ApproveDailyTimesheetView,
            task_title='Approve this timesheet',
        )
        .Permission('auth.can_approve')
        # .Assign(approve_assign)
        .Next(this.check_approval)
    )

    check_approval = (
        flow.If(check_daily_timesheet_approved)
        .Then(this.end)
        .Else(this.fill)
    )
    end = flow.End()


# vacation approval flow
class VacationApprovalFlow(Flow):
    process_class = VacationApproval
    # lock_impl = lock.select_for_update_lock
    lock_impl = lock.no_lock

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
        .Assign(assign_user)
        .Next(this.split_on_renew)
    )

    split_on_renew = (
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
        .Assign(assign_operator)
        .Next(this.join_on_check_approval)
    )

    update = (
        flow.View(
            UpdateVacationView,
            task_title='Update your vacation details')
        .Permission('auth.no_permission')
        .Assign(assign_user)
        .Next(this.approve)
    )

    approve = (
        flow.View(
            ApproveVacationView,
            task_title='Approve this vacation request',
        )
        .Permission('auth.can_approve')
        # .Assign(approve_assign)
        .Next(this.check_approval)
    )
    check_approval = (
        flow.If(check_vacation_approved)
        .Then(this.join_on_check_approval)
        .Else(this.update)
    )

    join_on_check_approval = (
        flow.Join()
        .Next(this.end)
    )
    end = flow.End()
