from abc import abstractmethod
from math import inf
import copy
from algorithms import Stack, Prio_queue, Queue
from utils import Node

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
                current_node.explored = len(visited)
                return current_node
                # return self.problem.reverse_steps(current_node)
            
            for action in self.problem.actions(current_node.state):
                new_state, action_description, tile= self.problem.result(current_node.state, action)
                if tuple(map(tuple, new_state)) not in visited:
                    g_cost = current_node.gx + 1 if cost else 0
                    h_cost = self.problem.heuristic(new_state) if heuristic else 0
                    new_node = Node(state=new_state, goal_cost=g_cost, heuristic_cost=h_cost, parent=current_node, action=(tile,action_description))
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
                return current_node
            
            if current_node.depth <= limit:
                visited.add(tuple(map(tuple, current_node.state)))
                for action in self.problem.actions(current_node.state):
                    new_state = self.problem.result(current_node.state, action)
                    if tuple(map(tuple, new_state)) not in visited:
                        g_cost = current_node.gx + 1 if cost else 0
                        h_cost = self.problem.heuristic(new_state) if heuristic else 0
                        new_node = Node(new_state, g_cost, h_cost, current_node, current_node.depth+1)
                        if new_node not in frontier:
                            frontier.enqueue(new_node)
                            visited.add(tuple(map(tuple, new_state)))
                            
                        elif new_node in frontier:
                            idx = frontier.index(new_node)
                            if frontier[idx].fx > new_node.fx:
                                frontier[idx].fx == new_node.fx
                                
                            
                    
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

