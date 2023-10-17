from dataclasses import dataclass

@dataclass 
class Player: 
    player_id: int 
    name: str 
    composite_score: float  
    composite_score3: float 
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
    lineup_size = 11 
    bench_size = 4 
    team_max = 3 
    formation_constraints = { 
        1: (1, 1), 
        2: (3, 5), 
        3: (2, 5), 
        4: (1, 3) 
    } 
    position_constraints = { 
        1: 2, 
        2: 5, 
        3: 5,
        4: 3
    }

class TransferOptimiser(Optimiser): 
    pass 

class ChipOptimiser(Optimiser): 
    chip_switcher = { 
        'free_hit': lambda player: player.composite_score, 
        'wildcard': lambda player: player.composite_score3 
    }

def player_rating(player): 
    pass 

def team_rating(team): 
    pass 


