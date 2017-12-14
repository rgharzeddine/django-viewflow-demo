
from django import forms
from django.conf import settings

from .models import DailyTimesheet, Vacation


# dailytimesheet flow forms
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


# vacation flow forms
class FillVacationForm(forms.ModelForm):

    start_date = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMAT,
        widget=forms.DateInput(
            attrs={'class': 'datepicker week-start-date form-control'}))

    end_date = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMAT,
        widget=forms.DateInput(
            attrs={'class': 'datepicker week-start-date form-control'}))

    details = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Vacation
        fields = ['start_date', 'end_date', 'details']


class ApproveVacationForm(forms.ModelForm):

    class Meta:
        model = Vacation
        fields = ['approval_status']
