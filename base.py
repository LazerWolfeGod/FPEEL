from dataclasses import dataclass

@dataclass 
class Player: 
    player_id: int 
    name: str 
    composite_score: float 
    cost: float 
    team: int 
    position: int 

@dataclass 
class User: 
    user_id: int 
    name: str   
    email: str 
    password: str 
    remaining_budget: float 
    players: list 
    gameweek_score: int 
    total_score: int 

@dataclass 
class League: 
    id: int 
    name: str 
    standings: list 

class DBHandler: 
    pass 

class Optimiser: 
    pass 

class TransferOptimiser: 
    pass 

class ChipOptimiser: 
    pass 

def player_rating(player): 
    pass 

def team_rating(team): 
    pass 


