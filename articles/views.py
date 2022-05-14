from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView

from articles.forms import ArticleForm, ArticleModelForm
from articles.models import Article

from comments.forms import CommentForm
from comments.models import Comment

__all__ = (
    'home',
    'show_article',
    'save_article',
    'ArticleUpdateView',
    'ArticleDeleteView',
    'save_comment',
    'like_article',
    'test'
)


def test(request):
    return render(request, 'ДЗ5.html')


def home(request):
    articles = Comment.objects.values_list('name', flat=True)
    # создание списка всех комментариев упорядоченных по количеству комментариев
    articles = sorted(list(articles), key=lambda x: list(articles).count(x), reverse=True)
    # создание упорядоченного словаря, где ключ - id статьи, а значение - кол-тво комментариев
    sorted_articles = dict()
    i = 0
    while len(sorted_articles) != 5:
        if articles[i] not in sorted_articles:
            sorted_articles[articles[i]] = articles.count(articles[i])
        i += 1
    # получение queryset с экземплярами нужных статей
    qs = Article.objects.filter(id__in=sorted_articles)
    # создание списка на основе упорядоченного по кол-тву комментариев словаря
    top_articles = list(sorted_articles)
    # замена элементов списка на словари
    for q in qs:
        top_articles[top_articles.index(q.id)] = {'article': q, 'count': sorted_articles[q.id]}

    qs = Article.objects.all()
    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'top_articles': top_articles}
    return render(request, 'articles/home.html', context)


def like_article(request, pk):
    post = get_object_or_404(Article, id=request.POST.get('article_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('detail', pk=pk)


def save_comment(request, pk=None):
    article = get_object_or_404(Article, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        obj = Comment()
        obj.name = article
        obj.comment = form.cleaned_data['comment']
        obj.commentator = request.user
        obj.save()
        return redirect('detail', pk=pk)


def show_article(request, pk=None):
    if request.method == 'POST':
        save_comment(request, pk)
    form = CommentForm()
    article = get_object_or_404(Article, pk=pk)
    liked = False
    if article.likes.filter(id=request.user.id).exists():
        liked = True
    users = article.likes.all()
    total_likes = article.likes.count()
    comments = article.article_names_set.all()
    context = {'article': article, 'comments': comments, 'form': form, 'total_likes': total_likes, 'liked': liked,
               'users': users}
    return render(request, 'articles/detail.html', context)


class ArticleUpdateView(SuccessMessageMixin, UpdateView):
    model = Article
    form_class = ArticleModelForm
    template_name = 'articles/update.html'
    success_message = 'Статья успешно отредактирована'

    def get_success_url(self, **kwargs):
        return reverse_lazy('detail', kwargs={'pk': self.kwargs['pk']})


class ArticleDeleteView(SuccessMessageMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('home')
    success_message = 'Статья успешно удалена'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


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

            messages.success(request, 'Статья успешно создана')
            return redirect('/')
        return render(request, 'articles/create.html', {"form": form})
    else:
        form = ArticleForm()
        context = {'form': form}
        return render(request, 'articles/create.html', context)
