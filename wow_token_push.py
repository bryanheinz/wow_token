#!/usr/bin/env python3
import json
import urllib.parse
import urllib.request


# Adjustable Variables #
push_price = 150000    # minimum gold price before sending notification
user_key = ''          # https://pushover.net key
app_token = ''         # https://pushover.net app token
# Adjustable Variables #


# Main Code #
def token():
    data, encoding = fetch_data('https://wowtokenprices.com/current_prices.json')
    
    try:
        json_data = json.loads(data.decode(encoding))
        gold = data['us']['current_price']
    except json.decoder.JSONDecodeError:
        # fallback if current_prices isn't returning data
        data, encoding = fetch_data(
            'https://wowtokenprices.com/history_prices_1_day.json'
        )
        json_data = json.loads(data.decode(encoding))
        gold = json_data['us'][-1]['price']
    
    if gold <= push_price:
        pushover("Buy - {:,}".format(gold))

def fetch_data(url):
    with urllib.request.urlopen(url) as page:
        encoding = page.info().get_content_charset('utf-8')
        data = page.read()
    return(data, encoding)

def pushover(msg):
    url = 'https://api.pushover.net:443/1/messages.json'
    
    headers = {
        'Content-type':'application/x-www-form-urlencoded',
    }
    
    data = urllib.parse.urlencode({
        'token':app_token,
        'user':user_key,
        'message':msg
    }).encode('utf-8')
    
    req = urllib.request.Request(url, headers=headers, data=data)
    urllib.request.urlopen(req).close()

try:
    token()
except Exception as e:
    print(e)
    pushover("wow_token_push exited with an error.")
