from viewflow import flow, lock
from viewflow.base import this, Flow
# from viewflow.flow.views import UpdateProcessView

from django.contrib.auth.models import User
# from viewflow.decorators import flow_start_func

# from .models import DailyTimesheet
from .models import DailyTimesheetApproval
from .views import FillProcessView, ApproveDailyTimesheetView

# @flow_start_func
# def create_flow(activation, **kwargs):
#     activation.prepare()
#     activation.done()
#     return activation


def approve_assign(activation):
    # return user by permissions
    return User.objects.get(username='omar')


def fill_assign(activation):
    # assign same user
    return User.objects.get(username='rawad')


def check_approved(this_flow):
    return this_flow.task.process.sheet.is_approved()


class DailyTimesheetApprovalFlow(Flow):
    process_class = DailyTimesheetApproval
    # lock_impl = lock.select_for_update_lock
    lock_impl = lock.no_lock

    label = 'daily'
    flow_label = 'daily'

    start = flow.Start(
        fields=['name'],
    ).Next(this.fill).Permission('auth.no_permission')

    fill = (
        flow.View(
            FillProcessView,
            # fields=['date', 'code'],
            task_title='Fill Daily Timesheet')
        .Permission('auth.no_permission')
        .Assign(fill_assign)
        .Next(this.approve)
    )

    approve = (
        flow.View(
            ApproveDailyTimesheetView,
            # UpdateProcessView,
            # fields=['sheet.approval_status']
        )
        .Permission('auth.can_approve')
        .Assign(approve_assign)
        .Next(this.check_approval)
    )

    check_approval = (
        flow.If(check_approved)
        .Then(this.end)
        .Else(this.fill)
    )
    end = flow.End()
