from django_tables2 import tables, TemplateColumn, Column
# from django.utils.safestring import mark_safe

from . import models


class DailyTimesheetTable(tables.Table):
    """table class to display attachments"""

    delete_column = TemplateColumn(
        """<button
            class="btn btn-sm btn-danger"
            name="remove"
            value="{{ record.pk }}">
            <i class="fa fa-times"></i>&nbsp; Remove
            </button>
        """,
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
            'delete_column',
        )
        attrs = {'class': 'table table-bordered '}
