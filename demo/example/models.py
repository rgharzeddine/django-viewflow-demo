"""main models"""

from django.contrib.auth.models import User

from django.db.models import (
    CASCADE,
    CharField,
    DateField,
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
        related_name='approvals')

    def is_approved(self):
        return self.approval_status == 'approved'


class DailyTimesheetApproval(Process):

    sheet = OneToOneField(
        DailyTimesheet,
        on_delete=CASCADE,
        null=True,
        related_name='approval')

    name = CharField(
        max_length=50,
    )

    def __str__(self):
        if self.name:
            return self.name
        return str(self.pk) + ' :D'

    __repr__ = __str__
    str = __str__
