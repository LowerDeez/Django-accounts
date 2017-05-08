from django import forms
from .models import Article

class ArticleForm(forms.Form):
    status = forms.CharField(widget=forms.HiddenInput)
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255)
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        max_length=5000)

    class Meta:
        model = Article
        fields = ['status', 'title', 'content']
