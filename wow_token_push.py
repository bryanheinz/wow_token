#!/usr/bin/env python3
import json
import time
import pathlib
import requests


token_dir = pathlib.Path(__file__).resolve().parent
settings_fp = token_dir / 'settings.json'
cache_path = token_dir / 'wow_at_cache.json'


def settings_file():
    '''This function reads the settings.json file or creates it if it doesn't
    exist. Returns a settings dictionary.'''
    if settings_fp.exists():
        with open(settings_fp, 'rb') as file:
            settings = json.loads(file.read())
    else:
        from base64 import b64encode
        print("Settings file not found, creating one...")
        push_price = int(input('Watch price > ').replace(',', ''))
        user_key = input('Pushover user key > ')
        app_token = input('Pushover app key > ')
        bliz_id = input('Blizzard API Client ID > ')
        bliz_secret = input('Blizzard API Client Secret > ')
        bliz_access_key = b64encode(f"{bliz_id}:{bliz_secret}".encode())
        settings = {
            'push_price'      : push_price,
            'push_user_key'   : user_key,
            'push_app_token'  : app_token,
            'bliz_access_key' : bliz_access_key
        }
        with open(settings_fp, 'w') as file:
            file.write(json.dumps(settings, indent=4))
    return(settings)

def get_new_at():
    '''This function gets a new access token and caches it.'''
    access_key = settings['bliz_access_key']
    response = requests.get(
        url='https://us.battle.net/oauth/token',
        params={
            'grant_type': 'client_credentials',
        },
        headers={
            'Authorization': f'Basic {access_key}',
        }
    )
    token_cache = response.json()
    # epoch time + expire seconds
    token_expire = int(time.time()) + token_cache['expires_in']
    token_cache['token_expire'] = token_expire
    with open(cache_path, 'w') as file:
        file.write( json.dumps(token_cache, indent=4) )
    return(token_cache['access_token'])

def read_at_cache():
    '''This function reads the access token cache or gets a new one if the token
    is expired.'''
    if not cache_path.exists():
        return(get_new_at())
    with open(cache_path, 'r') as file:
        token_cache = json.loads(file.read())
    if int(time.time()) > token_cache['token_expire']:
        return(get_new_at())
    else:
        return(token_cache['access_token'])

def get_wow_token_price():
    '''Return the current WoW Token price from Blizzard's API as a string.'''
    url = 'https://us.api.blizzard.com/data/wow/token/'
    params = {
        'namespace':'dynamic-us',
        'locale':'en_US'
    }
    response = requests.get(
        url=url,
        params=params,
        headers=headers
    )
    data = response.json()
    price = data['price']
    gold = str(price)[:-4]
    return(int(gold))

def pushover(msg):
    '''Send a push notification to Pushover.'''
    url = 'https://api.pushover.net/1/messages.json'
    data = {
        'user': settings['push_user_key'],
        'token': settings['push_app_token'],
        'message': msg
    }
    headers = { 'Content-type': 'application/x-www-form-urlencoded' }
    r = requests.post(url, data=data, headers=headers)
    if r.status_code != 200:
        print(r.text)
        print("Error sending push notification.")

def main():
    '''Main program - Get's the WoW Token price and compares it to the specified
    Pushover price.'''
    gold = get_wow_token_price()
    if gold <= settings['push_price']:
        pushover("Buy - {:,}".format(gold))


settings = settings_file()
access_token = read_at_cache()

headers = {
    'Authorization':f'Bearer {access_token}'
}


if __name__ == '__main__':
    main()
