from django.shortcuts import render,Http404,redirect
import requests
from .models import *
from django.contrib import messages
from datetime import datetime
from django.utils.timezone import now


API_KEY = '0da76c7c-a1db-41d5-94f2-9e41de11b016'
VALID_OPTIONS = ['currentMatches', 'players', 'match_info', 'players_info']


COUNTRY_CODE_MAP = {
    'India': 'in',
    'England': 'gb',
    'Luxembourg': 'lu',
    'Hungary': 'hu',
    'Switzerland': 'ch',
    'Slovenia': 'si',
    'Bangladesh': 'bd',
    'Nepal': 'np',
    'Netherlands': 'nl',
    'Vanuatu': 'vu',
    'Samoa': 'ws',
    'Sweden': 'se',
    'Papua New Guinea': 'pg'
}


def fetch_data(info):
    try:
        url = f'https://api.cricapi.com/v1/{info}?apikey={API_KEY}&offset=0'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': f'API error with status code {response.status_code}'}
    except Exception as e:
        return {'error': str(e)}


def cricket_data_view(request):
    try:
        url = f'https://api.cricapi.com/v1/currentMatches?apikey={API_KEY}&offset=0'
        response = requests.get(url)
        data = response.json() if response.status_code == 200 else {'data': []}
    except Exception as e:
        data = {'data': [], 'error': str(e)}

    return render(request, 'cricket.html', {'matches': data.get('data', [])})

def player_info_view(request):
    data = fetch_data('players') 
    players = data.get('data', []) if data else []

    COUNTRY_CODE_MAP = {
        'India': 'in', 'England': 'gb', 'Luxembourg': 'lu', 'Hungary': 'hu',
        'Switzerland': 'ch', 'Slovenia': 'si', 'Bangladesh': 'bd', 'Nepal': 'np',
        'Netherlands': 'nl', 'Vanuatu': 'vu', 'Samoa': 'ws', 'Sweden': 'se',
        'Papua New Guinea': 'pg'
    }
    for player in players:
        country = player.get('country', '')
        player['country_code'] = COUNTRY_CODE_MAP.get(country, '')
    return render(request, 'player.html', {'players': players})

def player_info_view(request):
    data = fetch_data('players') 
    players = data.get('data', []) if data else []

    for player in players:
        country = player.get('country', '')
        player['country_code'] = COUNTRY_CODE_MAP.get(country, '')

    return render(request, 'player.html', {'players': players})

def match_info_view(request):
    data = fetch_data('currentMatches')
    matches = data.get('data', []) if data else []
    return render(request, 'matches.html', {'matches': matches})

def match_detail_view(request, id):
    url = f'https://api.cricapi.com/v1/match_scorecard?apikey={API_KEY}&id={id}'

    response = requests.get(url)
    if response.status_code != 200:
        raise Http404("Failed to fetch match data")

    match_data = response.json().get("data")
    if not match_data:
        raise Http404("No data returned from API")

    return render(request, "match_detail.html", {"match": match_data})


def about_view(request):
    return render(request, 'about.html')

def isEmpty(value):
    return value is None or value is ''

def contact(request):
        if request.method == "POST":
                name = request.POST.get('name')
                phone = request.POST.get('phone')
                email = request.POST.get('email')
                desc = request.POST.get('desc')
                contact = Contact(name=name,phone=phone,email=email,desc=desc,date=datetime.today())
                if isEmpty(email):
                    messages.warning(request,"Name not be null")
                    return redirect('/contact/')
                contact.save()
                messages.success(request,'Your information has been submitted..!')
        return render(request,'contact.html',{'success': True, 'now': now()})

def default_url(request,id):
    return render(request,'default_url.html',context={'id' : id})