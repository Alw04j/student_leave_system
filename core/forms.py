from django import forms
from django.core.exceptions import ValidationError
from .models import LeaveRequest
from django.utils import timezone


class LeaveRequestForm(forms.ModelForm):
    single_day = forms.BooleanField(required=False, label="Single Day Leave")

    class Meta:
        model = LeaveRequest
        fields = ['from_date', 'to_date', 'reason']
        widgets = {
            'from_date': forms.DateInput(attrs={'type': 'date'}),
            'to_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 3, 'class': 'w-full'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = timezone.now().date().isoformat()
        self.fields['from_date'].widget.attrs['min'] = today
        self.fields['to_date'].widget.attrs['min'] = today

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get("from_date")
        to_date = cleaned_data.get("to_date")
        single_day = cleaned_data.get("single_day")

        if from_date and from_date < timezone.now().date():
            raise ValidationError("From date cannot be in the past.")

        if to_date and to_date < timezone.now().date():
            raise ValidationError("To date cannot be in the past.")

        if single_day:
            cleaned_data['to_date'] = from_date
        elif from_date and to_date and from_date > to_date:
            raise ValidationError("From date cannot be after To date.")

        return cleaned_data

