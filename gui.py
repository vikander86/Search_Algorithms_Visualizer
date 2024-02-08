# gui.py
from customtkinter import *
from problems import *
from utils import Node


theme_path = os.path.join("resources", "themes", "hades.json")        
set_default_color_theme("dark-blue")

class GUI(CTk):
    def __init__(self, controller):
        """
        Initializing window
        """
        super().__init__()
        self.controller = controller
        self.geometry("1000x800")
        self.title("Search Algorithms Visualizer")
        self.resizable(False, False)

    def create_main_frames(self):
        """
        MAIN FRAMES
        """
        self.top_frame = CTkFrame(self,corner_radius=0, height=40, width=1000, fg_color="transparent")
        self.top_frame.place(x=0,y=0)
        
        self.result_frame = CTkFrame(self, corner_radius=0, height=40,width=1000, fg_color="transparent")
        self.result_frame.place(x=0, y=760)
        
        self.description_frame = CTkFrame(self, corner_radius=0, height=120, width=1000)
        self.description_frame.place(x=0,y=40)
        
        self.initial_frame = CTkFrame(self, corner_radius=0, height=300, width=500)
        self.initial_frame.place(x=0,y=160)
        
        self.goal_frame = CTkFrame(self, corner_radius=0, height=300, width=500)
        self.goal_frame.place(x=0,y=460)
        
        self.solution_frame = CTkFrame(self, corner_radius=0, height=600, width=500)
        self.solution_frame.place(x=500,y=160)
        
    def create_dropbox(self):
        """
        COMBOBOX for algorithms
        """
        algorithms = ["Breadth First Search", 
                      "Depth First Search",
                      "Uniform Cost Search",
                      "Best First Search",
                      "A* Search"]
        self.placeholder = StringVar(value="Select an algorithm")
        self.algorithm_dropdown = CTkComboBox(self.top_frame, variable=self.placeholder, command=self.on_algorithm_selected, values=algorithms, state='readonly', width=160)
        self.algorithm_dropdown.place(x=10, rely=0.5, anchor="w")
        
    def on_algorithm_selected(self, selection):
        # Get the selected algorithm from the dropdown
        selection = self.algorithm_dropdown.get()
        # Call the controller's method and pass the selection
        self.controller.set_algorithm(selection)

    def create_buttons(self):
        """
        BUTTONS
        """
        top_frame_button_setup = [("Wolf Goat and Cabbage", 180, self.controller.on_wcg_selected),
                                  ("Eight Puzzle", 340, self.controller.on_eightpuzzle_selected),
                                  ("Maze", 500, self.controller.on_maze_selected),
                                  ("Eigth Queens", 660, self.controller.on_eightqueens_selected)]
        for text, x, command in top_frame_button_setup:
            button = CTkButton(self.top_frame, text=text, width=150, command=command)
            button.place(x=x, rely=0.5, anchor="w")
            
        self.reset = CTkButton(self.result_frame, text="Reset", width=150, command=self.controller.reset)
        self.reset.place(x=830, rely=0.5, anchor="e")         
        self.exit = CTkButton(self.result_frame, text="Exit", width=150, command=self.controller.exit)
        self.exit.place(x=990, rely=0.5, anchor="e")
