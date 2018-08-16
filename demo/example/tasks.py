"""tasks module"""
# from demo.celery import app
# from celery.decorators import task
from celery import shared_task

from demo.example.models import DailyTimesheet
from viewflow.decorators import flow_job


@shared_task
@flow_job
def calculate_sheet_payroll(activation, **kwargs):
    """calculates the sheet payroll asynchronously"""
    print('celery task called')
    sheet_id = activation.process.sheet.pk
    sheet = DailyTimesheet.objects.get(id=int(sheet_id))
    sheet.calculate_payroll()
    return 'happy new year'
