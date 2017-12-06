"""main models"""

from django.contrib.auth.models import User

from django.db.models import (
    CASCADE,
    CharField,
    DateField,
    # OneToOneField,
    DateTimeField,
    ForeignKey,
    # Model,
)
from viewflow.models import Process


class DailyTimesheet(Process):

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

# class DailyTimesheetApproval(Process):
#     pass
    # sheet = OneToOneField(
    #     DailyTimesheet, on_delete=CASCADE, related_name='approval')
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
        related_name='approvals')
