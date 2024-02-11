from abc import abstractmethod

class Problem:
    def __init__(self,initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state
    
    @abstractmethod
    def __repr__(self):
        pass

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
    
    def reverse_actions(self, final_state):
        """ 
        Return list with actions from initial state to goal state
        """
        actions = []
        while final_state:
            actions.append(final_state.action)
            final_state = final_state.parent
        actions.reverse()
        return actions
    
    def format_state(self, state):
        return tuple(map(tuple, state))