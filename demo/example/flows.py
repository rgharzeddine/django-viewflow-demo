from viewflow import flow, lock
from viewflow.base import this, Flow
from viewflow.flow.views import CreateProcessView, UpdateProcessView

from django.contrib.auth.models import User
# from viewflow.decorators import flow_start_func

# from .models import DailyTimesheet
from .models import DailyTimesheetApproval
from .views import FillProcessView

# @flow_start_func
# def create_flow(activation, **kwargs):
#     activation.prepare()
#     activation.done()
#     return activation


def approval_assign(activation):
    #
    return User.objects.get(username='omar')


class DailyTimesheetApprovalFlow(Flow):
    process_class = DailyTimesheetApproval
    # lock_impl = lock.select_for_update_lock
    lock_impl = lock.no_lock

    label = 'daily'
    flow_label = 'daily'

    start = flow.Start(
        fields=['name'],
    ).Next(this.fill)

    fill = (
        flow.View(
            # CreateDailyTimesheetView,
            FillProcessView,
            # fields=['date', 'code'],
            task_title='Fill Daily Timesheet')
        .Next(this.approve)
    )

    approve = (
        flow.View(
            # ApproveDailyTimesheetView,
            UpdateProcessView,
            fields=['approval_status'])
        .Permission('auth.can_approve')
        .Assign(approval_assign)
        .Next(this.check_approval)
    )

    check_approval = (
        flow.If(
            lambda approval: approval.approval_status == 'approved')
        .Then(this.end)
        .Else(this.fill)
    )
    end = flow.End()
