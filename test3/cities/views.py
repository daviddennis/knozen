import urllib2
from urllib2 import HTTPError, URLError
import json
from itertools import izip_longest
from operator import itemgetter
from time import sleep

from django.shortcuts import render

def index(request):
    city_names = []
    f = open('cities/cities.txt')
    for line in f.readlines():
        for city_name in _format_metro_areas_to_city_names(line.strip()):
            city_names += [city_name]
        
    temps = _get_city_temps(city_names)
    
    top_5_city_temps = sorted(temps.iteritems(), key=itemgetter(1), reverse=True)[:5]
    top_5_city_temps = [(city_name, 1.8*(temp - 273) + 32) for city_name, temp in top_5_city_temps]
    #print top_5_city_temps

    context = {
        'top_5_city_temps': top_5_city_temps
        }

    return render(request,
                  'index.html', 
                  context)


def _get_city_temps(city_names):
    temps = {}
    for i, city_name in enumerate(city_names):
        _city_name = _format_city_name(city_name)
        try:
            resp = urllib2.urlopen('http://api.openweathermap.org/data/2.5/weather?q=%s' % _city_name)
        except (HTTPError, URLError) as e:
            sleep(.5)
            continue
        except Exception as e:
            print "Warning, could not get data for %s: %s" % (city_name, e.message)
            sleep(.5)
            continue
        
        resp_json = json.loads(resp.read())
        temps[city_name] = float(resp_json.get("main", {"temp": 295.4}).get("temp")) # 72 degrees F
        #print i, city_name, temps[city_name]

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

