from tkinter import *
from customtkinter import *
from python_files.algorithms import *
from python_files.containers import *
import threading

theme_path = "C:\\Users\\bager\\OneDrive\\Projects\\Search_algorithms_visualizer\\theme\\Hades.json"
set_default_color_theme(theme_path)

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
        top_frame.grid_columnconfigure((0,1,2,3,4), weight=1)
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
        self.initial_frame.grid_rowconfigure(1, weight=5, uniform="a")
        self.initial_frame.grid_columnconfigure(0, weight=1, uniform="a")

        
        # initialize "goal state" frame
        self.goal_frame = CTkFrame(display_frame)
        self.goal_frame.grid(row=2, column=0, sticky="nswe")
        self.goal_frame.grid_rowconfigure(0, weight=1, uniform="a")
        self.goal_frame.grid_rowconfigure(1, weight=5, uniform="a")
        self.goal_frame.grid_columnconfigure(0, weight=1, uniform="a")
        
        # initialize solution frame
        self.solution_frame = CTkFrame(display_frame)
        self.solution_frame.grid(row=1, rowspan=2, column=1, sticky="nswe")
        self.solution_frame.grid_rowconfigure(0, weight=1, uniform="a")
        self.solution_frame.grid_rowconfigure(1, weight=3, uniform="a")
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
        
        button1 = CTkButton(top_frame, text="Wolf, Goat and Cabbage",  command=self.button_exit, corner_radius=10)
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
        
        """
        INITIAL STATE, GOAL STATE, SOLUTION
        """
        
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
        
        self.stop_search = False
        
    def error_window_destroy(self):
        self.error.destroy()
        self.reset_board()
           
        
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
    
    def button_exit(self):
        exit(0)
    
    def clear_entries(self):
        self.entries = []
    
    """
    METHODS FOR EIGTH PUZZLE
    """
    def init_EightPuzzle(self):
        self.banner.configure(text="Loading EightPuzzle")
        
        setup_thread = threading.Thread(target=self.EightPuzzle_gui)        
        setup_thread.start()
    
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
        return True
    
    # Reset entry inputs
    def reset_board(self):
        for row_entries in self.entries:
            for entry in (row_entries):
                entry.configure(validate="none")
                entry.delete(0,"end")
                entry.configure(validate="all")
        for row_label in self.solution_representation:
            for label in row_label:
                label.configure(text="")
        self.solution_action.configure(font=(None, 25), text="Waiting for input")
        self.solution_progress.set(0)
        self.stop_search = True

    def update_state_eightpuzzle(self, solution, actions, step_index=0):
        if step_index >=len(solution) or self.stop_search == True:
            return

        time = 1000 if self.selected_algorithm.get() != "DFS_algorithm" else 1
        step = solution[step_index]
        action = actions[step_index + 1]

        for i, row in enumerate(self.solution_representation):
            for j, column in enumerate(row):
                column.configure(text=f"{step[i][j]}" if step[i][j] != 0 else "")
        if self.selected_algorithm.get() != "DFS_algorithm":
            self.solution_action.configure(text=f"{action}")
            self.expand(action)
            self.text_size = 30
        else:
            if self.progress < 0.25:
                self.solution_action.configure(text=f"Yikes, check that path length!")
            elif 0.25 < self.progress < 0.50:
                self.solution_action.configure(text=f"Hang in there.")
            elif 0.50 < self.progress < 0.75:
                self.solution_action.configure(text=f"... I would grab a coffee")            
            elif 0.75 < self.progress < 1:
                self.solution_action.configure(text=f"Almost there...")
                
        self.progress += 1 / len(solution)
        if step_index == len(solution) - 1:
            self.solution_action.configure(text=f"SUCCESS")

        self.solution_progress.set(self.progress)
        self.after(time, lambda : self.update_state_eightpuzzle(solution, actions, step_index+1))

    def expand(self, action):
        if self.text_size < 50:
            self.text_size += 0.5
            self.solution_action.configure(font=(None, self.text_size))
            self.after(5, lambda: self.expand(action))
        else:
            self.text_size = 30

    def inversion_counter(self,array):
        number_of_inversion = 0
        redo_array = []
        for row in array:
            for number in row:
                redo_array.append(number)
        for i in range(len(redo_array)):
            for j in range(i+1,len(redo_array)):
                if redo_array[j] == 0 or redo_array[i] == 0:
                    continue
                elif redo_array[i] > redo_array[j]:
                    number_of_inversion += 1

        return True if number_of_inversion % 2 == 0 else False
        
    
    def solve_eightpuzzle(self):
        self.progress = 0
        self.text_size = 25
        self.stop_search = False
        self.solution_action.configure(font=(None, 25))
        
        self.solution_progress.set(self.progress)
        self.solution_progress.grid(row=3, column=0, padx=5, pady=2.5)

        # Get user input
        array = []
        for row in self.entries:
            row_list = []
            for column in row:
                number = column.get()
                row_list.append(int(number))
            array.append(row_list)
        
        if self.inversion_counter(array):
            # Setting up the Eight Puzzle problem
            problem = EightProblem(array)
            solver = Search_Algorithms(problem)
            get_algorithm = self.selected_algorithm.get()           # Get the StringVar from the radiobuttons. 
            assign_algorithm = getattr(solver, get_algorithm, None) # Match the StringVar with the algorithm method in ./Python_files/Algorithms.py
            result = assign_algorithm()                             # Return result (final node)
            solution = problem.reverse_steps(result)                # Return a list with initial state to goal state
            actions = problem.reverse_actions(result)               # Return a list with actions based on the empty tile
            actions.append("SUCCESS")

            self.update_state_eightpuzzle(solution, actions, 0)
            self.after(0, lambda: self.result_of_solution.configure(text=f"Path Length: {len(solution)}    Nodes Explored: {result.explored}"))
            self.after(0, lambda: self.solution_banner.configure(text=f"Solution\n\n{get_algorithm}"))
        else:
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
        self.reset_button.configure(command=self.reset_board)
        self.solve_button.configure(command=self.solve_eightpuzzle)

        """
        Banner change
        """
        self.banner.configure(text="The Eight Puzzle.\nType in integers between 0-8 (0 representing the empty tile).\nPress solve to see magic.")
        
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
        
        

def main():
    app = GUI()
    setup_thread = threading.Thread(target=app.mainloop())
    setup_thread.start()
    app.mainloop()
    
if __name__ == main():
    main()
