from dataclasses import dataclass 
import mysql.connector 
import pulp 

@dataclass 
class Player: 
    player_id: int 
    name: str 
    cost: float 
    team: int 
    position: int 
    ownership_percentage: float 
    form: float 
    fixture_diff: float 
    ppg: float 
    xga: float 
    total_points: int  
    composite_score: float = None 
    composite_score3: float = None 

@dataclass 
class User: 
    id: int 
    name: str   
    email: str  
    cookies: dict  

@dataclass 
class League: 
    id: int 
    name: str 
    standings: list 

class DBHandler: 
    def __init__(self, host, user, password, database): 
        self.host = host 
        self.user = user 
        self.password = password 
        self.database = database 
    
    def open_connection(self): 
        connection = mysql.connector.connect( 
            host=self.host, 
            user=self.user, 
            password=self.password, 
            database=self.database 
        ) 
        return connection   
    
    # MAYBE DO THIS SHIT IDFK

    def execute_query(self, connection, query, data=None): 
        pass 

    def execute_update(self, connection, query, data=None, data_to_update=None): 
        pass 

    def close_connection(self, connection): 
        connection.close() 

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
    @classmethod 
    def captain_chooser(cls, team: list) -> dict: 
        return { 
            'captain': max(team, key=lambda player: player.composite_score), 
            'vice_captain': max(team, key=lambda player: player.composite_score3) 
        } 
    
    @classmethod 
    def bench_boost_predict(cls, team: list) -> float: 
        return sum([player.composite_score for player in team[11:]]) 
    
    def interpolate_budget(cls, bench_importance: float, budget: float) -> float: 
        if bench_importance < 0 or bench_importance > 1: 
            raise ValueError('Bench importance value must be between 0 and 1') 
        min_multi = 0.83 
        max_multi = (220/3)/100 
        return budget*(min_multi + (max_multi - min_multi)*bench_importance)  

    def get_position_requirements(cls, team: list): 
        return {
            1: cls.position_constraints[1] - sum(1 for player in team if player.position == 1), 
            2: cls.position_constraints[2] - sum(1 for player in team if player.position == 2), 
            3: cls.position_constraints[3] - sum(1 for player in team if player.position == 3), 
            4: cls.position_constraints[4] - sum(1 for player in team if player.position == 4) 
        } 
    
    def generate_starters(cls, players: list, budget: float, chip_type: str):  
        key_function = cls.chip_switcher[chip_type] 
        problem = pulp.LpProblem('Starting_11_Optimiser', pulp.LpMaximize) 
        selected = pulp.LpVariable.dicts('Starters', [player.player_id for player in players], cat=pulp.LpBinary) 

        problem += pulp.lpSum(key_function(player)*selected[player.player_id] for player in players)   
        problem += pulp.lpSum(selected[player.player_id] for player in players) == cls.lineup_size 
        problem += pulp.lpSum(player.cost*selected[player.player_id] for player in players) <= budget 
        for position, (min, max) in cls.formation_constraints.items(): 
            problem += pulp.lpSum(selected[player.player_id] for player in players if player.position == position) >= min 
            problem += pulp.lpSum(selected[player.player_id] for player in players if player.position == position) <= max 
        for team in range(1, 21): 
            problem += pulp.lpSum(selected[player.player_id] for player in players if player.team == team) <= cls.team_max 
        
        problem.solve() 
        selected_team = [player for player in players if pulp.value(selected[player.player_id])==1]  
        budget_used = sum([player.cost for player in selected_team]) 
        return sorted(selected_team, key=lambda x: x.position), budget_used  
    
    
    def generate_bench(cls, players: list, budget: float, positions_left: dict, selected_11: list, chip_type: str) -> list:  
        key_function = cls.chip_switcher[chip_type]  
        problem = pulp.LpProblem('FPL_Optimiser', pulp.LpMaximize) 
        selected = pulp.LpVariable.dicts('Bench', [player.player_id for player in players], cat=pulp.LpBinary) 

        problem += pulp.lpSum(key_function(player)*selected[player.player_id] for player in players) 
        problem += pulp.lpSum(selected[player.player_id] for player in players) == cls.bench_size 
        problem += pulp.lpSum(player.cost*selected[player.player_id] for player in players) <= budget  
        problem += pulp.lpSum(selected[player] for player in players if player not in selected_11) 
        for position, value in positions_left.items(): 
            problem += pulp.lpSum(selected[player.player_id] for player in players if player.position == position) == value 
        problem.solve() 
        selected_bench = [player for player in players if pulp.value(selected[player.player_id])==1]  
        return sorted(selected_bench, key=lambda x: x.position) 
    
    @classmethod 
    def generate_team(self, players: list, budget: float, bench_importance: float, chip_type: str) -> list: 
        starter_budget = self.interpolate_budget(self, bench_importance, budget) 
        result_11, budget_used = self.generate_starters(self, players, starter_budget, chip_type)  
        bench_budget = budget-budget_used  
        positions_left = self.get_position_requirements(self, result_11) 
        result_bench = self.generate_bench(self, players, bench_budget, positions_left, players, chip_type)
        return result_11+result_bench


class RatingSystem: 
    players_weights = { 
        'form': 0.25, 
        'fixture_diff': 0.25, 
        'ppg': 0.4, 
        'xga': 0.1, 
        'total_points': 0.1, 
        'ownership_percentage': 0.1
    } 
    team_weights = {} 

    @classmethod 
    def get_player_rating(cls, player_information) -> float:  
        return sum([getattr(player_information, key)*cls.players_weights[key] for key in cls.players_weights.keys()]) 
    
    @classmethod 
    def get_team_rating(cls, team_information) -> float: 
        pass 

def FDR(): 
    # this might not even get made 
    pass 


