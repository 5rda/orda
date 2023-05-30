from django import forms
from .models import Post, PostComment

class PostForm(forms.ModelForm):
    title = forms.CharField(
        label = False,
        widget = forms.TextInput(
            attrs = {
                'placeholder':'제목',
                'class': 'form-box',
            }
        )
    )
    class Meta:
        model = Post
        fields = ['title', 'content']

class PostCommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': '댓글 내용', 'class': 'form-control'}),
        label=''
    )

    class Meta:
        model = PostComment
        fields = ['content']