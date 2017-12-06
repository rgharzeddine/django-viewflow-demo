from viewflow import flow
from viewflow.base import this, Flow
# from viewflow.flow.views import CreateProcessView, UpdateProcessView
from .views import ApproveDailyTimesheetView, CreateDailyTimesheetView

from .models import DailyTimesheet


class DailyTimesheetApprovalFlow(Flow):
    process_class = DailyTimesheet

    start = (
        flow.View(
            CreateDailyTimesheetView,
        ).Next(this.fill)
    )
    fill = (
        flow.View(
            CreateDailyTimesheetView,
            fields=['date', 'status'],
        ).Next(this.approve)
    )
    approve = (
        flow.View(
            ApproveDailyTimesheetView,
            fields=['approval_status'])
        .Permission('auth.can_approve_daily_timesheet')
        .Next(this.check_approval)
    )

    check_approval = (
        flow.If(
            lambda approval: approval.approval_status == 'approved')
        .Then(this.end)
        .Else(this.fill)
    )
    end = flow.End()
