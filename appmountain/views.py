from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

# Create your views here.
menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить Гору", 'url_name': 'add_mountain'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}]
data_db = [
    {'id': 1, 'title': 'Уктус', 'content': 'описание горы: Уктус', 'is_published': True},
    {'id': 2, 'title': 'Ежовая', 'content': 'описание горы: Ежовая', 'is_published': False},
    {'id': 3, 'title': 'Белая', 'content': 'описание горы: Белая', 'is_published': True},
]

def page_not_found(request, exceptions):
    return HttpResponseNotFound(f'<h1> Страница не найдена (VIEWS.PY)</h1>')
def index(request):
    template_name = 'appmountain/index.html'
    data = {
        'title': 'НАЗВАНИЕ',
        'menu': menu,
        'context': 'Горы',
        'posts': data_db      # название любое, но ПОСТЫ будут про горы
    }
    return render(request, template_name=template_name, context=data)
def show_mountain(request, mount_id):
    return HttpResponse(f"Отображение статьи с id = {mount_id}")

def categories(request, cat_slug):
    return HttpResponse(f"<h1>ГОРЫ по категориям</h1><p >slug:{ cat_slug }</p>")

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