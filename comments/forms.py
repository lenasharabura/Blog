from django import forms

from comments.models import Comment


class CommentForm(forms.ModelForm):
    comment = forms.CharField(label='Новый комментарий', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Введите ваш комментарий'}))

    class Meta:
        model = Comment
        fields = ['comment']