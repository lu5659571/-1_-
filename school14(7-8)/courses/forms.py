from django import forms
from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name", "level", "duration", "price"]

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "level": forms.Select(
                attrs={"class": "form-select"}
            ),
            "duration": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "price": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if len(name) < 3:
            raise forms.ValidationError(
                "Название должно содержать минимум 3 символа."
            )

        if Course.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError(
                "Курс с таким названием уже существует."
            )

        return name

    def clean_price(self):
        price = self.cleaned_data["price"]

        if price <= 0:
            raise forms.ValidationError(
                "Цена должна быть больше нуля."
            )

        return price

    def clean_duration(self):
        duration = self.cleaned_data["duration"]

        if not 1 <= duration <= 1000:
            raise forms.ValidationError(
                "Длительность должна быть от 1 до 1000 часов."
            )

        return duration