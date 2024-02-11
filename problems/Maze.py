from problems import Problem
from utils import Node
import numpy as np
import copy

from abc import abstractmethod

class Maze(Problem):
    """
    Problem: Maze

    Returns: List of states from initial to goal.
    """
    def __init__(self,initial_state=Node(tuple(["0","0"])), goal_state=Node(tuple(["9","13"])),size_x=10, size_y=14):
        super().__init__(initial_state,goal_state)
        self.maze = []
        self.size_x = size_x
        self.size_y = size_y
    def __repr__(self):
        return "Maze problem"

    def tile_location(self, tile):
        """
        Return indexes of tile in goal state
        """
        for i, row in enumerate(self.goal_state.state):
            if tile in row:
                return i, row.index(tile)
    
    def find_current_tile(self, state):
        """
        Return indexes of zero (empty tile)
        """
        for i, row in enumerate(state):
            for j, value in enumerate(row):
                if value == 'P':
                    return i,j
    
    def is_valid_move(self, x , y):
        """ 
        Return true if action is valid 
        """
        if 0 <= x < self.size_x and 0 <= y < self.size_y:
            if self.maze[x][y] != "#":
                return True
        return False

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        """
        possible_actions = [] # init empty set
        moves = {(1,0):"right",
                 (0,1):"down",
                 (-1,0):"left",
                 (0,-1):"up"}
        
        x,y = state
        x,y = int(x), int(y)
        for move, action in moves.items():
            dx,dy = move
            new_x, new_y = x+dx, y+dy
            
            if self.is_valid_move(new_x,new_y):
                possible_actions.append((new_x,new_y, action))
                
        return possible_actions
    
    def result(self, state, action):
        """
        Return the state that results from executing the given action in the given state.
        """
        x, y, action_description = action 
        new_state = copy.deepcopy(state)
        tile = x,y
        self.maze[x][y] = "E"
        
        x, y = str(x),str(y)
        new_state = tuple([x,y])
        return new_state, action_description, tile
    
    def heuristic(self, state):
        """ 
        Heuristic value is calculated by measuring how far each tile is from goal state using ManhattenDistance
        """
        heuristic_cost = 0
        x,y = state
        x,y = int(x),int(y)
        heuristic_cost += abs(9 - x) + abs(13 - y)       
        return heuristic_cost
    
    def format_state(self, state):
        return tuple(map(int, state))