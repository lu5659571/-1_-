from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "full_name", "birth_date", "phone", "email"
        ]
        widgets = {
            "birth_date": forms.DateInput(
                attrs={"type": "date"}
            )
        }