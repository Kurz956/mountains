from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from .models import Mountains, Category, TagMountain

# Create your views here.
menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить Гору", 'url_name': 'add_mountain'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}]

cats_db = [
    {'id': 1, 'name': 'Отличные'},
    {'id': 2, 'name': 'Норм'},
    {'id': 3, 'name': 'Так себе'},
]
def page_not_found(request, exceptions):
    return HttpResponseNotFound(f'<h1> Страница не найдена (VIEWS.PY)</h1>')
def index(request):
    posts = Mountains.published.all()
    template_name = 'appmountain/index.html'
    data = {
        'title': 'НАЗВАНИЕ',
        'menu': menu,
        'context': 'Горы',
        'posts': posts,      # название любое, но ПОСТЫ будут про горы
        'cat_selected': 0      # хотя у нас и там и прописано дефолтное значение - 0, так что это можно не писать
    }
    return render(request, template_name=template_name, context=data)
def show_mountain(request, mount_slug):
    mountain = get_object_or_404(Mountains, slug=mount_slug)
    template_name = 'appmountain/mountain.html'
    data = {
        'title': 'mountain.title',
        'menu': menu,
        'context': 'mountain.description',
        'mountain': mountain,
        'cat_selected': 1,
    }
    return render(request, template_name=template_name, context=data)

def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    template_name = 'appmountain/index.html'
    posts = Mountains.published.filter(cat_id=category.pk)
    data = {
        'title': f'Отображение по рубрикам {category.name}',
        'menu': menu,
        'posts': posts,  # название любое, но ПОСТЫ будут про горы
        'cat_selected': category.pk  # в list_categories будем сравненивать с cat.id и если да - подсвечивать
    }

    return render(request, template_name=template_name, context=data)

def about(request):
    template_name = 'appmountain/about.html'
    data = {
        'title': 'О Сайте',
        'context': 'about context',
        'menu': menu,
    }
    return render(request, template_name=template_name, context=data)


def addmountain(request):
    return HttpResponse("Добавление статьи")
def contact(request):
    return HttpResponse("Обратная связь")
def login(request):
    return HttpResponse("Авторизация")


def show_tag_mountainlist(request, tag_slug):
    tag = get_object_or_404(TagMountain, slug=tag_slug)
    template_name = 'appmountain/index.html'
    posts = tag.tags.filter(is_published=Mountains.Status.PUBLISHED)
    data = {
        'title': f'Тег: {tag.tags}',
        'menu': menu,
        'posts': posts,  # название любое, но ПОСТЫ будут про горы
        'cat_selected': None  # в list_categories будем сравненивать с cat.id и если да - подсвечивать
    }

    return render(request, template_name=template_name, context=data)