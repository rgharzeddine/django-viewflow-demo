from django_tables2 import tables, TemplateColumn, Column
# from django.utils.safestring import mark_safe
from viewflow.models import Process, Task

from . import models


class DailyTimesheetTable(tables.Table):
    """table class to display attachments"""

    delete_column = TemplateColumn(
        "No actions",
        # """<a href="{% url 'update_daily' record.pk %}"
        #     class="btn btn-sm btn-primary">
        #     <i class="fa fa-edit"></i>&nbsp; Modify
        #     </a>
        # """,
        verbose_name='Actions',
        orderable=False,
    )
    date = Column(
        verbose_name='Date',
        orderable=False,
        accessor='date',
    )
    code = Column(
        verbose_name='Code',
        orderable=False,
        accessor='code',
    )
    for_user = Column(
        verbose_name='User',
        orderable=False,
        accessor='for_user',
    )
    approval_status = Column(
        verbose_name='Approval Status',
        orderable=False,
        accessor='approval_status',
    )
    approved_by = Column(
        verbose_name='Approved By',
        orderable=False,
        accessor='approved_by',
    )
    approved_at = Column(
        verbose_name='Approved At',
        orderable=False,
        accessor='approved_at',
    )

    class Meta:
        """Meta Attributes"""
        orderable = False
        model = models.DailyTimesheet
        fields = (
            'date',
            'code',
            'for_user',
            'approval_status',
            'approved_by',
            'approved_at',
            # 'delete_column',
        )
        attrs = {'class': 'table table-bordered '}


class TaskTable(tables.Table):
    """table class to display attachments"""

    delete_column = TemplateColumn(
        "No actions",
        # """<a href="{% url 'update_daily' record.pk %}"
        #     class="btn btn-sm btn-primary">
        #     <i class="fa fa-edit"></i>&nbsp; Modify
        #     </a>
        # """,
        verbose_name='Actions',
        orderable=False,
    )
    created = Column(
        verbose_name='Created at',
        orderable=False,
        accessor='created',
    )
    status = Column(
        verbose_name='Status',
        orderable=False,
        accessor='status',
    )
    comments = Column(
        verbose_name='Comments',
        orderable=False,
        accessor='comments',
    )
    owner = Column(
        verbose_name='Owner',
        orderable=False,
        accessor='owner.username',
    )

    class Meta:
        """Meta Attributes"""
        orderable = False
        model = Task
        fields = (
            'comments',
            'created',
            'status',
            'owner',
            # 'delete_column',
        )
        attrs = {'class': 'table table-bordered '}
