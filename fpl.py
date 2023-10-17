import base 
import utils   
import os  
import requests 

class FPL: 
    def __init__(self): 
        self.session = requests.Session() 

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

