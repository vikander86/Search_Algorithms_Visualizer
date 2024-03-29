from abc import abstractmethod
from math import inf
import copy
from algorithms import Stack, Prio_queue, Queue
from utils import Node
from problems import *

class Search_Algorithms:
    def __init__(self, problem):
        self.problem = problem
        self.count = 0

    def convert_state(self,state):
        x,y = state
        x,y = int(x),int(y)
        state = tuple((x,y))
        return state
    
    def create_new_node(self, state, action, parent,cost,heuristic):
        g_cost = parent.gx + 1 if cost else 0
        h_cost = self.problem.heuristic(state) if heuristic else 0
        return Node(state=state,goal_cost=g_cost,heuristic_cost=h_cost,parent=parent, action=action)
    
    def finalize_result(self, node, visited_order, frontier_order):
        node.explored = len(visited_order)
        node.visit_list = visited_order
        node.frontier_order = frontier_order
        return node
    
    def Search_algorithm(self, queue=Queue, heuristic=False, cost=False):
        frontier = queue()
        visited = set()
        visited_order = []
        frontier_order = []
        initial_state = self.problem.format_state(self.problem.initial_state.state)
        frontier.enqueue(self.problem.initial_state)
        visited.add(initial_state)
        
        while not frontier.is_empty():
            self.count += 1
            current_node = frontier.dequeue()
            state = self.problem.format_state(current_node.state)
            frontier_order.append(state)
            if self.problem.goal_test(current_node):
                return self.finalize_result(current_node,visited_order, frontier_order)
            
            for action in self.problem.actions(current_node.state):
                new_state, action_description, tile= self.problem.result(current_node.state, action)
                formatted_new_state = self.problem.format_state(new_state)
                if formatted_new_state not in visited:
                    new_node = self.create_new_node(new_state,(tile, action_description), current_node, cost, heuristic)
                    frontier.enqueue(new_node)
                    visited.add(formatted_new_state)
                    visited_order.append(formatted_new_state)
    
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
    
    def BFS(self):
        return self.Search_algorithm()       
        
    def DFS(self):
        return self.Search_algorithm(queue=Stack)

    def UFC(self):
        return self.Search_algorithm(queue=Prio_queue,heuristic=False, cost=True)

    def BeFE(self):
        return self.Search_algorithm(queue=Prio_queue,heuristic=True, cost=False)

    def Astar(self):
        return self.Search_algorithm(queue=Prio_queue,heuristic=True, cost=True)

