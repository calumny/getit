from django.conf.urls import patterns, url, include

from api import views

urlpatterns = [
    url(r'^register/', views.register),
    url(r'get_token/', views.get_token),
    url(r'get_it/', views.get_it),
    url(r'get_stats/', views.get_stats, name='get_stats'),
    url(r'get_map_locations/', views.get_map_locations, name='get_map_locations'),
    url(r'did_i_give_it/', views.did_i_give_it),
    url(r'give_it/', views.give_it),
    url(r'confirm_location/', views.confirm_location),
    url(r'countdown/', views.countdown),
    url(r'count/', views.count),
    url(r'status/', views.status),
    url(r'set_gcm_token/', views.set_gcm_token),
    url(r'set_apns_token/', views.set_apns_token),
    url(r'get_generations/', views.get_generations),
]
