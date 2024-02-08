# controller.py

from gui import GUI
from problems import WolfGoatCabbage, EightPuzzle
from algorithms import search

class AppController: 
    def __init__(self):
        self.view = GUI(self)
        self.algorithm = None
        self.problem = None
        self.game_on = False
        self.view.create_main_frames()
        self.view.create_dropbox()
        self.view.create_buttons()
    
    def run(self):
        self.view.mainloop()    
        
        
    
    

    def set_algorithm(self, algorithm):
        if algorithm == "Breadth First Search": self.algorithm = "BFS"
        if algorithm == "Depth First Search": self.algorithm = "DFS"
        if algorithm == "Uniform Cost Search": self.algorithm = "UFC"
        if algorithm == "Best First Search": self.algorithm = "BeFS"
        if algorithm == "A* Search": self.algorithm = "Astar"
        print(self.algorithm)
        
        
    def on_wcg_selected(self):
        pass
    def on_eightpuzzle_selected(self):
        pass
    def on_maze_selected(self):
        pass
    def on_eightqueens_selected(self):
        pass
        
    def exit(self):
        self.view.destroy()
    
    def reset(self):
        print("test")