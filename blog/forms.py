from django import forms

from .models import Comment


class EmailPostForm(forms.Form):
    """form for sent email"""
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    """form for commenting posts"""
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


class SearchForm(forms.Form):
    """form for search"""
    query = forms.CharField()
