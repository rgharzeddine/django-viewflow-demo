
from django import forms
from django.conf import settings

from .models import DailyTimesheet


class FillDailyTimesheetForm(forms.ModelForm):

    date = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMAT,
        widget=forms.DateInput(
            attrs={'class': 'datepicker week-start-date form-control'}))

    class Meta:
        model = DailyTimesheet
        fields = ['date', 'code']


class ApproveDailyTimesheetForm(forms.ModelForm):

    class Meta:
        model = DailyTimesheet
        fields = ['approval_status']
