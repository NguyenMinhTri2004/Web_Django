
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('new', views.new),
    path('favorite', views.favorite),
    path('category', views.category),
    path('search', views.search),
    path('profile', views.profile),
    path('register', views.register),
    path('hot', views.hot),
    path('login', views.Login),
    path('logout', views.logoutPage),
    path('manga/<str:id>/', views.manga),
    path('manga/<str:mangaId>/chapter/<str:chapterId>/', views.chapter),
]
