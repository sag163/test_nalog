from .models import Nalog
from django import forms
from django.forms import ModelForm


class InnForm(forms.ModelForm):
    class Meta:
        model = Nalog
        fields = ("request_numbers",)
