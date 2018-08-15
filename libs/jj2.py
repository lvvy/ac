# coding: utf-8
"""添加自定义过滤器"""
import time
from datetime import datetime
from jinja2 import Environment
from jinja2.runtime import Undefined
from django.conf import settings

def do_date(date, format):
    """时间格式化, 支持整数时间戳
    ~ 用法：{{xxx|date('%Y-%m-%d %H:%M:%S')}}
    """
    if not date:
        return u''
    if isinstance(date, int):
        t = time.localtime(date)
        date = datetime(*t[:6])
    if settings.VER==3:
        s = date.strftime(format.encode('unicode-escape').decode()).encode().decode('unicode-escape')
    else:
        s = date.strftime(format.encode('utf-8')).decode('utf-8')
    return s


def do_default(value, default_value=u''):
    "默认值"
    if isinstance(value, Undefined) or (not value):
        return default_value
    return value


def do_weekcn(now):
    "过滤成中文星期几"
    return [u'一', u'二', u'三', u'四', u'五', u'六', u'日'][now.weekday()]


def do_cut(s, length, end='...'):
    "截取字符"
    if not s:
        return ''
    return s[:length] + (end if len(s) > length else '')


filters = {
    'date': do_date,
    'd': do_default,
    'default': do_default,
    'weekcn': do_weekcn,
    'cut': do_cut,
}


def finalize(o):
    "把None换成空"
    return '' if o is None else o


class MyUndefined(object):
    "把未定义变量处理为None"

    def __init__(self, *args, **kwargs):
        pass

    def __getattr__(self, name):
        if name[:2] == '__':
            raise AttributeError(name)
        return None

    def __str__(self):
        return u''

    def __len__(self):
        return 0

    def __iter__(self):
        if 0:
            yield None

    def __cmp__(self, other):
        return cmp(None, other)

    def __nonzero__(self):
        return False

    __bool__ = __nonzero__

    def __repr__(self):
        return ''


class Env(Environment):
    def __init__(self, *args, **kw):
        kw['extensions'] = ('jinja2.ext.with_',)  # 启用with语句
        Environment.__init__(self, *args, **kw)
        # 把未定义变量和None处理为空字符串
        self.finalize = finalize
        self.undefined = MyUndefined
        self.filters.update(filters)
