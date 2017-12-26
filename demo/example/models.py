"""main models"""

from time import sleep
from random import uniform as randfloat

from datetime import datetime
from datetime import timedelta

from django.contrib.auth.models import User

from django.db.models import (
    CASCADE,
    CharField,
    DateField,
    BooleanField,
    DateTimeField,
    ForeignKey,
    Model,
    FloatField,
)
from viewflow.models import Process

APPROVAL_STATUS = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]


class DailyTimesheet(Model):

    CODE = [
        ('absent', 'Absent'),
        ('present', 'Present'),
        ('weekend', 'Weekend'),
        ('holiday', 'Holiday'),
        ('paid_leave', 'Paid Leave'),
        ('unpaid_leave', 'Unpaid Leave'),
        ('sick_leave', 'Sick Leave'),
        ('business_trip', 'Business Trip'),
    ]

    for_user = ForeignKey(User, on_delete=CASCADE, related_name='sheets')
    date = DateField()
    code = CharField(max_length=20, choices=CODE, default='present')
    created_at = DateTimeField(auto_now=True)
    payroll = FloatField(null=True, blank=True)

    approval_status = CharField(
        max_length=20,
        choices=APPROVAL_STATUS,
        default='pending',
    )

    approved_at = DateTimeField(blank=True, null=True)

    approved_by = ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=CASCADE,
        related_name='timesheet_approvals')

    def is_approved(self):
        return self.approval_status == 'approved'

    def calculate_payroll(self):
        print('started calculating payroll (takes some time...)')
        sleep(randfloat(10.0, 30.0))
        self.payroll = randfloat(200.0, 1000.0)
        print('finished calculating payroll')
        self.save()


class DailyTimesheetApproval(Process):

    sheet = ForeignKey(
        DailyTimesheet,
        on_delete=CASCADE,
        null=True,
        related_name='approval')

    def __str__(self):
        if self.sheet:
            return 'Daily timesheet approval for {} on date {}'.format(
                self.sheet.for_user.username,
                self.sheet.date,
            )
        return 'New timesheet approval'


class Vacation(Model):

    for_user = ForeignKey(User, on_delete=CASCADE, related_name='vacations')
    start_date = DateField()
    end_date = DateField()
    passport_expiry_date = DateField(null=True, blank=True)
    requested_on = DateField(auto_now=True)
    details = CharField(max_length=300, default='vacation')

    approval_status = CharField(
        max_length=20,
        choices=APPROVAL_STATUS,
        default='pending',
    )

    approved_at = DateTimeField(blank=True, null=True)
    approved_by = ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=CASCADE,
        related_name='vacation_approvals')
    request_details = BooleanField(default=False)

    def is_approved(self):
        return any([
            self.approval_status == 'approved',
            not self.request_details,
        ])

    def renew_passport(self):
        self.passport_expiry_date = (
            datetime.now() + timedelta(days=365)).date()

    def requires_renewal(self):
        if not self.passport_expiry_date:
            return True
        elif self.passport_expiry_date < self.end_date:
            return True
        else:
            return False


class VacationApproval(Process):

    vacation = ForeignKey(
        Vacation,
        on_delete=CASCADE,
        null=True,
        related_name='approval')

    def __str__(self):
        if self.vacation:
            return 'Vacation approval for {} starting {} and ending {}'.format(
                self.vacation.for_user.username,
                self.vacation.start_date,
                self.vacation.end_date,
            )
        return 'New vacation approval request'
