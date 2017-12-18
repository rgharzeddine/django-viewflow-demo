"""main models"""

from django.contrib.auth.models import User

from django.db.models import (
    CASCADE,
    CharField,
    DateField,
    BooleanField,
    OneToOneField,
    DateTimeField,
    ForeignKey,
    Model,
)
from viewflow.models import Process


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
    code = CharField(
        max_length=20,
        choices=CODE,
        default='present',
    )
    created_at = DateTimeField(auto_now=True)

    APPROVAL_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

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
        return 'New Daily timesheet'


class Vacation(Model):

    for_user = ForeignKey(User, on_delete=CASCADE, related_name='vacations')
    start_date = DateField()
    end_date = DateField()
    requested_on = DateField(auto_now=True)
    details = CharField(max_length=300, default='vacation')

    APPROVAL_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

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
    final = BooleanField(default=False)

    def is_approved(self):
        return self.approval_status == 'approved'


class VacationApproval(Process):

    vacation = OneToOneField(
        Vacation,
        on_delete=CASCADE,
        null=True,
        related_name='approval')

    def __str__(self):
        return 'Vacation approval for {} starting {} and ending {}'.format(
            self.vacation.for_user.username,
            self.vacation.start_date,
            self.vacation.end_date,
        )

# from django.contrib import admin
# admin.site.register(DailyTimesheet)
# admin.site.register(DailyTimesheetApproval)
# admin.site.register(Vacation)
# admin.site.register(VacationApproval)
