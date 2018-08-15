# coding:utf-8
import traceback
import logging
import time
import datetime
from functools import wraps
from django.conf import settings
from django.http import HttpResponseRedirect
from logs.models import Time

log = logging.getLogger(__name__)


def error_handler(func):
    """接口异常修饰器"""

    @wraps(func)
    def wrap(request, *args, **kw):
        try:
            return func(request, *args, **kw)
        except:
            exc = traceback.format_exc()
            log.error(exc)
            if settings.DEBUG:
                print(exc)
                return
            return HttpResponseRedirect('/errors/500/')

    return wrap


def ctim(func):
    '计算耗时'

    @wraps(func)
    def wrap(request, *args, **kw):
        begin = time.perf_counter()
        func(request, *args, **kw)
        end = time.perf_counter()
        elapsed = begin - end
        now = datetime.datetime.now()
        path = request.path
        name = func.__name__

