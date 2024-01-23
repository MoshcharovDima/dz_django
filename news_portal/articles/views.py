from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from .filters import NewsFilter
from django.views.decorators.http import require_POST
from django.urls import reverse
def news_list(request):
    news = Post.objects.filter(post_type='NW').order_by('-creation_time')
    return render(request, 'news_list.html', {'news': news})
def news_detail(request, news_id):
    news_item = get_object_or_404(Post, pk=news_id)
    return render(request, 'news_detail.html', {'news': news_item})
def news_list(request):
    news_list = Post.objects.filter(post_type='NW').order_by('-creation_time')
    paginator = Paginator(news_list, 10)  # Показывать по 10 новостей на странице

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'articles/news_list.html', {'page_obj': page_obj})

def search(request):
    news_list = Post.objects.all()
    news_filter = NewsFilter(request.GET, queryset=news_list)
    return render(request, 'articles/news_search.html', {'filter': news_filter})

@login_required
def create_news(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            news_item = form.save(commit=False)
            news_item.post_type = 'NW'
            news_item.save()
            form.save_m2m()
            return redirect('news_detail', pk=news_item.pk)
    else:
        form = PostForm()
    return render(request, 'articles/post_edit.html', {'form': form})
@login_required
def create_article(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.post_type = 'AR'
            article.save()
            form.save_m2m()
            return redirect('article_detail', pk=article.pk)
    else:
        form = PostForm()
    return render(request, 'articles/post_edit.html', {'form': form})

@login_required
@require_POST
def delete_news(request, pk):
    news = get_object_or_404(Post, pk=pk, post_type='NW')
    news.delete()
    return redirect(reverse('news_list'))
@login_required
@require_POST
def delete_article(request, pk):
    article = get_object_or_404(Post, pk=pk, post_type='AR')
    article.delete()
    return redirect(reverse('article_list'))

@login_required
def edit_news(request, pk):
    news = get_object_or_404(Post, pk=pk, post_type='NW')
    if request.method == "POST":
        form = PostForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            return redirect('news_detail', pk=news.pk)
    else:
        form = PostForm(instance=news)
    return render(request, 'articles/post_edit.html', {'form': form, 'post': news})

@login_required
def edit_article(request, pk):
    article = get_object_or_404(Post, pk=pk, post_type='AR')
    if request.method == "POST":
        form = PostForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = PostForm(instance=article)
    return render(request, 'articles/post_edit.html', {'form': form, 'post': article})

