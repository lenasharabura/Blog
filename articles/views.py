from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView

from articles.forms import ArticleForm
from articles.models import Article

__all__ = (
    'home',
    'show_article',
    'create_article',
    'save_article',
    'ArticleUpdateView',
    'ArticleDeleteView',
)

from comments.forms import CommentForm
from comments.models import Comment


def home(request):
    articles = Comment.objects.values_list('name', flat=True)
    articles = sorted(list(articles), key=lambda x: list(articles).count(x), reverse=True)

    sorted_articles = dict()
    i = 0
    while len(sorted_articles) != 5:
        if articles[i] not in sorted_articles:
            sorted_articles[articles[i]] = articles.count(articles[i])
        i += 1
    qs = Article.objects.filter(id__in=sorted_articles)
    top_articles = list(sorted_articles)
    for q in qs:
        top_articles[top_articles.index(q.id)] = {'article': q, 'count': sorted_articles[q.id]}
    print(sorted_articles)
    print(top_articles)

    qs = Article.objects.all()
    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'top_articles': top_articles}
    return render(request, 'articles/home.html', context)


def show_article(request, pk=None):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            obj = Comment()
            obj.name = article
            obj.comment = form.cleaned_data['comment']
            obj.commentator = request.user
            obj.save()
            return redirect('detail', pk=pk)

    form = CommentForm()
    article = get_object_or_404(Article, pk=pk)
    comments = article.name_set.all()
    context = {'article': article, 'comments': comments, 'form': form}
    return render(request, 'articles/detail.html', context)


def top_comments(request):
    articles = dict(Comment.objects.values('name'))
    sorted(articles, key=articles.get)
    print(articles)


class ArticleUpdateView(UpdateView):
    model = Article
    fields = ['name', 'article']
    template_name = 'articles/update.html'

    success_url = reverse_lazy('home')


class ArticleDeleteView(SuccessMessageMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


def create_article(request):
    form = ArticleForm()
    context = {'form': form}
    return render(request, 'articles/create.html', context)


def save_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        data = request.POST
        if form.is_valid():
            obj = Article()
            obj.name = data['name']
            obj.article = data['article']
            obj.author = request.user
            obj.save()

            messages.success(request, 'Статья успешно сохранена')
            return redirect('/')
        return render(request, 'articles/create.html', {"form": form})
    else:
        messages.error(request, 'Невозможно сохранить статью')
        return redirect('/')
