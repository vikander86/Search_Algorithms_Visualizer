from tkinter import *
from customtkinter import *
from algorithms import *
from problems import *
from PIL import Image
from itertools import permutations
import threading
import os


"""
init states for Eight Puzzle
"""
goal_state = [[1,2,3],
              [4,5,6],
              [7,8,""]]

class GUI(CTk):
    def __init__(self, *args, **kwargs):
        
        """
        Initializing window
        """
        super().__init__(*args, **kwargs, )
        self.geometry("1000x800")
        self.title("Search Algorithms Visualizer")
        
        self.grid_columnconfigure((0,1,2,3,4), weight=1, uniform="a")
        self.grid_rowconfigure(0,weight=1, uniform="a")
        self.grid_rowconfigure(4,weight=1, uniform="a")
        self.grid_rowconfigure((1,2,3),weight=4, uniform="a")
        
        """
        Frame work for window
        """
        top_frame = CTkFrame(self,corner_radius=0)
        top_frame.grid(row = 0, column=0, columnspan=5, sticky="nsew")
        top_frame.grid_columnconfigure((0,1,2,3,4), weight=1, uniform="a")
        top_frame.grid_rowconfigure(0,weight=1, uniform="a")
        
        left_frame = CTkFrame(self, corner_radius=50)
        left_frame.grid(row=1, column=0, rowspan=4, padx=5, pady=5, sticky="nsew")
        left_frame.grid_rowconfigure((0,1,2,3,4), weight=1, uniform="a")
        left_frame.grid_columnconfigure(0, weight=1, uniform="a")
        
        result_frame = CTkFrame(self,corner_radius=50)
        result_frame.grid(row = 4, column=1, columnspan=4, padx= 5, pady=(5,5), sticky="nswe")
        result_frame.grid_rowconfigure(0, weight=1, uniform="a")
        result_frame.grid_columnconfigure((0,1,2,3), weight=3, uniform="a")
        
        display_frame = CTkFrame(self, corner_radius=5, fg_color="transparent")
        display_frame.grid(row = 1, column=1, rowspan=3, columnspan=4, padx=5, pady=5, sticky="nswe")
        display_frame.grid_rowconfigure(0, weight = 1, uniform="a")
        display_frame.grid_rowconfigure((1,2), weight = 2, uniform="a")
        display_frame.grid_columnconfigure((0,1), weight = 1, uniform="a")
        
        """"
        DISPLAY FRAME: Displaying results and ... stuff?
        """
        # initialize a banner frame
        banner_frame = CTkFrame(display_frame)
        banner_frame.grid(row=0,column=0,columnspan=2,sticky="nswe")
        banner_frame.grid_rowconfigure(0, weight=1, uniform="a")
        banner_frame.grid_columnconfigure(0, weight=1, uniform="a")
        
        # Descriptive text about current problem
        self.banner = CTkLabel(banner_frame, text="Hey there!\nChoose a problem.", font=("Consolas", 14))
        self.banner.grid(row=0, column=0, padx=5, sticky="we")
        
        # initialize "initial state" frame
        self.initial_frame = CTkFrame(display_frame)
        self.initial_frame.grid(row=1, column=0, sticky="nswe")
        self.initial_frame.grid_rowconfigure(0, weight=1, uniform="a")
        self.initial_frame.grid_rowconfigure(1, weight=6, uniform="a")
        self.initial_frame.grid_columnconfigure(0, weight=1, uniform="a")

        
        # initialize "goal state" frame
        self.goal_frame = CTkFrame(display_frame)
        self.goal_frame.grid(row=2, column=0, sticky="nswe")
        self.goal_frame.grid_rowconfigure(0, weight=1, uniform="a")
        self.goal_frame.grid_rowconfigure(1, weight=6, uniform="a")
        self.goal_frame.grid_columnconfigure(0, weight=1, uniform="a")
        
        # initialize solution frame
        self.solution_frame = CTkFrame(display_frame)
        self.solution_frame.grid(row=1, rowspan=2, column=1, sticky="nswe")
        self.solution_frame.grid_rowconfigure(0, weight=1, uniform="a")
        self.solution_frame.grid_rowconfigure(1, weight=4, uniform="a")
        self.solution_frame.grid_rowconfigure(2, weight=1, uniform="a")
        self.solution_frame.grid_rowconfigure(3, weight=1, uniform="a")
        self.solution_frame.grid_columnconfigure(0, weight=1, uniform="a")
        
        self.solution_representation = []
        
        
        """
        LEFT FRAME: Radio buttons
        """
        
        # Variable to store radio button press
        self.selected_algorithm = StringVar(value="BFS_algorithm")
        
        # Buttons for each of the algorithms included
        self.radio_button_BFS = CTkRadioButton(left_frame,variable=self.selected_algorithm, value="BFS_algorithm", text="Breadth First Search",font=("Consolas", 12))
        self.radio_button_DFS = CTkRadioButton(left_frame,variable=self.selected_algorithm, value="DFS_algorithm", text="Depth First Search",font=("Consolas", 12))
        self.radio_button_UFC = CTkRadioButton(left_frame,variable=self.selected_algorithm, value="UFC_algorithm", text="Uniform Cost Search",font=("Consolas", 12))
        self.radio_button_BeFS = CTkRadioButton(left_frame,variable=self.selected_algorithm, value="BeFE_algorithm", text="Best First Search",font=("Consolas", 12))
        self.radio_button_astar = CTkRadioButton(left_frame, variable=self.selected_algorithm, value="Astar_search_algorithm", text="A* Search",font=("Consolas", 12))
        self.radio_button_BFS.grid(row=0, column=0, padx=10, sticky="w")
        self.radio_button_DFS.grid(row=1, column=0, padx=10, sticky="w")
        self.radio_button_UFC.grid(row=2, column=0, padx=10, sticky="w")
        self.radio_button_BeFS.grid(row=3, column=0, padx=10, sticky="w")
        self.radio_button_astar.grid(row=4, column=0, padx=10, sticky="w")
        
        """
        TOP FRAME: Fun with buttons
        """
        # Buttons for problems - Wolf, Goat and cabbage - Eight Puzzle - Maze
        
        button1 = CTkButton(top_frame, text="Wolf, Goat and Cabbage",  command=self.init_wolfgoatcabbage, corner_radius=10)
        button1.grid(row=0, column=0,sticky="nswe", padx= 10, pady=10)
        
        button2 = CTkButton(top_frame, text="Eight Puzzle",  command=self.init_EightPuzzle, corner_radius=10)
        button2.grid(row=0, column=1,sticky="nswe", padx= 10, pady=10)
        
        button3 = CTkButton(top_frame, text="Maze",  command=self.button_exit, corner_radius=10)
        button3.grid(row=0, column=2,sticky="nswe", padx= 10, pady=10)
        
        button4 = CTkButton(top_frame, text="Exit",   command=self.button_exit, corner_radius=10)
        button4.grid(row=0, column=4,sticky="nswe", padx= 10, pady=10)

        """
        RESULT FRAME: solve button and various information about the search
        """
        self.solve_button = CTkButton(result_frame, text="SOLVE", width=100, height=50, corner_radius=50)
        self.solve_button.grid(row=0, column=0, padx=(5,2.5), pady=10)
        
        self.reset_button = CTkButton(result_frame, text="RESET", width=100, height=50, corner_radius=50)
        self.reset_button.grid(row=0, column=1, padx=(2.5,2.5), pady=10, sticky="w")
        
        self.result_of_solution = CTkLabel(result_frame, text="")
        self.result_of_solution.grid(row=0, column=2, columnspan=2, padx=(2.5,2.5), pady=5)
        
        self.stop_search = False
        self.game_on = False
        
        self.numbers_left = [0,1,2,3,4,5,6,7,8]
        self.numbers_entered = []
    """
    INITIAL STATE, GOAL STATE, SOLUTION
    """
    def init_states(self):  
        self.initial_state_text = CTkLabel(self.initial_frame, text="Initial State", fg_color="transparent", font=("Consolas", 14))
        self.initial_state_text.grid(row=0, column=0, sticky="nwe", padx=5, pady=5)
        
        self.goal_state_text = CTkLabel(self.goal_frame, text="Goal State", fg_color="transparent", font=("Consolas", 14))
        self.goal_state_text.grid(row=0, column=0, sticky="nwe", padx=5, pady=5)
        
        self.solution_banner = CTkLabel(self.solution_frame, text="Solution", fg_color="transparent", font=("Consolas", 14))
        self.solution_banner.grid(row=0, column=0, padx=5,pady=5, sticky="nwe")
        
        self.solution_action = CTkLabel(self.solution_frame, text="", fg_color="transparent", font=("Consolas", 20), height=80)
        self.solution_action.grid(row=2, column=0, padx=5,pady=2.5, sticky="nwe")
        
        self.solution_progress = CTkProgressBar(self.solution_frame, orientation="horizontal", height=20, width=300)
        self.solution_progress.set(0)
        
    """
    
    HELPER FUNCTIONS FOR UI
    
    """    
    # Destroy error window
    def error_window_destroy(self):
        self.error.destroy()
        self.reset_eight_puzzle()
           
    # Return center point of main window adjusting to where it currently is
    def error_popup_loc(self):
        main_window_width = self.winfo_width()
        main_window_height = self.winfo_height()
        main_window_x = self.winfo_x()
        main_window_y = self.winfo_y()

        error_width = 200
        error_height = 100

        center_x = main_window_x + (main_window_width - error_width) // 2
        center_y = main_window_y + (main_window_height - error_height) // 2
        return center_x, center_y
    
    # Exit, destroy main window
    def button_exit(self):
        self.destroy()
        exit()
        
    def reset_frames(self):
        for widget in self.initial_frame.winfo_children():
            widget.destroy()
        for widget in self.goal_frame.winfo_children():
            widget.destroy()
        for widget in self.solution_frame.winfo_children():
            widget.destroy()
        self.init_states()

    """
    
    
    WOLF GOAT AND CABBAGE PROBLEM
    
    
    """
    # Init WGC Problem
    def init_wolfgoatcabbage(self):
        self.init_states()
        self.solution_action.configure(font=(None, 20), text="Press Solve")
        
        self.after(10, lambda: self.WolfGoatCabbage_gui())
        
        self.x_left = 0.85
        self.x_right = 0.15
    
    def solve_wolfgoatcabbage(self):
        self.progress = 0
        self.text_size = 10
        self.stop_search = False
        self.solution_action.configure(font=(None, 20), text="Press Solve")
        
        self.solution_progress.set(self.progress)
        self.solution_progress.grid(row=3, column=0, padx=5, pady=2.5)
        
        problem = WolfGoatCabbage((sorted(tuple({"Cabbage", "Farmer","Goat","Wolf"})),sorted(tuple())))
        solver = Search_Algorithms(problem)
        get_algorithm = self.selected_algorithm.get()           # Get the StringVar from the radiobuttons. 
        assign_algorithm = getattr(solver, get_algorithm, None) # Match the StringVar with the algorithm method in ./Python_files/Algorithms.py
        result = assign_algorithm()                             # Return result (final node)
        solution = problem.reverse_steps(result)                # Return a list with initial state to goal state
        actions = problem.reverse_actions(result)               # Return a list with actions based on the empty tile
        actions.append(("", {None,"Finished"}))

        self.after(1000, lambda: self.update_state_wgc(solution, actions))
        self.after(0, lambda: self.result_of_solution.configure(text=f"Path Length: {len(solution)}    Nodes Explored: {result.explored}"))
        self.after(0, lambda: self.solution_banner.configure(text=f"Solution\n\n{get_algorithm}"))
        
    def move_characters(self,state, direction, x):
        if direction == "Left":
            if x > 0.15:
                x -= 0.005
                state.place(relx=x)
                self.after(5, lambda: self.move_characters(state,direction,x))
        else:
            if x < 0.85:
                x += 0.005
                state.place(relx=x)
                self.after(5, lambda: self.move_characters(state,direction,x))
   
    def update_state_wgc(self, solution, actions, step_index=0):
        if step_index >=len(solution) or self.stop_search == True:
            return
        
        time = 1500
        step = solution[step_index] # init current state   
        action = actions[step_index+1] # init action to current state

        direction, act  = action
        for i in range(len(self.solution_representation)):
            if "Farmer" in act and i == 0:
                if direction == "Left":
                    self.move_characters(self.solution_representation[i], "Left", 0.85)
                else:
                    self.move_characters(self.solution_representation[i], "Right", 0.15)
            if "Wolf" in act and i == 1:
                if direction == "Left":
                    self.move_characters(self.solution_representation[i], "Left", 0.85)
                else:
                    self.move_characters(self.solution_representation[i], "Right", 0.15)       
            if "Goat" in act and i == 2:
                if direction == "Left":
                    self.move_characters(self.solution_representation[i], "Left", 0.85)
                else:
                    self.move_characters(self.solution_representation[i], "Right", 0.15)         
            if "Cabbage" in act and i == 3:
                if direction == "Left":
                    self.move_characters(self.solution_representation[i], "Left", 0.85)
                else:
                    self.move_characters(self.solution_representation[i], "Right", 0.15)
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
    
    def reset_wcg_puzzle(self):
        pass   
        
    """
    SETTING UP THE WOLF, GOAT and CABBAGE UI
    """
    def WolfGoatCabbage_gui(self):
        """
        Initialize buttons - solve and reset
        """
        if self.game_on == True:
            self.reset_frames()
        self.game_on = True
        self.reset_button.configure(command=self.reset_wcg_puzzle)
        self.solve_button.configure(command=self.solve_wolfgoatcabbage)
        
        """
        Banner change
        """
        self.banner.configure(text=("The Wolf, Goat, and Cabbage problem is a classic river crossing puzzle\n"
                                    "where a farmer must transport a wolf, a goat, and a cabbage across a river using a boat\n"
                                    "that can only carry the farmer and one of the three items at a time.\n"
                                    "The challenge is to devise a strategy that prevents the goat from eating the cabbage\n"
                                    "and the wolf from eating the goat when the farmer is not present."))
        
        """
        FRAME instantiation
        
        Return a frame with specific configurations for the Eight Puzzle
        """
        def frame_builder(parent_frame,image_size=(150,220), placement=0.5):
            river_bg = CTkImage(light_image=Image.open(bg_wcg_image_path), size=image_size)
            frame = CTkFrame(parent_frame,height = 200, width=275,border_width=0, fg_color="transparent")
            frame.place(relx=0.5, rely=placement, anchor="center")
            
            background_label = CTkLabel(frame, image=river_bg, text="")
            background_label.place(relx=0.5, rely=0.5, anchor="center")
            return frame
        
        """
        Building the frames
        """
        self.initial_frame_puzzle = frame_builder(self.initial_frame)
        self.goal_frame_puzzle = frame_builder(self.goal_frame)
        self.solution_frame_output = frame_builder(self.solution_frame, (140,250),0.4)
        """
        WIDGET instantiation
        
        Returns list with widgets for Eight Puzzle board - input, goal and solution.
        """
        def create_board(type="", label_width=60, label_height=20, font_size=14):
            widget_list =[]
            character = ["Farmer","Wolf","Goat","Cabbage"]
            y_loc = 0.1
            for i in range(4):
                if type == "initial":
                    new_widget = CTkLabel(self.initial_frame_puzzle, width=label_width, height=label_height, 
                                          text=character[i], fg_color="black", corner_radius=10)
                    new_widget.place(relx=0.15, rely=y_loc,anchor=CENTER)
                if type == "goal_labels":
                    new_widget = CTkLabel(self.goal_frame_puzzle, width=label_width, height=label_height, text=character[i], fg_color="black", corner_radius=10)
                    new_widget.place(relx=0.85, rely=y_loc,anchor=CENTER)
                    
                if type == "solution_labels":
                    new_widget = CTkLabel(self.solution_frame_output, width=60, height=30, text=character[i], font=(None, 18), fg_color="black", corner_radius=10)
                    new_widget.place(relx=0.15, rely=y_loc,anchor=CENTER)
                    
                y_loc += 0.25
                widget_list.append(new_widget)
            return widget_list
               
        """
        Call functions set up problem
        """
        self.initial_state = create_board("initial")
        self.goal_representation = create_board("goal_labels")
        self.solution_representation = create_board("solution_labels", 50,40)
        self.solution_action.configure(text="Waiting for input")
            
    
    
    """
    
    
    EIGHT PUZZLE PROBLEM
    
    
    """
    
    # Init Eight Puzzle
    def init_EightPuzzle(self):
        self.init_states()
        self.after(10, lambda: self.EightPuzzle_gui())

        self.numbers_left = [0,1,2,3,4,5,6,7,8]
        self.numbers_entered = []       
    
    # Validatate user entries
    def validate_eightpuzzle_input(self):
        # throw a validation check for each entry, see callback()
        for i, row_entries in enumerate(self.entries):
            for j, entry in enumerate(row_entries):
                validate_cmd = (self.register(lambda P, i=i, j=j: self.callback(P, i, j)), "%P")
                entry.configure(validate='key', validatecommand=validate_cmd)
    
    def callback(self, P, row, col):
        # Return if input is not a digit, a sequence, or the number 9
        if not P.isdigit() or len(P) > 1 or P == "9":
            return False
        # Check if input already exists
        for i, row_entries in enumerate(self.entries):
            for j, entry in enumerate(row_entries):
                if i == row and j == col:
                    continue  # Skip the entry field
                if entry.get() == P:
                    return False  # Return if duplicate found
        self.numbers_left.remove(int(P))
        self.numbers_entered.append(int(P))
        if len(self.numbers_entered)==6:
            self.after(50, lambda: self.auto_fill_last_three())
        return True
    
    # Fills in the last three entries to make the puzzle solvable.
    def auto_fill_last_three(self):
        entry_array = [int(entry.get()) if entry.get() else "empty" for row in self.entries for entry in row]
        arrays = list(permutations(self.numbers_left, 3))  
        for array in arrays:
            count = 3
            while count > 0:
                for i in range(len(array)):
                    for j in range(len(entry_array)):
                        if entry_array[j] == "empty":
                            entry_array[j] = int(array[i])
                            break
                    count -= 1
            if self.inversion_counter(entry_array):
                break
            entry_array = [int(entry.get()) if entry.get() else "empty" for row in self.entries for entry in row]
        idx = 0  
        for i, row in enumerate(self.entries):
            for j, entry in enumerate(row):
                entry.configure(validate="none")
                entry.delete(0, "end")
                entry.insert(0, int(entry_array[idx]))
                idx += 1
            
    # Reset entries and search if ongoing
    def reset_eight_puzzle(self):
        for row_entries in self.entries:
            for entry in (row_entries):
                self.after(1, entry.configure(validate="none"))
                self.after(2, entry.delete(0,"end"))
                self.after(3,entry.configure(validate="all", validatecommand=NONE))
        for row_label in self.solution_representation:
            for label in row_label:
                label.configure(text="")
        self.numbers_left = [0,1,2,3,4,5,6,7,8]
        self.numbers_entered = []
        self.solution_action.configure(font=(None, 25), text="Waiting for input")
        self.solution_progress.set(0)
        self.validate_eightpuzzle_input()
        self.stop_search = True

    # Iterate through solution and update solution labels
    def update_state_eightpuzzle(self, solution, actions, step_index=0):
        # End search if index ever surpasses solution length or if search manually stopped
        if step_index >=len(solution) or self.stop_search == True:
            return
        
        time = 1000 if self.selected_algorithm.get() != "DFS_algorithm" else 1 # Set time 1000ms, unless Depth First Search
        step = solution[step_index] # init current state   
        action = actions[step_index + 1] # init action to current state

        # Configure labels in solution output frame to match that of the current state
        for i, row in enumerate(self.solution_representation):
            for j, label in enumerate(row):
                label.configure(text=f"{step[i][j]}" if step[i][j] != 0 else "") # Allow for empty space instead of empty string
        if self.selected_algorithm.get() != "DFS_algorithm": # Print performed action on given tile
            if len(action) == 2:
                tile, move = action
                self.solution_action.configure(text=f"{tile} {move}")
            else:
                self.solution_action.configure(text=f"SUCCESS")
            self.expand(action) # Expand action effect
            self.text_size = 30
        else:
            if self.progress < 0.25: # Run this instead if Depth First Search.
                self.solution_action.configure(text=f"Yikes, check that path length!")
            elif 0.25 < self.progress < 0.50:
                self.solution_action.configure(text=f"Hang in there.")
            elif 0.50 < self.progress < 0.75:
                self.solution_action.configure(text=f"... I would grab a coffee")            
            elif 0.75 < self.progress < 1:
                self.solution_action.configure(text=f"Almost there...")
                
        self.progress += 1 / len(solution) # Calculate progress bar increment
        self.solution_progress.set(self.progress) # Update progress bar
        self.after(time, lambda : self.update_state_eightpuzzle(solution, actions, step_index+1)) # Iterate through solution

    # Expand animation effect
    def expand(self, action, start_size=30,size=50):
        if self.text_size < size:
            self.text_size += 0.5
            test = self.text_size
            self.solution_action.configure(font=(None, self.text_size))
            self.after(5, lambda: self.expand(action,start_size, size))
        else:
            self.text_size = start_size

    # Return True or False if user input puzzle is unsolvable
    def inversion_counter(self,array):
        length=len(array)
        number_of_inversion=0
        if len(array) == 3: # If matrix remake as list
            redo_array = [number for row in array for number in row]
        else:
            redo_array=array
            
        number_of_inversion = sum(1 for i in range(length) for j in range(i+1, length)
                                  if 0 not in (redo_array[i],redo_array[j])
                                  and redo_array[i] > redo_array[j])
        return True if number_of_inversion % 2 == 0 else False
    
    def turn_matrix(self):
        array = []
        for row in self.entries:
            row_list = []
            for column in row:
                number = column.get()
                row_list.append(int(number))
            array.append(row_list)
        return array
       
    # Initiate the solve
    def solve_eightpuzzle(self):
        self.progress = 0
        self.text_size = 25
        self.stop_search = False
        self.solution_action.configure(font=(None, 25))
        
        self.solution_progress.set(self.progress)
        self.solution_progress.grid(row=3, column=0, padx=5, pady=2.5)

        # Get user input
        array = self.turn_matrix()

        if self.inversion_counter(array): # If solvable
            # Setting up the Eight Puzzle problem
            problem = EightPuzzle(array)
            solver = Search_Algorithms(problem)
            get_algorithm = self.selected_algorithm.get()           # Get the StringVar from the radiobuttons. 
            assign_algorithm = getattr(solver, get_algorithm, None) # Match the StringVar with the algorithm method in ./Python_files/Algorithms.py
            result = assign_algorithm()                             # Return result (final node)
            solution = problem.reverse_steps(result)                # Return a list with initial state to goal state
            actions = problem.reverse_actions(result)               # Return a list with actions based on the empty tile
            actions.append("SUCCESS")                               # 

            # Update solution frame with the puzzle solution
            self.update_state_eightpuzzle(solution, actions, 0)
            self.after(0, lambda: self.result_of_solution.configure(text=f"Path Length: {len(solution)}    Nodes Explored: {result.explored}"))
            self.after(0, lambda: self.solution_banner.configure(text=f"Solution\n\n{get_algorithm}"))
        else:
            # Code obselete since auto_fill_last_three() makes sure no puzzle input are unsolvable
            center_x, center_y = self.error_popup_loc()
            self.error = CTkToplevel(self)
            self.error.title("Error")
            self.error.geometry(f"{200}x{100}+{center_x}+{center_y}")
            self.error.attributes('-topmost', True)
            error_text = CTkLabel(self.error, text="Not solvable\nInversion prohibited", font=(None, 16))
            error_text.pack(pady=5)
            close_button = CTkButton(self.error, text="Close", command=self.error_window_destroy, font=(None, 16))
            close_button.pack(pady=5)

    """ 
    Setting up the Eight Puzzle UI
    """
    def EightPuzzle_gui(self):
        """
        Initialize buttons - solve and reset
        """
        if self.game_on:
            self.reset_frames()
        self.game_on = True
        self.reset_button.configure(command=self.reset_eight_puzzle)
        self.solve_button.configure(command=self.solve_eightpuzzle)

        """
        Banner change
        """
        self.banner.configure(text="The Eight Puzzle.\n"
                                    "Type in integers between 0-8 (0 representing the empty tile)."
                                    "\nIt will auto place the last three digits to be solvable.\n"
                                    "Press solve to see magic.")
        
        """
        FRAME instantiation
        
        Return a frame with specific configurations for the Eight Puzzle
        """
        def frame_builder(parent_frame):
            frame = CTkFrame(parent_frame, border_width=0, fg_color="transparent")
            frame.grid(row=1, column=0, sticky="nswe", padx=5, pady=5)
            frame.grid_rowconfigure((0,2), weight=2, uniform="a")
            frame.grid_rowconfigure(1, weight=1, uniform="a")
            frame.grid_columnconfigure((0,2), weight=2, uniform="a")
            frame.grid_columnconfigure(1, weight=1, uniform="a")
            return frame
        
        """
        Building the frames
        """
        self.initial_frame_puzzle = frame_builder(self.initial_frame)
        self.goal_frame_puzzle = frame_builder(self.goal_frame)
        self.solution_frame_output = frame_builder(self.solution_frame)
        
        """
        WIDGET instantiation
        
        Returns list with widgets for Eight Puzzle board - input, goal and solution.
        """
        def create_board(type="", frame_size=30, font_size=20):
            widget_list = []
            for i in range(3):
                row_entries = []
                for j in range(3):
                    if type == "entries": new_widget = CTkEntry(self.initial_frame_puzzle, width=frame_size, height=frame_size, validate="all")
                    elif type == "solution_labels": new_widget = CTkLabel(self.solution_frame_output, text="", width=frame_size, height=frame_size, font=(None, font_size), fg_color="black", corner_radius=5)
                    elif type == "goal_labels": new_widget = CTkLabel(self.goal_frame_puzzle, text=f"{goal_state[i][j]}",
                                                                    width=frame_size, height=frame_size, font=(None, font_size), fg_color="black", corner_radius=5)
                    new_widget.grid(row=i, column=j, sticky="e" if j == 0 else "w" if j == 2 else "") # Added logic to make the board nice and neat
                    row_entries.append(new_widget)
                widget_list.append(row_entries)
            return widget_list
        
        """
        Call functions set up problem
        """
        self.entries = create_board("entries")
        self.goal_representation = create_board("goal_labels")
        self.solution_representation = create_board("solution_labels", 50,40)
        self.solution_action.configure(text="Waiting for input")
        self.validate_eightpuzzle_input()
script_dir = os.path.dirname(__file__)
     
bg_wcg_image_path = os.path.join(script_dir,"resources", "images", "bg_wgc.png")

theme_path = os.path.join("resources", "themes", "hades.json")        
set_default_color_theme(theme_path)

def main():
    app = GUI()
    setup_thread = threading.Thread(target=app.mainloop())
    setup_thread.start()
    app.mainloop()
    
if __name__ == main():
    main()
