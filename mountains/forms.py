from django import forms
from .models import *
from django.utils.html import format_html
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe
from django.forms.widgets import CheckboxSelectMultiple


        
class ButtonSelectMultiple(CheckboxSelectMultiple):
    def __init__(self, queryset=None, *args, **kwargs):
        self.queryset = queryset
        super().__init__(*args, **kwargs)
        
    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = []

        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(self.attrs, attrs) if attrs else self.attrs

        output = []
        for tag in self.queryset:
            option_value = str(tag.pk)
            option_label = str(tag)
            is_checked = option_value in value

            button_attrs = final_attrs.copy()
            button_attrs['type'] = 'checkbox'
            button_attrs['name'] = name
            button_attrs['value'] = option_value
            button_attrs['data-tag-name'] = option_label

            if is_checked:
                button_attrs['class'] += ' selected'

            output.append(format_html(
                '<label class="mountain__reviewcrt--tag"><input{0} /> # {1}</label>',
                flatatt(button_attrs),
                option_label,
            ))

        return mark_safe('\n'.join(output))
    

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
        required=False,
        widget=forms.FileInput(
            attrs={
                'onchange': "previewImage(event)",
                'class': "mountain__reviewcrt--imgbox",
                'id': "id_image"
            }
        ),
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=ButtonSelectMultiple(
            queryset=Tag.objects.all(),
            attrs={
                'class': "visually-hidden"
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
        widget=ButtonSelectMultiple(
            queryset=Tag.objects.all(),
            attrs={
                'class': "visually-hidden"
            }
        ),
        label='태그 선택'
    )
        
    # sido2 = forms.CharField(label='시도', max_length=100, widget=forms.HiddenInput())
    # gugun2 = forms.CharField(label='시군구', max_length=100, widget=forms.HiddenInput())