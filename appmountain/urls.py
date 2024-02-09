from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cats/<slug:cat_slug>', views.categories, name='cats'),
    path('about/', views.about, name='about'),
    path('addmountain/', views.addmountain, name='add_mountain'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('mountain/<int:mount_id>', views.show_mountain, name='mountain'),

]
