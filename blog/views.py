from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Article

def article_list(request):
    articles = Article.objects.all().order_by('-published_at')
    return render(request, 'blog/list.html', {'articles': articles})

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'blog/detail.html', {'article': article})

@login_required
def article_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        text = request.POST['text']
        Article.objects.create(title=title, text=text, author=request.user)
        return redirect('article_list')
    return render(request, 'blog/form.html')

@login_required
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.title = request.POST['title']
        article.text = request.POST['text']
        article.save()
        return redirect('article_list')
    return render(request, 'blog/form.html', {'article': article})

@login_required
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    return redirect('article_list')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('article_list')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('article_list')
