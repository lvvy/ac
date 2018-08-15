# coding:utf-8
from django.conf.urls import url
from .import views
urlpatterns = [
    url(r'^404/', views.page_not_found),
    url(r'^500/', views.server_error),

]