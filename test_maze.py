from problems import Maze
from utils import generate_random_maze
from algorithms import Search_Algorithms

test = Maze()

test.maze = generate_random_maze()
print(test.maze)
solver = Search_Algorithms(test)
result = solver.BeFE()

solution = test.reverse_steps(result)
actions = test.reverse_actions(result)
print(result.visit_list)
for x,y in solution:
    test.maze[int(x)][int(y)] = "V"
    
print(test.maze)
