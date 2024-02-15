from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

from .forms import AddMountainForm, UploadFileForm
from .models import Mountains, Category, TagMountain, UploadFiles

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

class MountainIndex(ListView):
    model = Mountains
    template_name = 'appmountain/index.html'
    context_object_name = 'posts'
    extra_context = {
        'title': 'НАЗВАНИЕ',
        'menu': menu,

        'cat_selected': 0  # хотя у нас и там и прописано дефолтное значение - 0, так что это можно не писать
    }
    #
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['menu'] = menu
        context['cat_selected'] = 0
        return context

    def get_queryset(self):
        return Mountains.objects.all().select_related('cat')

class ShowMountain(DetailView):
    model = Mountains
    template_name = 'appmountain/mountain.html'
    slug_url_kwarg = 'mount_slug'
    context_object_name = 'mountain'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['mountain']
        context['menu'] = menu
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Mountains.published, slug=self.kwargs[self.slug_url_kwarg])


class UpdateMountain(UpdateView):
    model = Mountains
    fields = ['title', 'description', 'photo', 'is_published', 'cat']
    template_name = 'appmountain/addmountain.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'menu': menu,
        'title': "Редактирование статьи",
    }
class MountainCategory(ListView):
    template_name = 'appmountain/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        context['title'] = f'Категория - {cat.name}'
        context['menu'] = menu
        context['cat_selected'] = cat.id
        return context

    def get_queryset(self):
        return Mountains.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

def about(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    data = {
        'title': 'О сайте',
        'menu': menu,
        'form': form,
    }
    template_name = 'appmountain/about.html'
    return render(request, template_name=template_name, context=data)

class AddMountain(CreateView):
    form_class = AddMountainForm
    template_name = 'appmountain/addmountain.html'
    extra_context = {
        'menu': menu,
        'title': "Добавление статьи",
    }

def contact(request):
    return HttpResponse("Обратная связь")
def login(request):
    return HttpResponse("Авторизация")

class TagMountainList(ListView):
    template_name = 'appmountain/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = context['posts'][0].tags
        context['title'] = f'Тэг - {tag.name}'
        context['menu'] = menu
        context['cat_selected'] = None
        return context

    def get_queryset(self):
        return Mountains.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')
