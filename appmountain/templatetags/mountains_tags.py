from django import template
import appmountain.views as views
from appmountain.models import Category, TagMountain

register = template.Library()

@register.simple_tag()
def get_categories():
    return views.cats_db

@register.inclusion_tag('appmountain/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}

@register.inclusion_tag('appmountain/list_tags.html')
def show_all_tags():
    return {'tags': TagMountain.objects.all()}