
from django import forms
from django.conf import settings

from .models import DailyTimesheet


class DailyTimesheetForm(forms.ModelForm):

    date = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMAT,
        widget=forms.DateInput(
            attrs={'class': 'datepicker week-start-date form-control'}))

    class Meta:
        model = DailyTimesheet
        fields = ['date', 'code']


class DailyTimesheetApprovalForm(forms.ModelForm):

    class Meta:
        model = DailyTimesheet
        fields = ['approval_status']


class DailyTimesheetUpdateForm(forms.ModelForm):

    date = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMAT,
        widget=forms.DateInput(
            attrs={'class': 'datepicker week-start-date form-control'}))

    class Meta:
        model = DailyTimesheet
        fields = ['date', 'code']
