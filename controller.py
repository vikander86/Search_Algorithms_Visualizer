# controller.py

from gui import GUI
from problems import WolfGoatCabbage, EightPuzzle
from algorithms import Search_Algorithms

class AppController: 
    def __init__(self):
        self.view = GUI(self)
        self.algorithm = None
        self.problem = None
        self.game_on = False
        self.moveable_objects = None
        
    def init_start_up(self):    
        self.view.create_main_frames()
        self.view.create_dropbox()
        self.view.create_buttons()
    
    def run(self):
        self.view.mainloop()    

    def set_algorithm(self, algorithm):
        if algorithm == "Breadth First Search": self.algorithm = Search_Algorithms.BFS
        if algorithm == "Depth First Search": self.algorithm = Search_Algorithms.DFS
        if algorithm == "Uniform Cost Search": self.algorithm = Search_Algorithms.UFC
        if algorithm == "Best First Search": self.algorithm = Search_Algorithms.BeFE
        if algorithm == "A* Search": self.algorithm = Search_Algorithms.Astar
        
    def on_wcg_selected(self):
        self.problem = WolfGoatCabbage
        self.view.description(self.problem)
        frames = ["initial_frame","solution_frame","goal_frame"]
        self.view.init_states()
        self.view.init_frames_wsg(frames)
        self.view.description(self.problem)
    
    def solve_problem(self):
        if self.problem == WolfGoatCabbage:
            self.solve_wolfgoatcabbage()
    
    
    def move_characters_wsg(self,state, direction, x):
        if direction == "Left":
            if x > 0.25:
                x -= 0.005
                state.place(relx=x)
                self.after(5, lambda: self.move_characters(state,direction,x))
        else:
            if x < 0.75:
                x += 0.005
                state.place(relx=x)
                self.after(5, lambda: self.move_characters(state,direction,x))

    def solve_wolfgoatcabbage(self):
        self.text_size = 10
        self.game_on = True
        
        problem = self.proble()
        solver = Search_Algorithms(problem)
        result = self.algorithm(solver)
        
        solution = self.algorithm(solver).reverse_steps(result)                # Return a list with initial state to goal state
        actions = self.algorithm(solver).reverse_actions(result)               # Return a list with actions based on the empty tile
        actions.append(("", {None,"Finished"}))

        self.after(1000, lambda: self.update_state_wgc(solution, actions))
    
    def update_state_wgc(self, solution, actions, step_index=0):
        if step_index >=len(solution) or self.game_on == False:
            return
        
        time = 1500
        action = actions[step_index+1] # init action to current state
        self.game_on = True

        direction, act  = action
        for i in range(len(self.moveable_objects)):
            if "Farmer" in act and i == 0:
                if direction == "Left":
                    self.move_characters(self.moveable_objects[i], "Left", 0.85)
                else:
                    self.move_characters(self.moveable_objects[i], "Right", 0.15)
            if "Wolf" in act and i == 1:
                if direction == "Left":
                    self.move_characters(self.moveable_objects[i], "Left", 0.85)
                else:
                    self.move_characters(self.moveable_objects[i], "Right", 0.15)       
            if "Goat" in act and i == 2:
                if direction == "Left":
                    self.move_characters(self.moveable_objects[i], "Left", 0.85)
                else:
                    self.move_characters(self.moveable_objects[i], "Right", 0.15)         
            if "Cabbage" in act and i == 3:
                if direction == "Left":
                    self.move_characters(self.moveable_objects[i], "Left", 0.85)
                else:
                    self.move_characters(self.moveable_objects[i], "Right", 0.15)
            left,right=act
            self.x_right = 0.15
            self.x_left = 0.85
            if None in act:
                not_none = left if left != None else right
                self.solution_action.configure(text=f"{not_none}\n"
                                                    f"{direction}")
            else:
                self.solution_action.configure(text=f"{left} & {right}\n"
                                                    f"{direction}")
        self.expand(action,10,30)
        self.text_size = 10
        self.progress += 1 / len(solution) # Calculate progress bar increment
        self.solution_progress.set(self.progress) # Update progress bar
        self.after(time, lambda: self.update_state_wgc(solution,actions, step_index + 1))
        
    def on_eightpuzzle_selected(self):
        self.problem = EightPuzzle
        pass
    def on_maze_selected(self):
        pass
    def on_eightqueens_selected(self):
        pass
        

    
    def reset(self):
        if self.problem == WolfGoatCabbage:
            self.view.create_board_wsg("solution_frame", self.view.solution_frame)
        self.game_on = False
        
    def exit(self):
        self.view.destroy()