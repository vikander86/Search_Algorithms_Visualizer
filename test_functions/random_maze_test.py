import numpy as np
import random
from itertools import permutations

def generate_random_maze(size=10, wall_prob=0.3):
    maze = np.random.choice([" ", "#"], size=(size, size), p=[1-wall_prob, wall_prob])
    positions = [[0,1],[1,1],[1,0]]
    count_s, count_g=0,0
    count_s = sum(1 for pos in positions if maze[pos[0]][pos[1]] == "#")
    count_g = sum(1 for pos in positions if maze[size-1-pos[0]][size-1-pos[1]] == "#")
    print(count_g, count_s)
    if count_s == 3 or count_g == 3:
        generate_random_maze()
    maze[0, 0] = "S"
    maze[size-1, size-1] = "G"
    return maze

# Example usage
maze = generate_random_maze()
print(maze)