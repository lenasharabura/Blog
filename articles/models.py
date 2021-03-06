from django.contrib.auth.models import User
from django.db import models


class Article(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название статьи')
    article = models.TextField(verbose_name="Текст статьи")
    date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='username_set', verbose_name='Автор')
    likes = models.ManyToManyField(User, related_name='blog_articles')

    def __str__(self):
        return f'Название: {self.name}. Автор: {self.author}'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-date']


