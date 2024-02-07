from heapq import heappop, heappush

class Stack:
    def __init__(self):
        self.stack = []
        
    def enqueue(self, node):
        self.stack.append(node)
    
    def dequeue(self):
        if self.is_empty():
            return None
        return self.stack.pop()
    
    def is_empty(self):
        return len(self.stack) == 0

class Queue:
    def __init__(self):
        self.queue = []
        
    def enqueue(self, node):
        self.queue.append(node)
    
    def dequeue(self):
        if self.is_empty():
            return None
        return self.queue.pop(0)
    
    def is_empty(self):
        return len(self.queue) == 0
    
class Prio_queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, node):
        heappush(self.queue, (node.fx(), node))
            
    def dequeue(self):
        return heappop(self.queue)[1]
    
    def is_empty(self):
        return len(self.queue) == 0
    
    def printqueue(self):
        for item in self.queue:
            print(item.state.fx())