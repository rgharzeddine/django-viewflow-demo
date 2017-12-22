from viewflow import flow, lock
from viewflow.base import this, Flow
from viewflow.flow.views import CreateProcessView
from viewflow.activation import AbstractJobActivation, STATUS

from django.contrib.auth.models import User
from django.utils.timezone import now

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


def dummy(*args):
    print('SUCCESS: dummy called')


class CeleryJobActivation(AbstractJobActivation):

    def run_async(self, *args, **kwargs):
        dummy()

        # IMPORTANT
        # using id(self) as a fast solution instead of
        # pickling for serialization

        # FAILS TO WORK
        calculate_sheet_payroll.delay(id(self))

        # WORKS
        # calculate_sheet_payroll(id(self))

        self.done()

    status = AbstractJobActivation.status

    # @status.transition(source=STATUS.ASSIGNED)
    # def schedule(self):
    #     print('scheduled !!')

    #     # self.flow_task.job(id(self))
    #     # self.flow_task.job.delay(id(self))
    #     # calculate_sheet_payroll.delay(id(self))
    #     print('schedule finished !!')
    #     self.done()

    @status.transition(
        source=[STATUS.STARTED, STATUS.ASSIGNED], target=STATUS.DONE)
    def done(self):
        """Cancel existing task."""
        self.task.finished = now()
        self.task.status = STATUS.DONE
        self.task.save()
        self.activate_next()


class FlowJob(flow.AbstractJob):
    activation_class = CeleryJobActivation


def assign_user(activation):
    return activation.process.created_by


def check_vacation_approved(this_flow):
    return this_flow.task.process.vacation.is_approved()


class DailyTimesheetApprovalFlow(Flow):
    process_class = DailyTimesheetApproval
    lock_impl = lock.no_lock

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
        .Assign(assign_user)
        .Next(this.calculate_payroll)
    )

    calculate_payroll = (
        # flow.Function(
        FlowJob(
            # calculate_sheet_payroll
            # test_celery
            calculate_sheet_payroll
        )
        .Next(this.approve)
    )

    approve = (
        flow.View(
            ApproveDailyTimesheetView,
            task_title='Approve this timesheet',
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

    # @method_decorator(flow.flow_func)
    # def on_calculate_payroll(self, activation, sheet):
    #     activation.prepare()
    #     calculate_payroll.delay(activation)
    #     activation.done()

    # def get_sheet_handler_task(self, flow_task, sheet):
    #     return Task.objects.get(process=sheet.process)


class VacationApprovalFlow(Flow):
    process_class = VacationApproval
    # lock_impl = lock.select_for_update_lock
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
        .Assign(assign_user)
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
        .Assign(assign_user)
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
        flow.If(check_vacation_approved)
        .Then(this.join_)
        .Else(this.update)
    )

    join_ = (
        flow.Join()
        .Next(this.end)
    )
    end = flow.End()
