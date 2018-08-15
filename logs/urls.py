# coding:utf-8
__author__ = 'lv'

from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$',views.log ),
]
