from django.conf.urls import patterns, url, include

from api import views

urlpatterns = [
    url(r'register/', views.register),
    url(r'get_token/', views.get_token),
    url(r'get_it/', views.get_it),
    url(r'give_it/', views.give_it),
    url(r'get_generations/', views.get_generations),
    
]