import base 
import utils   
import os  
import requests 

class FPL: 
    def __init__(self, session, user=None):  
        self.session = session 
        self.user = user 
        self.session = requests.Session()  
        self.db_handler = base.DBHandler  
    
    def get_current_user_picks(self): 
        if self.user: 
            data = utils.fetch(self.session, utils.api_urls['current-team'].format(self.user.id)) 
            return data['picks'] 
        return False 
    
    def get_current_user_rank(self): 
        return utils.fetch(self.session, utils.api_urls['user'].format(self.user.id))['summary_overall_rank']

    def get_current_user_leagues(self): 
        data = utils.fetch(self.session, utils.api_urls['user'].format(self.user.id))['leagues']['classic']  
        return [x['name'] for x in data] 

    def get_current_gameweek(self): 
        static = utils.read_json(os.path.join(os.getcwd(), 'json_data', 'static.json')) 
        for x in static['events']: 
            if x['is_current']: 
                return x['id'] 

    def update_fpl_data(self, type: str): 
        data = utils.fetch(self.session, utils.api_urls[type]) 
        utils.write_json(data, os.path.join(os.getcwd(), 'json_data', type+'.json'))  
    







    
