from django.shortcuts import render,render_to_response
from django.http import HttpResponse, HttpRequest
from django.utils import simplejson
from django.template import RequestContext
 
import sys
import os
import math
import requests
import concurrent.futures

def load_url(url, timeout):
    conn = requests.get(url=url, timeout=timeout)
    return simplejson.loads(conn.content)

def index(request) :
	from datetime import datetime

	startTime = datetime.now()



	url='http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
	payload = {
		'key':'753C3B3FF04FD9A4B520F90BB97059D6',
		'steamids':'76561198064586875'}
	summaryURL=requests.get(url=url, params=payload)

	url='http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'

	payload = {
		'key':'753C3B3FF04FD9A4B520F90BB97059D6',
		'steamid':'76561198064586875&format:json',
		'include_appinfo':'1',
		'include_played_free_games':'1'}
	gamesURL=requests.get(url=url, params=payload)
	
	summaryJson=simplejson.loads(summaryURL.content)
	gamesJson=simplejson.loads(gamesURL.content)
	
	totalprice=0
	for i in gamesJson['response']['games']:
		if i['playtime_forever'] > 0:
			hours_played+=i['playtime_forever']/60
			key = i['appid']

			url='http://store.steampowered.com/api/appdetails/?appids='+str(key)+'&cc=US&l=english&v=1%20HTTP/1.1'
			gameinfoURL=requests.get(url=url)

			gameinfoJson=simplejson.loads(gameinfoURL.content)
			try:
				totalprice+=gameinfoJson[str(key)]['data']['price_overview']['final']
	        except Exception as exc:
	            print('%r generated an exception: %s' % (url, exc))
	        else:
	            print('%r page is %d bytes' % (url, len(data)))

	print(totalprice)
	print(datetime.now()-startTime)
	profile_data={
		'profile' : profile
	}
	render=render_to_response('base.html',profile_data,context_instance=RequestContext(request))
	return render

