import base 
import utils   
import os  
import requests 

class FPL: 
    def __init__(self, session, user=None):  
        self.session = session 
        self.user = user 
        self.session = requests.Session()   
        self.db_connection = utils.connect_to_db()    
    
    def get_all_players(self): 
        cursor = self.db_connection.cursor() 
        cursor.execute('SELECT * FROM players') 
        data = cursor.fetchall() 
        cursor.close() 
        return [base.Player(*x) for x in data] 
    
    def get_current_user_picks(self): 
        if self.user: 
            data = utils.fetch(self.session, utils.api_urls['current-team'].format(self.user.id), cookies=self.session.cookies)     
            ids_list = [x for x in data['picks']] 
            return ids_list
        return False   
    
    def get_current_user_rank(self): 
        return utils.fetch(self.session, utils.api_urls['user'].format(self.user.id))['summary_overall_rank']

    def get_current_user_leagues(self): 
        data = utils.fetch(self.session, utils.api_urls['user'].format(self.user.id))['leagues']['classic']  
        return [x for x in data]  

    def get_current_user_balance(self): 
        return utils.fetch(self.session, utils.api_urls['user'].format(self.user.id))['last_deadline_bank']/10 

    def get_current_gameweek(self): 
        static = utils.read_json(os.path.join(os.getcwd(), 'json_data', 'static.json')) 
        for x in static['events']: 
            if x['is_current']: 
                return x['id']  
    
    def get_player_from_id(self, player_id): 
        data = utils.read_json(os.path.join(os.getcwd(), 'json_data', 'static.json')) 
        for x in data['elements']: 
            if x['id'] == player_id: 
                return x['web_name'] 

    def update_fpl_data(self, type: str): 
        data = utils.fetch(self.session, utils.api_urls[type]) 
        utils.write_json(data, os.path.join(os.getcwd(), 'json_data', type+'.json'))   
    
    # returns the standings in json format of a league when inputted with the league id 
    def get_league_standings(self, league_id): 
        return utils.fetch(self.session, utils.api_urls['league'].format(league_id))['standings']['results']  
    


USE_THIS = "https://fantasy.premierleague.com/api/fixtures/" 


    







    
