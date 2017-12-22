"""tasks module"""
# from demo.celery import app
from celery.decorators import task
import ctypes


def get_by_id(object_id):
    # return ctypes.cast(object_id, ctypes.py_object).value
    value = ctypes.cast(object_id, ctypes.py_object).value
    # print(value)
    return value


# @app.task(bind=True)


@task(name='calculate_sheet_payroll')
def calculate_sheet_payroll(activation_id, *args, **kwargs):
    """calculates the sheet payroll asynchronously"""
    print('celery task called')
    activation = ctypes.cast(activation_id, ctypes.py_object).value
    activation.process.sheet.calculate_payroll()
