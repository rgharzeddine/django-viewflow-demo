"""tasks module"""
# from demo.celery import app
from celery.decorators import task

from demo.example.models import DailyTimesheet


@task(name='calculate_sheet_payroll')
def calculate_sheet_payroll(sheet_id, *args, **kwargs):
    """calculates the sheet payroll asynchronously"""
    print('celery task called: %s' % sheet_id)
    sheet = DailyTimesheet.objects.get(id=int(sheet_id))
    sheet.calculate_payroll()
