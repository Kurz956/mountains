from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

from .forms import AddMountainForm, UploadFileForm
from .models import Mountains, Category, TagMountain, UploadFiles
from .utils import DataMixin

# Create your views here.


cats_db = [  # сюда ссылается navbar пока что
    {'id': 1, 'name': 'Отличные'},
    {'id': 2, 'name': 'Норм'},
    {'id': 3, 'name': 'Так себе'},
]
def page_not_found(request, exceptions):
    return HttpResponseNotFound(f'<h1> Страница не найдена (VIEWS.PY)</h1>')


class MountainIndex(DataMixin, ListView):
    model = Mountains
    template_name = 'appmountain/index.html'
    context_object_name = 'posts'


    def get_context_data(self, *, object_list=None, **kwargs):
        return self.get_mixin_context(super().get_context_data(**kwargs),
                                      title='Главная страница',
                                      cat_selected=0,)

    def get_queryset(self):
        return Mountains.objects.all().select_related('cat')

class ShowMountain(DataMixin, DetailView):
    model = Mountains
    template_name = 'appmountain/mountain.html'
    slug_url_kwarg = 'mount_slug'
    context_object_name = 'mountain'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context,
                                      title=context['mountain'])

    def get_object(self, queryset=None):
        return get_object_or_404(Mountains.published, slug=self.kwargs[self.slug_url_kwarg])


class UpdateMountain(UpdateView):
    model = Mountains
    fields = ['title', 'description', 'photo', 'is_published', 'cat']
    template_name = 'appmountain/addmountain.html'
    success_url = reverse_lazy('index')
    title_page = "Редактирование статьи"


class MountainCategory(DataMixin, ListView):
    template_name = 'appmountain/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title = f'Категория - {cat.name}',
                                      cat_selected = cat.id,
                                      )


    def get_queryset(self):
        return Mountains.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')


@login_required
def about(request):
    contact_list = Mountains.published.all()
    paginator = Paginator(contact_list, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    # if request.method == 'POST':
    #     form = UploadFileForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         fp = UploadFiles(file=form.cleaned_data['file'])
    #         fp.save()
    # else:
    #     form = UploadFileForm()
    data = {
        'title': 'О сайте',
       # 'form': form,
        'page_obj': page_obj,
    }
    template_name = 'appmountain/about.html'
    return render(request, template_name=template_name, context=data)


class AddMountain(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddMountainForm
    template_name = 'appmountain/addmountain.html'
    title_page = "Добавление статьи"

    def form_valid(self, form):
        mount = form.save(commit=False)
        mount.author = self.request.user
        return super().form_valid(form)

def contact(request):
    return HttpResponse("Обратная связь")
def login(request):
    return HttpResponse("Авторизация")


class TagMountainList(DataMixin, ListView):
    template_name = 'appmountain/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = context['posts'][0].tags
        return self.get_mixin_context(context,
                                      title = f'Тэг - {tag.name}',
                                      )


    def get_queryset(self):
        return Mountains.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')
