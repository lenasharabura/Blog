from django.shortcuts import render

from comments.forms import CommentForm


def create_comment(request):
    form = CommentForm()
    context = {'form': form}
    return render(request, '/', context)