from datetime import date
from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student

        fields = [
            "full_name",
            "birth_date",
            "phone",
            "email",
        ]

        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "birth_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),
        }

    def clean_birth_date(self):
        birth_date = self.cleaned_data["birth_date"]

        if birth_date >= date.today():
            raise forms.ValidationError(
                "Укажите корректную дату рождения."
            )

        return birth_date

    def clean_phone(self):
        phone = self.cleaned_data["phone"]

        digits = "".join(
            char for char in phone if char.isdigit()
        )

        if not 10 <= len(digits) <= 15:
            raise forms.ValidationError(
                "Введите корректный номер телефона."
            )

        return phone