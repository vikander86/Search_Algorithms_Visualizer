from abc import abstractmethod
from math import inf
import copy
from python_files.containers import Stack, Prio_queue, Queue

# node class, that holds information about the state, its  
class Node:
    def __init__(self,state,goal_cost=0,heuristic_cost=0, parent=None, depth=0):
        self.state = state
        self.gx = goal_cost
        self.hx = heuristic_cost
        self.parent = parent
        self.depth = depth
        
    def __repr__(self):
        return f"{self.state}, Goal:{self.gx}, Heuristic:{self.hx}, Parent:{self.parent}"
    
    def __lt__(self, other):
        return self.fx() < other.fx()
    
    def fx(self): #return f(x) = g(x) + h(x)
        return self.gx + self.hx


"""
PROBLEMS
"""

class Problem:
    def __init__(self,initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state

    @abstractmethod
    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        """
        pass

    @abstractmethod
    def result(self, state, action):
        """
        Return the state that results from executing the given action in the given state.
        """
        pass

    @abstractmethod
    def heuristic(self, state):
        """
        Return the heuristic value for a given state.
        """
        pass
    
    def goal_test(self, node):
        """
        Return True if the state is a goal state.
        """
        return node.state == self.goal_state.state

    def reverse_steps(self, final_state):
        """ 
        Return list with path from initial state to goal state
        """
        path = []
        while final_state:
            path.append(final_state.state)
            final_state = final_state.parent
        path.reverse()
        return path



class WolfGoatCabbage(Problem):
    """ The problem of a farmer, trying to cross a river with his wolf, goat and cabbage
    with the use of a row boat that only fits the farmer and 1 item. If the wolf is ever left
    alone with the goat, it will eat it. If the goat is left with the cabbage, it will eat it.
    
    The problem is seperated in two sets, left and right, to illustrate the left and right bank of the river.
    """
    def __init__(self, initial_state, goal_state=Node((sorted(tuple()),sorted(tuple({"Cabbage", "Farmer","Goat","Wolf"}))))):
        super().__init__(Node(initial_state), goal_state)
    
    def __repr__(self):
        return "------Wolf Goat Cabbage problem------"
    
    def is_valid_state(self, state):
        """ 
        Check if state is valid. Goat and cabbage cannot be left alone, aswell as wolf
        and goat cannot be left alone
        """
        left, right = state                                 # devide state into left bank and right bank of the river
        if len(left) == 2:                                  # check if only 2 items left on either side. Return false if restrictions are met
            if ('Goat' in left and 'Cabbage' in left) or ('Goat' in right and 'Cabbage' in right):
                return False
            if ('Wolf' in left and 'Goat' in left) or ('Wolf' in right and 'Goat' in right):
                return False
        return True                                         # else return True
    
    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        """
        actions = []                               # init empty list of actions
        left, right = state                                 # devide state into left bank and right bank of the river
        if "Farmer" in left:                                # check which side the farmer is on
            start = left
        else:
            start = right
        actions.append({"Farmer", None})           # add all actions including farmer goes alone
        for item in start:
            if item != "Farmer":
                actions.append({"Farmer",item})
        return actions                             # return all possible actions
    
    def result(self, state, action):
        """
        Return the state that results from executing the given action in the given state.
        """
        left,right = copy.deepcopy(state)   # make deepcopy of current state
        new_left = set(left)                # convert tuple to mutable set
        new_right = set(right)              # convert tuple to mutable set
        if "Farmer" in left:                # check which bank of the river the farmer is currently on
            new_left.remove("Farmer")       # move the farmer
            new_right.add("Farmer")
            for item in action:                 # now move the item specified in the action, which is not the farmer
                if item and item != "Farmer":
                    new_left.remove(item)   
                    new_right.add(item)           
        else:
            new_right.remove("Farmer")          # move the farmer
            new_left.add("Farmer")        
            for item in action:
                if item and item != "Farmer":   # now move the item specified in the action, which is not the farmer
                    new_right.remove(item)
                    new_left.add(item)
        new_left_F, new_right_F = sorted(tuple(new_left)), sorted(tuple(new_right))         # convert sets back to immutable tuples
        if self.is_valid_state((new_left_F,new_right_F)):                   # check if new state is valid
            return new_left_F,new_right_F                                   # return new state if valid else return current state
        else:
            return state
    
    def display_state(self, state):
        """ 
        Super fancy display function to see the steps taken, woah woah whaaat?
        Hit me up blizz
        """
        left, right = state
        items = ["Farmer", "Wolf", "Goat", "Cabbage"]
        for item in items:
            if item in left:
                print(f"{item:10} ------- __________")
            else:
                print(f"__________ ------- {item:10}")

    def heuristic(self, state):
        """ 
        Heuristic value is calculated by counting how many items still remains on the left bank of the river. 
        """
        left, right = state
        return len(left)
    
    def goal_test(self, node):
        """
        Return True if the state is a goal state.
        """
        left, right = node.state
        g_left, g_right = self.goal_state.state
        return right == g_right
    



class EightProblem(Problem):
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
        moves = ((1,0),(0,1),(-1,0),(0,-1))
        x,y = self.find_zero(state)
        
        for dx,dy in moves:
            new_x, new_y = x+dx, y+dy
            if self.is_valid_move(new_x,new_y):
                possible_actions.append((new_x,new_y))
                
        return possible_actions
    
    def result(self, state, action):
        """
        Return the state that results from executing the given action in the given state.
        """
        x, y = self.find_zero(state)
        new_state = copy.deepcopy(state)
        new_x, new_y = action
        new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
        return new_state
    
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
        


class Search_Algorithms:
    def __init__(self, problem):
        self.problem = problem
        self.count = 0

    def Search_algorithm(self, queue=Queue, heuristic=False, cost=False):
        frontier = queue()
        visited = set()
        frontier.enqueue(self.problem.initial_state)
        while not frontier.is_empty():
            self.count += 1
            current_node = frontier.dequeue()
            visited.add(tuple(map(tuple, current_node.state)))
            
            if self.problem.goal_test(current_node):
                return self.problem.reverse_steps(current_node)
            
            for action in self.problem.actions(current_node.state):
                new_state = self.problem.result(current_node.state, action)
                if tuple(map(tuple, new_state)) not in visited:
                    g_cost = current_node.gx + 1 if cost else 0
                    h_cost = self.problem.heuristic(new_state) if heuristic else 0
                    new_node = Node(new_state, g_cost, h_cost, current_node)
                    frontier.enqueue(new_node)
                    visited.add(tuple(map(tuple, new_state)))
    
    def Iterative_DDFS(self,heuristic=False, cost=False, limit=0):
        frontier = Stack()
        visited = set()
        frontier.enqueue(self.problem.initial_state)
        while not frontier.is_empty():
            self.count += 1
            current_node = frontier.dequeue()
            
            if self.problem.goal_test(current_node):
                return self.problem.reverse_steps(current_node)
            
            if current_node.depth <= limit:
                visited.add(tuple(map(tuple, current_node.state)))
                for action in self.problem.actions(current_node.state):
                    new_state = self.problem.result(current_node.state, action)
                    if tuple(map(tuple, new_state)) not in visited:
                        g_cost = current_node.gx + 1 if cost else 0
                        h_cost = self.problem.heuristic(new_state) if heuristic else 0
                        new_node = Node(new_state, g_cost, h_cost, current_node, current_node.depth+1)
                        frontier.enqueue(new_node)
                        visited.add(tuple(map(tuple, new_state)))
                    
    def IDDFS(self):
        solution = None
        limit = 0
        while solution is None:
            self.count = 0
            solution = self.Iterative_DDFS(limit=limit)
            limit += 1
        return solution
    
    def BFS_algorithm(self):
        return self.Search_algorithm()       
        
    def DFS_algorithm(self):
        return self.Search_algorithm(queue=Stack)

    def UFC_algorithm(self):
        return self.Search_algorithm(queue=Prio_queue,heuristic=False, cost=True)

    def BeFE_algorithm(self):
        return self.Search_algorithm(queue=Prio_queue,heuristic=True, cost=False)

    def Astar_search_algorithm(self):
        return self.Search_algorithm(queue=Prio_queue,heuristic=True, cost=True)
      

    
# def print_test(problems, algorithms):
#     for problem in problems:
#         print(f"{problem}")
#         for algorithm in algorithms:
#             solver = Search_Algorithms(problem)
#             algo_function = getattr(solver, algorithm)
#             solution = algo_function()
#             print(f"{algorithm} takes {len(solution)} steps")
#             print(f"Number of states the AI evaluated: {solver.count}")
            
            

# problems = [EightProblem([[3,7,5], [8,1,2], [0,4,6]]),
#             WolfGoatCabbage((sorted(tuple({"Cabbage", "Farmer","Goat","Wolf"})),tuple()))]

# solvers = ["Astar_search_algorithm",
#            "BFS_algorithm",
#         #    "DFS_algorithm",
#            "UFC_algorithm",
#            "BeFE_algorithm",
#            "IDDFS"]

# print_test(problems, solvers)

# problem = WolfGoatCabbage((sorted(tuple({"Cabbage", "Farmer","Goat","Wolf"})),tuple()))
# solver = Search_Algorithms(problem)
# solution = solver.Astar_search_algorithm()
# print(f"{len(solution)} steps")
# print(f"Number of states the AI evaluated: {solver.count}")

# problem = EightProblem(test_state_8)
# solver = Depth_First_Search(problem)
# solution = solver.DFS_algorithm()
# for step in solution:
#     for row in step:
#         print(row)
#     print()




# problem1 = WolfGoatCabbage((tuple({"Farmer", "Wolf","Goat","Cabbage"}),tuple()))
# solver1 = Astar_search(problem1)
# solution1 = solver1.Astar_search_algorithm()
# for step in solution1:
#     for row in step:
#         print(row)
#     print()
# print(f"Best solution takes {len(solution1)} steps")
# tests run
# search = Astar_search(goal_state_8, test_state_8)
# solution = search.Astar_search_algorithm()


