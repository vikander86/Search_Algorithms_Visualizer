from tkinter import *
from customtkinter import *
import threading

"""
init states for Eight Puzzle
"""
goal_state = [[1,2,3],
              [4,5,6],
              [7,8,0]]

class GUI(CTk):
    def __init__(self, *args, **kwargs):

        """
        Initializing window
        """
        super().__init__(*args, **kwargs, )
        self.geometry("1000x800")
        self.grid_columnconfigure((0,1,2,3,4), weight=1, uniform="a")
        self.grid_rowconfigure(0,weight=1, uniform="a")
        self.grid_rowconfigure(4,weight=2, uniform="a")
        self.grid_rowconfigure((1,2,3),weight=3, uniform="a")
        
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
        result_frame.grid(row = 4, column=1, columnspan=4, padx= 10, pady=(5,5), sticky="nswe")
        result_frame.grid_rowconfigure(0, weight=1, uniform="a")
        result_frame.grid_columnconfigure((0,1,2,3), weight=1, uniform="a")
        
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
        self.solution_frame.grid_rowconfigure((1,2), weight=3, uniform="a")
        self.solution_frame.grid_columnconfigure(0, weight=1, uniform="a")
        
        
        """
        LEFT FRAME: Radio buttons
        """
        
        # Variable to store radio button press
        self.selected_algorithm = StringVar(value="BFS")
        
        # Buttons for each of the algorithms included
        self.radio_button_BFS = CTkRadioButton(left_frame,variable=self.selected_algorithm, value="BFS", text="Breadth First Search")
        self.radio_button_DFS = CTkRadioButton(left_frame,variable=self.selected_algorithm, value="DFS", text="Depth First Search")
        self.radio_button_UFC = CTkRadioButton(left_frame,variable=self.selected_algorithm, value="UFC", text="Uniform Cost Search")
        self.radio_button_BeFS = CTkRadioButton(left_frame,variable=self.selected_algorithm, value="BeFS", text="Best First Search")
        self.radio_button_astar = CTkRadioButton(left_frame, variable=self.selected_algorithm, value="A*", text="A* Search")
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
        
        self.reset_button = CTkButton(result_frame, text="RESET", width=100, height=50, corner_radius=50, command=self.reset_board)
        self.reset_button.grid(row=0, column=1, padx=(2.5,2.5), pady=10, sticky="w")
        
        
        """
        INITIAL STATE & GOAL STATE
        """
        self.entries = []
        
        self.initial_state_text = CTkLabel(self.initial_frame, text="Initial State", fg_color="transparent")
        self.initial_state_text.grid(row=0, column=0, sticky="nwe", padx=5, pady=5)
        
        self.goal_state_text = CTkLabel(self.goal_frame, text="Goal State", fg_color="transparent")
        self.goal_state_text.grid(row=0, column=0, sticky="nwe", padx=5, pady=5)
        
        self.solution_text = CTkLabel(self.solution_frame, text="Solution", fg_color="transparent")
        self.solution_text.grid(row=0, column=0, padx=5,pady=5, sticky="nwe")
        

    def button_exit(self):
        exit(1)
    
    def clear_entries(self):
        self.entries = []
    
    """
    METHODS FOR EIGTH PUZZLE
    """
    def init_EightPuzzle(self):
        self.banner.configure(text="Loading EightPuzzle")
        
        setup_thread = threading.Thread(target=self.EightPuzzle_gui)        
        setup_thread.start()
    
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
        for row_entries in (self.entries):
            for entry in (row_entries):
                entry.configure(validate="none")
                entry.delete(0,"end")
                entry.configure(validate="all")
    
    # Setting up the Eight Puzzle UI
    def EightPuzzle_gui(self):
       
        
        # self.reset_button.configure(command=self.reset_board)
        
        """
        Banner change
        """
        self.banner.configure(text="The Eight Puzzle.\nType in integers between 0-8 (0 representing the empty tile).\nPress solve to see magic.")
        
        """
        Initialize grid, button input for initial state
        """
        
        self.initial_frame_puzzle = CTkFrame(self.initial_frame, border_width=0, fg_color="transparent")
        self.initial_frame_puzzle.grid(row=1, column=0, sticky="nswe", padx=5, pady=5)
        self.initial_frame_puzzle.grid_rowconfigure((0,2), weight=2, uniform="a")
        self.initial_frame_puzzle.grid_rowconfigure(1, weight=1, uniform="a")
        self.initial_frame_puzzle.grid_columnconfigure((0,2), weight=2, uniform="a")
        self.initial_frame_puzzle.grid_columnconfigure(1, weight=1, uniform="a")
        
        """
        Logic for creating Eight Puzzle board with entries.
        """

        # Create entry widgets for input
        for i in range(3):
            row_entries = []
            for j in range(3):
                entry = CTkEntry(self.initial_frame_puzzle, width=30, height=30, validate="all")
                entry.grid(row=i, column=j, sticky="e" if j == 0 else "w" if j == 2 else "") # Added logic to make the board nice and neat
                row_entries.append(entry)
            self.entries.append(row_entries)
        
        # Logic for validating inputs (see callback())
        for i, row_entries in enumerate(self.entries):
            for j, entry in enumerate(row_entries):
                # setting up validation cmd, 
                validate_cmd = (self.register(lambda P, i=i, j=j: self.callback(P, i, j)), "%P")
                entry.configure(validate='key', validatecommand=validate_cmd)
 
        """
        Load goal state - set to default, make adjustable later
        """
        self.goal_frame_puzzle = CTkFrame(self.goal_frame, border_width=0, fg_color="transparent")
        self.goal_frame_puzzle.grid(row=1, column=0, sticky="nswe", padx=5, pady=5)
        self.goal_frame_puzzle.grid_rowconfigure((0,2), weight=2, uniform="a")
        self.goal_frame_puzzle.grid_rowconfigure(1, weight=1, uniform="a")
        self.goal_frame_puzzle.grid_columnconfigure((0,2), weight=2, uniform="a")
        self.goal_frame_puzzle.grid_columnconfigure(1, weight=1, uniform="a")
        
        
        # create a list of goal labels
        self.goal_representation = []
        
        for i in range(3):
            row_entries = []
            for j in range(3):
                goal_tile = CTkLabel(self.goal_frame_puzzle, text=f"{goal_state[i][j]}", 
                                     width=30, height=30, font=(None, 20), fg_color="black", corner_radius=5)
                if j == 0:
                    sticky_value = "e"
                elif j == 2:
                    sticky_value = "w"
                else:
                    sticky_value = ""
                goal_tile.grid(row=i, column=j, sticky=sticky_value)
                row_entries.append(goal_tile)
            self.goal_representation.append(row_entries)
            
        def entry_puzzle_state(self):
            puzzle_state = []
            for row_entry in self.entries:
                row_state = []
                for entry in row_entry:
                    value = entry.get()
                    row_state.append(value)
                row_state.append(puzzle_state)
                

theme_path = os.path.expanduser("~/Programmering/CTK_theme_builder/ctk_theme_builder/user_themes/Hades.json")
set_default_color_theme(theme_path)
app = GUI()
app.mainloop()
