from django.contrib import admin

from comments.models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'comment', 'commentator')

    class Meta:
        model = Comment


admin.site.register(Comment, CommentAdmin)
