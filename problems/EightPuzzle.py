from problems import Problem
import copy
from utils import Node

class EightPuzzle(Problem):
    """
    Problem: Eight Puzzle

    Returns: List of states from initial to goal.
    """
    def __init__(self,initial_state, goal_state=Node([[1,2,3], [4,5,6], [7,8,0]],0,0, None)):
        super().__init__(Node(initial_state,0,0,None), goal_state)
        self.width = 3

    def __repr__(self):
        return "------Eight Puzzle problem------"

    def tile_location(self, tile):
        """
        Return indexes of tile in goal state
        """
        for i, row in enumerate(self.goal_state.state):
            if tile in row:
                return i, row.index(tile)
    
    def find_zero(self, state):
        """
        Return indexes of zero (empty tile)
        """
        for i, row in enumerate(state):
            for j, value in enumerate(row):
                if value == 0:
                    return i,j
    
    def is_valid_move(self, x , y):
        """ 
        Return true if action is valid 
        """
        width = 3
        return 0 <= x < width and 0 <= y < width

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        """
        possible_actions = [] # init empty set
        moves = {(1,0):"left",
                 (0,1):"up",
                 (-1,0):"right",
                 (0,-1):"down"}
        x,y = self.find_zero(state)
        
        for move, action in moves.items():
            dy,dx = move
            new_x, new_y = x+dx, y+dy
            if self.is_valid_move(new_x,new_y):
                possible_actions.append((new_x,new_y, action))
                
        return possible_actions
    
    def result(self, state, action):
        """
        Return the state that results from executing the given action in the given state.
        """
        x, y, action_description = action 
        zero_x, zero_y = self.find_zero(state)
        new_state = copy.deepcopy(state)
        tile = new_state[x][y] 
        new_state[zero_x][zero_y], new_state[x][y] = new_state[x][y], new_state[zero_x][zero_y]
        return new_state, action_description, tile
    
    def heuristic(self, state):
        """ 
        Heuristic value is calculated by measuring how far each tile is from goal state using ManhattenDistance
        """
        heuristic_cost = 0
        for i in range(len(state)):
            for j in range(len(state)):
                if state[i][j] != 0:
                    x,y = self.tile_location(state[i][j])
                    heuristic_cost += abs(i - x) + abs(j - y)       
        return heuristic_cost 