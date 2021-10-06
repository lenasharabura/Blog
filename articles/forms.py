from django import forms


class ArticleForm(forms.Form):
    name = forms.CharField(label='Название статьи', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Название статьи'
    }))

    article = forms.CharField(label='Текст статьи', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Текст статьи'}))

