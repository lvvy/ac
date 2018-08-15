# coding:utf-8
from django.contrib import admin
# Register your models here.
from .models import Event, Personage, Country, Armament, Photo
from .admin_com import DecadeBeginListFilter
import requests
# 去掉删除功能
admin.site.disable_action('delete_selected')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'personage', 'location', 'type']}),
        (u'摘要/详情', {'fields': ['abstract', 'detail'], 'classes': ['collapse']}),
        (u'日期信息', {'fields': ['begin_time', 'end_time'], 'classes': ['collapse']}),
    ]
    filter_vertical = ["personage"]
    list_display = ('name', 'abstract', 'begin_time', 'end_time')
    list_display_links = ('name', 'abstract')
    # 搜索框
    search_fields = ['name', 'personage__name', 'abstract']
    list_filter = ['add_time', DecadeBeginListFilter, 'personage__type', 'personage__position']
    # 精确时间管理
    date_hierarchy = 'begin_time'


@admin.register(Personage)
class PersonageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'position', 'nation', 'type']}),
        (u'摘要/详情', {'fields': ['abstract', 'sex', 'nation'], 'classes': ['collapse']}),
        (u'日期信息', {'fields': ['birthday', 'die'], 'classes': ['collapse']}),
    ]
    list_display = ('name', 'nation', 'position', 'type', 'birthday', 'die')
    list_editable = ('position', 'type')
    list_display_links = ('name', 'nation')
    list_filter = ['add_time', 'position', 'sex', 'type', 'country__continent']
    search_fields = ['name', 'nation__name', 'abstract']
    radio_fields = {"nation": admin.VERTICAL}
    # raw_id_fields = ("nation",)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'type', 'leader', 'level', 'pid', 'continent', 'abstract', 'latitude', 'longitude']})
    ]
    list_display = ('id', 'name', 'type', 'leader', 'level', 'pid', 'continent', 'latitude', 'longitude')
    list_editable = ('pid', 'continent', 'level')
    list_display_links = ('name', 'type', 'leader')
    list_filter = ['add_time', 'type', 'continent', 'level', 'pid']
    search_fields = ['name']


admin.site.register(Armament)
admin.site.register(Photo)