from django import template
from django.db.models import Count

import appmountain.views as views
from appmountain.models import Category, TagMountain
from appmountain.utils import menu

register = template.Library()

@register.simple_tag()
def get_categories():
    return views.cats_db

@register.inclusion_tag('appmountain/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()             # ОТОБРАЗИТЬ ВСЕ КАТЕГОРИИ В САЙДБАРЕ
    #cats = Category.objects.annotate(total=Count('mountains')).filter(total__gt=0) # ОТОБРАЗИТЬ НЕ ПУСТЫЕ КАТЕГОРИИ В САЙДБАРЕ
    return {'cats': cats, 'cat_selected': cat_selected}

@register.inclusion_tag('appmountain/list_tags.html')
def show_all_tags():
    #return {'tags': TagMountain.objects.all()}  # ОТОБРАЗИТЬ ВСЕ ТЕГИ В САЙДБАРЕ
    return {'tags': TagMountain.objects.annotate(total=Count('tags')).filter(total__gt=0)} # ОТОБРАЗИТЬ НЕ ПУСТЫЕ ТЕГИ В САЙДБАРЕ


@register.simple_tag
def get_menu():
    return menu