# coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render_to_response
try :
    import simplejson as json
except:
    import json

def server_error(request):
    acc = [a.split(';')[0] for a in request.META['HTTP_ACCEPT'].split(',')]
    if 'text/html' not in acc and 'text/json' in acc:
        response = json.dumps({'error': 'internal server error','status_code':500})
        return HttpResponse(response)
    return render_to_response('common/500.html')


def page_not_found(request):
    acc = [a.split(';')[0] for a in request.META['HTTP_ACCEPT'].split(',')]
    if 'text/html' not in acc and 'text/json' in acc:
        response = json.dumps({'error': 'not found','status_code':'404'})
        return HttpResponse(response)
    return render_to_response('common/404.html')
