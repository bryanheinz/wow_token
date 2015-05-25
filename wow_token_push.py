#!/usr/bin/env python
import json
import urllib
import httplib
import urllib2

class main(object):
    def __init__(self):
        self.push_price = 20000
        self.key = ''
        self.app_token = ''

    def token(self):
        url = 'https://wowtoken.info/wowtoken.json'
        page = urllib2.urlopen(url)
        data = json.load(page)
        page.close()
        
        self.gold = data['update']['NA']['formatted']['buy']
        self.raw_gold = data['update']['NA']['raw']['buy']
        self.date_stamp = data['update']['NA']['formatted']['updated']
        
        if self.raw_gold <= self.push_price:
            self.pushover()
            
    def pushover(self):
        conn = httplib.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
          urllib.urlencode({
            "token": self.app_token,
            "user": self.key,
            "message": "Buy %s" % self.gold,
          }), { "Content-type": "application/x-www-form-urlencoded" })
        conn.getresponse()
            
run = main()
run.token()