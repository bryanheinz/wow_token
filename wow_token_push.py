#!/usr/bin/env python
import json
import urllib
import httplib
import urllib2

push_price = 180000 # minimum gold price before sending notification
key = ''            # https://pushover.net key
app_token = ''      # https://pushover.net app token



def token():
    url = 'https://data.wowtoken.info/snapshot.json'
    page = urllib2.urlopen(url)
    data = json.load(page)
    page.close()
    
    gold = data['NA']['formatted']['buy']
    raw_gold = data['NA']['raw']['buy']
    
    if raw_gold <= push_price:
        pushover("Buy - {0}".format(gold))
    
def pushover(msg):
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST",
                "/1/messages.json",
                urllib.urlencode({
                    "token": app_token,
                    "user": key,
                    "message": msg}),
                { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()
    

try:
    token()
except:
    pushover("wow_token_push exited with an error.")
