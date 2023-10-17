import time 
import json  
import requests 

base_url = 'https://fantasy.premierleague.com/api/' 
api_urls = { 
    'login': 'https://users.premierleague.com/accounts/login/',
    'fantasy_login': 'https://fantasy.premierleague.com/login/',
    'static': '{}bootstrap-static/'.format(base_url)
}  

def write_json(data, filename): 
    with open(filename, 'w') as f: 
        json.dump(data, f, indent=4) 

def fetch(session, url, retries=10, cooldown=1):
    retries_count = 0 
    while True: 
        try: 
            with session.get(url) as response: 
                return response.json() 
        except: 
            retries_count += 1  
            if retries_count == retries: 
                raise Exception("Too many retries") 
            time.sleep(cooldown)  

def get_account_cookies(session, email, password, retries=10, cooldown=1): 
    retries_count = 0 
    data = {
        'login': email, 
        'password': password, 
        'app': 'plfpl-web', 
        'redirect_uri': api_urls['fantasy_login']
    } 
    headers = { 
        'User-Agent': 'Dalvik', 
        'Accept-Language': 'en-US,enq=0.5'
    } 
    while True: 
        try: 
            with session.post(api_urls['login'], data=data, headers=headers): 
                return { 
                    'pl_profile': session.cookies['pl_profile'], 
                    'datadome': session.cookies['datadome']  
                }
        except: 
            retries_count += 1 
            if retries_count > retries: 
                raise Exception("Too many retries") 
            time.sleep(cooldown) 
