import base 
import utils   
import os  
import requests 

class FPL: 
    def __init__(self, user=None):  
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
        pass  

    def update_fpl_data(self, type: str): 
        data = utils.fetch(self.session, utils.api_urls[type]) 
        utils.write_json(data, os.path.join(os.getcwd(), 'json_data', type+'.json'))  
    

user = utils.create_user_object(requests.Session(), utils.get_account_cookies(requests.Session(), 'harryespley@outlook.com', 'James141005!')) 
fpl = FPL(user)  
print(fpl.get_current_user_leagues()) 






    
