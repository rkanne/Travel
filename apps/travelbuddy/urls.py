from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^insert$', views.insert),
    url(r'^login$', views.login),
    url(r'^travels$', views.trips),
    url(r'^success$', views.trips),
    url(r'^travels/add$', views.add_trips), 
    url(r'^travels/(?P<id>\d+)$', views.delete),
    url(r'^travels/destination/(?P<id>\d+)$', views.user_destination),
    url(r'^travels/join/(?P<id>\d+)$', views.join),
    url(r'^travels/delete/(?P<id>\d+)$', views.delete),    
    url(r'^remove/(?P<trip_id>\d+)/(?P<id>\d+)$', views.remove_join),
    url(r'^logout$', views.logout)

]