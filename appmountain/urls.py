from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.MountainIndex.as_view(), name='index'),
    path('category/<slug:cat_slug>/', views.MountainCategory.as_view(), name='category'),
    path('about/', views.about, name='about'),
    path('addmountain/', views.AddMountain.as_view(), name='add_mountain'),
    path('edit/<slug:slug>/', views.UpdateMountain.as_view(), name='edit_mountain'),
    path('contact/', views.contact, name='contact'),
   # path('login/', views.login, name='login'),
    path('mountain/<slug:mount_slug>/', views.ShowMountain.as_view(), name='mountain'),
    path('tag/<slug:tag_slug>/', views.TagMountainList.as_view(), name='tag')

]
