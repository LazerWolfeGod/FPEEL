import time 
import json  
import requests 

base_url = 'https://fantasy.premierleague.com/api/' 
api_urls = { 
    'login': 'https://users.premierleague.com/accounts/login/',
    'fantasy_login': 'https://fantasy.premierleague.com/login/',
    'static': '{}bootstrap-static/'.format(base_url), 
    'user': '{}entry/{{}}/'.format(base_url), 
    'league': '{}leagues-classic/{{}}/'.format(base_url), 
    'current-team': '{}my-team/{{}}/'.format(base_url), 
    'given-team': '{}entry/{{}}/event/{{}}/'.format(base_url) 
}   

def write_json(data, filename): 
    with open(filename, 'w') as f: 
        json.dump(data, f, indent=4)  

def read_json(filename): 
    with open(filename, 'r') as f: 
        return json.load(f) 

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

def get_account_cookies(session, email, password, retries=1, cooldown=1): 
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
                return False 
            time.sleep(cooldown)  

def get_current_gameweek(session): 
    data = fetch(session, api_urls['static']) 
    for x in data['events']: 
        if x['is_current']: 
            return x['id']

def convert_team(team_id): 
    pass 

def convert_team_short(team_idea): 
    pass 

def convert_position(position_id): 
    pass  
