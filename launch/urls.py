from django.conf.urls import patterns, url, include

from launch import views

urlpatterns = [
    url(r'main/', views.main),
    url(r'', views.main),
    
]
