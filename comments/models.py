from django.contrib.auth.models import User
from django.db import models

from articles.models import Article


class Comment(models.Model):
    name = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_names_set',
                             verbose_name='Статья', blank=True, null=True)
    comment = models.TextField(verbose_name="Комментарий")
    commentator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='username_sets',
                                    verbose_name='Автор комментария')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
