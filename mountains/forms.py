from django import forms
from .models import *

class ReviewCreationForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': "mountain__reviewcrt--cont",
                'placeholder': "내용를 입력하세요."
            }
        ),
    )

    image = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                'onchange': "previewImage(event)",
                'class': "mountain__reviewcrt--imgbox",
                'id': "id_image"
            }
        ),
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': "mountain__reviewcrt--tagbox"
            }
        ),
        label='태그 선택',
    )

    def clean_tags(self):
        selected_tags = self.cleaned_data.get('tags', [])
        if len(selected_tags) > 4:
            raise forms.ValidationError("태그는 4개까지 선택할 수 있습니다.")

        return selected_tags

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].widget.attrs['onclick'] = "limitCheckboxSelections(this, 4)"
    class Meta:
        model = Review
        fields = ['content', 'image', 'tags']


class SearchForm(forms.Form):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='태그 선택'
    )
    # sido2 = forms.CharField(label='시도', max_length=100, widget=forms.HiddenInput())
    # gugun2 = forms.CharField(label='시군구', max_length=100, widget=forms.HiddenInput())