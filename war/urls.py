# coding:utf-8
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/', views.r_index),
    url(r'^country/$', views.r_country),
    url(r'^country/(?P<country_id>\d+)/$', views.r_country_detail),
    url(r'^index2/', views.r_index2),
]
