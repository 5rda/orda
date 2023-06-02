from django import forms
from .models import *

class ReviewCreationForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'image', 'tags']