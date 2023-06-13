from django import forms
from .models import Post, PostComment, Mountain
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostForm(forms.ModelForm):
    title = forms.CharField(
        label=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': '제목',
                'class': 'my-2 fs-5 p-2 focus:outline-[#A2E04E] outline-offset-2 rounded',
                'style': 'width: 100%;',
            }
        )
    )
    content = forms.CharField(
        widget=CKEditorUploadingWidget(
            attrs={
                'placeholder': '내용',
            }
        ),
        label=''
    )
    mountain = forms.ModelChoiceField(
        queryset=Mountain.objects.all(),
        empty_label=None,
        widget=forms.Select(
            attrs={
                'id': 'mountain',
                'required': True,
            }
        )
    )
    
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        initial = kwargs.get('initial', {})
        initial['mountain'] = instance.mountain if instance else None
        kwargs['initial'] = initial
        super(PostForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Post
        fields = ['title', 'content', 'mountain']
        widgets = {
            'content': CKEditorUploadingWidget(),
        }

class PostCommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '작성자에게 격려의 댓글을 달아주세요!', 
                'class': 'my-2 fs-6 p-2 focus:outline-none',
                'style': 'width: 90%;'}),
        label=''
    )

    class Meta:
        model = PostComment
        fields = ['content']