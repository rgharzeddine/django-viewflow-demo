
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Field,
    Layout,
    HTML,
    ButtonHolder,
    Submit)


from .models import DailyTimesheet


class DailyTimesheetForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """initializes form with desired style configuration"""

        super(DailyTimesheetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form form-inline'
        self.helper.label_class = 'hidden'

    class Meta:
        model = DailyTimesheet
        fields = ['date', 'status']
        widgets = {'user': forms.HiddenInput()}
