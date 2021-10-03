from django import forms

from articles.models import Article


class ArticleForm(forms.ModelForm):
    name = forms.CharField(label='Название статьи', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Название статьи'
    }))

    article = forms.CharField(label='Текст статьи', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Текст статьи'}))

    class Meta:
        model = Article
        fields = '__all__'
