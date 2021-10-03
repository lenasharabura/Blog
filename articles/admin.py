from django.contrib import admin

from articles.models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'article', 'date', 'author')

    class Meta:
        model = Article


admin.site.register(Article, ArticleAdmin)
