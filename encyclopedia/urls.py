from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('wiki/<str:entry>', views.entry_detail, name='entry_detail'),
    path('search/', views.search, name='search'),
    path('create_page/', views.create_page, name='create_page'),
    path('wiki/<str:entry>/edit', views.edit_page, name='edit_page'),
    path('random_page/', views.random_page, name='random_page')
]
