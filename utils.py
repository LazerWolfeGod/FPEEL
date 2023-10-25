import base 
import time  
import json   
import os  
import mysql.connector 
import requests 

base_url = 'https://fantasy.premierleague.com/api/' 
api_urls = { 
    'login': 'https://users.premierleague.com/accounts/login/',
    'fantasy_login': 'https://fantasy.premierleague.com/login/',
    'static': '{}bootstrap-static/'.format(base_url), 
    'user': '{}entry/{{}}/'.format(base_url), 
    'league': '{}leagues-classic/{{}}/standings'.format(base_url),  
    'me': '{}me/'.format(base_url), 
    'current-team': '{}my-team/{{}}/'.format(base_url), 
    'given-team': '{}entry/{{}}/event/{{}}/'.format(base_url) 
}   

def update_static_data(session): 
    data = fetch(session, api_urls['static']) 
    write_json(data, os.path.join(os.getcwd(), 'json_data', 'static.json')) 

def write_json(data: json, path: str):  
    print(path, "PATHHH") 
    with open(path, 'w') as f: 
        json.dump(data, f, indent=4)  

def read_json(path): 
    with open(path, 'r') as f: 
        return json.load(f) 

def fetch(session, url, cookies=None, retries=2, cooldown=1):
    retries_count = 0 
    while True: 
        try: 
            with session.get(url, cookies=cookies) as response: 
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
    return {
        1: 'Arsenal',
        2: 'Aston Villa',
        3: 'Bournemouth',
        4: 'Brentford',
        5: 'Brighton',
        6: 'Burnley',
        7: 'Chelsea',
        8: 'Crystal Palace',
        9: 'Everton',
        10: 'Fulham',
        11: 'Liverpool',
        12: 'Luton',
        13: 'Manchester City',
        14: 'Manchester United',
        15: 'Newcastle',
        16: 'Nottingham Forest',
        17: 'Sheffield United',
        18: 'Spurs',
        19: 'West Ham',
        20: 'Wolves'
    }[team_id] 

def convert_team_short(team_idea): 
    pass  

def convert_position(position_id): 
    return {
        1: 'Goalkeeper', 
        2: 'Defender', 
        3: 'Midfielder', 
        4: 'Forward' 
    }[position_id]  

def create_user_object(session, cookies): 
    data = fetch(session, api_urls['me'], cookies=cookies)['player']
    return base.User( 
        data['entry'], 
        data['first_name'], 
        data['email'], 
        cookies 
    ) 

def create_player_object(player_id):  
    data = read_json(os.path.join(os.getcwd(), 'json_data', 'static.json'))['elements'] 
    for x in data: 
        if x['id'] == player_id: 
            data = x 
            break 
    return base.Player( 
        data['id'], 
        data['web_name'], 
        data['now_cost']/10, 
        data['team'], 
        data['element_type'], 
        data['selected_by_percent'], 
        data['form'], 
        0, 
        data['points_per_game'], 
        0, 
        data['total_points'], 
        None, 
        None 
    ) 

def connect_to_db(): 
    return mysql.connector.connect( 
        host='5.133.180.245', 
        user='espleyh', 
        password= 'HE141005wgsb', 
        database='espleyh_fpl'
    )

def colour_distance(c1, c2): 
    return ((c1[0]-c2[0])**2 +(c1[1]-c2[1])**2 + (c1[2]-c2[2])**2)**0.5

def rgb_to_string(rgb_list): 
    return 'rgb({},{},{});'.format(rgb_list[0], rgb_list[1], rgb_list[2]) 

def string_to_rgb(rgb_string): 
    return [int(x) for x in rgb_string.strip('rgb();').split(',')]      

def merge_sort(array, key=lambda x: x): 
    if len(array) > 1: 
        mid = len(array)//2 
        left = array[:mid] 
        right = array[mid:] 
        merge_sort(left, key) 
        merge_sort(right, key) 
        i = j = k = 0 
        while i < len(left) and j < len(right): 
            if key(left[i]) < key(right[j]): 
                array[k] = left[i] 
                i += 1 
            else: 
                array[k] = right[j] 
                j += 1 
            k += 1 
        while i < len(left): 
            array[k] = left[i] 
            i += 1 
            k += 1 
        while j < len(right): 
            array[k] = right[j] 
            j += 1 
            k += 1 
    return reversed(array) 





