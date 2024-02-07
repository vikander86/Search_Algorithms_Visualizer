


class Node:
    """Initialize a new instance of the Node Class
    
    args:
        state(any) : The state represented by a node
        
    
    
    """
    def __init__(self,state,goal_cost=0,heuristic_cost=0, parent=None, depth=0, explored=0,action=list()):
        self.state = state
        self.gx = goal_cost
        self.hx = heuristic_cost
        self.parent = parent
        self.depth = depth
        self.explored = explored
        self.action = action
        
    def __repr__(self):
        return f"{self.state}, Goal:{self.gx}, Heuristic:{self.hx}, Parent:{self.parent}"
    
    def __lt__(self, other):
        return self.fx() < other.fx()
    
    def fx(self): #return fx = PATH_COST + HEURISTIC_COST
        return self.gx + self.hx