from dataclasses import dataclass 
import mysql.connector 
import pulp 

@dataclass 
class Player: 
    player_id: int 
    name: str 
    cost: float  
    total_points: int 
    position: int 
    team: int 
    ppg: float 
    owned_by: float 
    composite_score: float                                                  
    sell_cost: float = None  

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

class DB_Handler: 
    pass  

class Queue: 
    def __init__(self): 
        self.items = [] 
    
    def enqueue(self, item): 
        self.items.append(item) 

    def dequeue(self): 
        self.items.pop(0)

    @property 
    def front(self): 
        return self.items[0] 
    
    @property 
    def back(self): 
        return self.items[-1] 

    def is_empty(self): 
        return not self.items 

class Stack: 
    def __init__(self): 
        self.items = []   
    
    def push(self, item): 
        self.items.append(item) 
    
    def pop(self): 
        self.items.pop()   

    @property    
    def top(self): 
        return self.items[-1] 
    
    @property 
    def bottom(self): 
        return self.items[0]                
    
    def is_empty(self): 
        return not self.items 

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
    def generate_transfers(self, players, current_team, budget, max_transfers, number_of_suggestions=10): 
        problem = pulp.LpProblem('FPL_Optimiser', pulp.LpMaximize) 
        remove_player = pulp.LpVariable.dicts('Remove', [player.player_id for player in current_team], cat=pulp.LpBinary)  
        add_player = pulp.LpVariable.dicts('Add', [player.player_id for player in players if player not in current_team], cat=pulp.LpBinary)   

        problem += pulp.lpSum(player.composite_score*add_player[player.player_id] for player in players if player not in current_team) - pulp.lpSum(player.composite_score*remove_player[player.player_id] for player in current_team)  
        problem += pulp.lpSum(add_player[player.player_id] for player in players if player not in current_team) == pulp.lpSum(remove_player[player.player_id] for player in current_team) 
        problem += pulp.lpSum(add_player[player.player_id] for player in players if player not in current_team) <= max_transfers 
        budget_change = pulp.lpSum(add_player[player.player_id]*player.cost for player in players if player not in current_team) - pulp.lpSum(remove_player[player.player_id]*player.cost for player in current_team) 
        problem += budget_change + budget >= 0 

        for position, value in self.position_constraints.items(): 
            current_in_position = sum(1 for player in current_team if player.position == position) 
            min_in_position, max_in_position = self.formation_constraints[position]  

            problem += pulp.lpSum(add_player[player.player_id] for player in players if player.position == position) - pulp.lpSum(remove_player[player.player_id] for player in current_team if player.position == position) + current_in_position >= min_in_position 
            problem += pulp.lpSum(add_player[player.player_id] for player in players if player.position == position) - pulp.lpSum(remove_player[player.player_id] for player in current_team if player.position == position) + current_in_position <= max_in_position 
        
        for team in range(1, 21): 
            current_in_team = sum(1 for player in current_team if player.team == team) 
            problem += pulp.lpSum(add_player[player.player_id] for player in players if player.team == team) - pulp.lpSum(remove_player[player.player_id] for player in current_team if player.team == team) + current_in_team <= self.team_max 

        problem.solve()  
        transfers = [player for player in players if pulp.value(add_player[player.player_id])==1] + [player for player in current_team if pulp.value(remove_player[player.player_id])==1] 
        budget_used = sum([player.cost for player in transfers if player not in current_team]) 
        return sorted(transfers, key=lambda x: x.position), budget_used 

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
        'ppg': 0.5, 
        'total_points': 0.4, 
        'ownership_percentage': 0.1
    } 
    team_weights = {} 

    @classmethod 
    def get_player_rating(cls, ppg, total_points, ownership_percentage): 
        return ppg*cls.players_weights['ppg'] + total_points*cls.players_weights['total_points'] + ownership_percentage*cls.players_weights['ownership_percentage'] 

    @classmethod 
    def get_team_rating(cls, team_information) -> float: 
        pass  
