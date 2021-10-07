from django import forms

from articles.models import Article


class ArticleForm(forms.Form):
    name = forms.CharField(label='Название статьи', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Название статьи',
    }))

    article = forms.CharField(label='Текст статьи', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Текст статьи',
        'style': 'white-space: pre-line;',
        'cols': 50,
        'rows': 8,
    }))


class ArticleModelForm(forms.ModelForm):
    name = forms.CharField(label='Название статьи', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Название статьи',
    }))

    article = forms.CharField(label='Текст статьи', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Текст статьи',
        'style': 'white-space: pre-line;',
        'cols': 50,
        'rows': 8,
    }))

    class Meta:
        model = Article
        fields = ['name', 'article']
