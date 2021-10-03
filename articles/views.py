import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView

from articles.forms import ArticleForm
from articles.models import Article

__all__ = (
    'home',
    'show_article',
    'ArticleCreateView',
    'create_article',
    'save_article',
)


def home(request):
    qs = Article.objects.all()
    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'articles/home.html', context)


def show_article(request, pk=None):
    article = get_object_or_404(Article, pk=pk)
    comments = article.name_set.all()
    context = {'article': article, 'comments': comments}
    return render(request, 'articles/detail.html', context)


class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/create.html'
    success_url = reverse_lazy('articles:home')
    success_message = "Статья успешно создана"


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

            messages.success(request, 'Маршрут успешно сохранен')
            return redirect('/')
        return render(request, 'articles/create.html', {"form": form})
    else:
        messages.error(request, 'Невозможно сохранить статью')
        return redirect('/')
