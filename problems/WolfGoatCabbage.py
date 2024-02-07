from problems import Problem
import copy
from utils import Node

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
        direction = "Right" if start == left else "Left"
        actions.append(({"Farmer", None}, direction))           # add all actions including farmer goes alone
        for item in start:
            if item != "Farmer":
                actions.append(({"Farmer", item}, direction))
        return actions                        # return all possible actions
    
    def result(self, state, action):
        """
        Return the state that results from executing the given action in the given state.
        """
        new_state = copy.deepcopy(state)   # make deepcopy of current state
        left, right = new_state
        new_left = set(left)                # convert tuple to mutable set
        new_right = set(right)              # convert tuple to mutable set
        act, direction = action
        if "Farmer" in left:                # check which bank of the river the farmer is currently on
            new_left.remove("Farmer")       # move the farmer
            new_right.add("Farmer")
            for item in act:                 # now move the item specified in the action, which is not the farmer
                if item and item != "Farmer":
                    new_left.remove(item)   
                    new_right.add(item)           
        else:
            new_right.remove("Farmer")          # move the farmer
            new_left.add("Farmer")        
            for item in act:
                if item and item != "Farmer":   # now move the item specified in the action, which is not the farmer
                    new_right.remove(item)
                    new_left.add(item)
        new_left_F, new_right_F = sorted(tuple(new_left)), sorted(tuple(new_right))      # convert sets back to immutable tuples
        new_state = (new_left_F,new_right_F)
        if self.is_valid_state(new_state):                   # check if new state is valid
            return new_state, act, direction                             # return new state if valid else return current state
        else:
            return state, act, direction
    
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