import base 
import utils   
import os  
import requests 

class FPL: 
    def __init__(self, user=None, cookies=None): 
        self.user = user  
        self.cookies = cookies 
        self.session = requests.Session() 
        self.db_handler = base.DBHandler(
            '5.133.180.245', 
            'espleyh', 
            'HE141005wgsb', 
            'espleyh_fpl' 
        ) 

    def user_picks(self): 
        pass 

    def user_leagues(self): 
        pass  

    def update_data(self, type: str):  
        data = utils.fetch(self.session, utils.api_urls[type]) 
        utils.write_json(data, os.path.join(os.getcwd(), 'json_data', type+'.json')) 
    


if __name__ == "__main__":  
    fpl = FPL() 
    fpl.update_data('static') 

