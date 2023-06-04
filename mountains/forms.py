from django import forms
from .models import *

class ReviewCreationForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='태그 선택'
    )
    class Meta:
        model = Review
        fields = ['content', 'image', 'tags']