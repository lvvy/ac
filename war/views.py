# coding:utf-8
from django.http import HttpResponseRedirect

from django.views import generic
from django.shortcuts import render, render_to_response
from .models import Personage, Armament, Country, Event, Photo
from libs.utils import error_handler


@error_handler
def r_index(request):
    events = Event.objects.order_by('-begin_time').select_related().all()
    return render_to_response('war/index.html', {"events": events})


def r_country(request):
    county = Country.objects.order_by('continent').select_related().all()
    return render_to_response('war/country.html', {"county": county})


def r_country_detail(request, country_id):
    country_id = int(country_id)
    country = Country.objects.filter(pk=country_id).select_related().first()
    if not country:
        return HttpResponseRedirect('/errors/404/')
    person = country.personage_set.order_by('position').all()[:3]
    event = Event.objects.filter(personage__nation=country_id).distinct().all()[:3]
    return render_to_response('war/country_detail.html', {"country": country, 'person': person, 'event': event})


def r_index2(request):
    events = Event.objects.order_by('-begin_time').select_related().all()
    return render_to_response('war/index2.html', {"events": events})


class Index2View(generic.ListView):
    template_name = 'war/index2.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Event.objects.order_by('-begin_time').select_related().all()
