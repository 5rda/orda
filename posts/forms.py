from django import forms
from .models import Post, PostComment
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
        label='')

    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'content': CKEditorUploadingWidget(),
        }

class PostCommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '댓글 내용', 'class': 'form-control'}),
        label=''
    )

    class Meta:
        model = PostComment
        fields = ['content']