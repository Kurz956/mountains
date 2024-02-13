from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<slug:cat_slug>/', views.show_category, name='category'),
    path('about/', views.about, name='about'),
    path('addmountain/', views.addmountain, name='add_mountain'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('mountain/<slug:mount_slug>/', views.show_mountain, name='mountain'),
    path('tag/<slug:tag_slug>/', views.show_tag_mountainlist, name='tag')

]
