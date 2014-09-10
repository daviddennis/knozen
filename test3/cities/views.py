import urllib3
import json
from itertools import izip_longest

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader


def index(request):
    city_names = []
    f = open('cities/cities.txt')
    for line in f.readlines():
        for city_name in _format_metro_areas_to_city_names(line.strip()):
            city_names += [city_name]
        
    temps = self._get_city_temps(city_names)

    template = loader.get_template('cities/index.html')
    context = RequestContext(request, {
            'cities': [],
            'temps': []
        })
    return HttpResponse(render(context))


def _get_city_temps(city_names):
    temps = {}
    for city_name in city_names:
        city_name = _format_city_name(city_name)
        resp = urllib3.urlopen('http://api.openweathermap.org/data/2.5/weather?q=%s' % city_name)
        
        resp_json = json.loads(resp.read())
        temps[city_name] = float(resp_json.get("main", {"temp": 295.4}).get("temp"))
        break

    return temps

def _format_city_name(city_name):
    return city_name.replace(' ', '%20')


def _format_metro_areas_to_city_names(metro_area_line):
    tokens = metro_area_line.split(', ')
    city_token = tokens[0]
    if '-' in city_token:
        cities = city_token.split('-')
    else:
        cities = [city_token]
    
    state_token = tokens[1].replace(' Metropolitan Statistical Area', '')
    if '-' in state_token:
        states = state_token.split('-')
    else:
        states = [state_token]

    city_names = []
    prev_c = cities[0]
    prev_s = states[0]
    for c, s in izip_longest(cities, states):
        if c == None:
            c = prev_c
        if s == None:
            s = prev_s
        city_names += ['%s,%s' % (c,s)]
        prev_c = c
        prev_s = s

    return city_names

