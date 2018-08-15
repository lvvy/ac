# coding:utf-8
from django.db import models
from django.conf import settings


class CommonInfo(models.Model):
    add_time = models.DateField(u'添加时间', auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        if settings.VER == 3:
            return self.name
        return self.name.encode('utf-8')


class Messages(CommonInfo):
    """报错信息"""
    LEVEL = (
        (1, 'm'),
        (2, 'c'),
        (3, 'b')
    )
    title = models.CharField(max_length=100)
    time = models.DateTimeField(blank=True, null=True)
    position = models.DateField(u'位置', blank=True, null=True, max_length=100)
    log = models.TextField(blank=True, null=True)
    level = models.IntegerField(u'类型', choices=LEVEL, default=1)

    class Meta:
        db_table = "log_message"


class Time(CommonInfo):
    '''接口信息记录'''
    function = models.CharField(max_length=30)
    time = models.DateTimeField(u'响应时间', blank=True, null=True)
    position = models.DateField(u'位置', blank=True, null=True, max_length=50)
    path = models.CharField(max_length=50)
