import numpy as np

def generate_random_maze(size=14, wall_prob=0.5):
    maze = np.random.choice([" ", "#"], size=(10, size), p=[1-wall_prob, wall_prob])
    positions = [[0,1],[1,1],[1,0]]
    count_s, count_g=0,0
    count_s = sum(1 for pos in positions if maze[pos[0]][pos[1]] == "#")
    count_g = sum(1 for pos in positions if maze[10-1-pos[0]][size-1-pos[1]] == "#")
    if count_s == 3 or count_g == 3:
        generate_random_maze()
    maze[0, 0] = "S"
    maze[10-1, size-1] = "G"
    return maze
