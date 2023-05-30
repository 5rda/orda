from django import forms
from .models import *

class MountainForm(forms.ModelForm):
    class Meta:
        model = Mountain
        fields = '__all__'