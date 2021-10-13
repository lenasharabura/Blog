from django.contrib import admin

from articles.models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'author')

    class Meta:
        model = Article


admin.site.register(Article, ArticleAdmin)
