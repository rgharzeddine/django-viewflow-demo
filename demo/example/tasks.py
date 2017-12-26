"""tasks module"""
# from demo.celery import app
from celery.decorators import task

from demo.example.models import DailyTimesheet


@task(name='calculate_sheet_payroll')
def calculate_sheet_payroll(sheet_id, *args, **kwargs):
    """calculates the sheet payroll asynchronously"""
    print('celery task called: %s' % sheet_id)
    done = False
    counter = 1

    # sometimes for an unkown reason yet:
    # DailyTimesheet.objects.get(id=int(sheet_id)) raises DoesNotExist
    while not done:
        try:
            sheet = DailyTimesheet.objects.get(id=int(sheet_id))
            print('tried %s time(s)' % counter)
            sheet.calculate_payroll()
            done = True
        except:
            counter += 1
            pass
