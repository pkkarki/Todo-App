from django import forms
from .models import Task


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "status"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Add New Task"}
            ),
            "status": forms.Select(attrs={"class": "form-control"}),
        }
