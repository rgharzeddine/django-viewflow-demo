from viewflow import flow, lock
from viewflow.base import this, Flow
# from viewflow.flow.views import UpdateProcessView, CreateProcessView

from django.contrib.auth.models import User
# from viewflow.decorators import flow_start_func

# from .models import DailyTimesheet
from .models import DailyTimesheetApproval, VacationApproval
from .views import (
    StartDailyTimesheetProcessView,
    FillDailyTimesheetView,
    ApproveDailyTimesheetView,

    StartVacationProcessView,
    FillVacationView,
    ApproveVacationView,

)

# @flow_start_func
# def create_flow(activation, **kwargs):
#     activation.prepare()
#     activation.done()
#     return activation


def approve_assign(activation):
    # return user by permissions
    return User.objects.get(username='omar')


def assign_daily_timesheet_fill(activation):
    # assign same user
    return activation.process.sheet.for_user


def assign_vacation_fill(activation):
    # assign same user
    return activation.process.vacation.for_user


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
            StartDailyTimesheetProcessView,
            task_title="Timesheet submittal")
        .Permission('auth.no_permission')
        .Next(this.approve)
    )
    start.comments = 'start a daily timesheet fill process'

    fill = (
        flow.View(
            FillDailyTimesheetView,
            task_title='Update Timesheet')
        .Permission('auth.no_permission')
        .Assign(assign_daily_timesheet_fill)
        .Next(this.approve)
    )

    approve = (
        flow.View(
            ApproveDailyTimesheetView,
            task_title='daily timesheet approval',
        )
        .Permission('auth.can_approve')
        .Assign(approve_assign)
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
            StartVacationProcessView,
            task_title="Request for vacation")
        .Permission('auth.no_permission')
        .Next(this.approve)
    )
    start.comments = 'start vacation request process'

    fill = (
        flow.View(
            FillVacationView,
            task_title='Update Vacation Details')
        .Permission('auth.no_permission')
        .Assign(assign_vacation_fill)
        .Next(this.approve)
    )

    approve = (
        flow.View(
            ApproveVacationView,
            task_title='vacation approval',
        )
        .Permission('auth.can_approve')
        .Assign(approve_assign)
        .Next(this.check_approval)
    )

    check_approval = (
        flow.If(check_vacation_approved)
        .Then(this.end)
        .Else(this.fill)
    )
    end = flow.End()
