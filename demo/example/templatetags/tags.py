# from django import template
# from demo.example.models import DailyTimesheet

# register = template.Library()


# @register.inclusion_tag('example/user_dailytimesheets.html')
# def user_dailytimesheets(user):
#     """returns user daily timesheets"""
#     context = {'sheets': DailyTimesheet.objects.filter(user=user)}
#     return context
