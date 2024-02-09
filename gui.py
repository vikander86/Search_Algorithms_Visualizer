# gui.py
from customtkinter import *
from problems import *
from utils import Node
from PIL import Image


# theme_path = os.path.join("resources", "themes", "hades.json")
set_appearance_mode("Dark")    
set_default_color_theme("dark-blue")
script_dir = os.path.dirname(__file__)
bg_wcg_image_path = os.path.join(script_dir,"resources", "images", "bg_wgc.png")

class GUI(CTk):
    def __init__(self, controller):
        """
        Initialize the GUI for the Search Algorithms Visualizer application.

        Args:
            controller: The controller that handles logic and interaction between the GUI and the application's data model.
        """
        super().__init__()
        self.controller = controller
        self.geometry("1000x800")
        self.title("Search Algorithms Visualizer")
        self.resizable(False, False)
        
        self.goal_state = [[1,2,3],
                           [4,5,6],
                           [7,8,""]]

    def create_main_frames(self):
        """
        Sets up the main frames of the application window, including top, result, description, initial state, goal state,
        solution, and loading frames.
        """
        self.top_frame = CTkFrame(self,corner_radius=0, height=40, width=1000, fg_color="transparent")
        self.top_frame.place(x=0,y=0)
        
        self.result_frame = CTkFrame(self, corner_radius=0, height=40,width=1000, fg_color="transparent", bg_color="transparent")
        self.result_frame.place(x=0, y=760)
        
        self.description_frame = CTkFrame(self, corner_radius=0, height=120, width=1000, fg_color="transparent", bg_color="transparent")
        self.description_frame.place(x=0,y=40, bordermode="inside")
        
        self.description_text = CTkLabel(self.description_frame, text="", fg_color="transparent", font=(None, 16))
        self.description_text.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        self.initial_frame = CTkFrame(self, corner_radius=20, bg_color="transparent", height=300, width=500, border_width=2, border_color="grey10")
        self.initial_frame.place(x=0,y=160 , bordermode="inside")
        
        self.goal_frame = CTkFrame(self, corner_radius=20, bg_color="transparent",  height=300, width=500, border_width=2, border_color="grey10")
        self.goal_frame.place(x=0,y=460, bordermode="inside")
        
        self.solution_frame = CTkFrame(self, corner_radius=20, bg_color="transparent", height=600, width=500, border_width=2, border_color="grey10")
        self.solution_frame.place(x=500,y=160, bordermode="inside")
        
        self.maze_frame = CTkFrame(self, corner_radius=20, height=600, width=1000, bg_color="transparent", border_width=2, border_color="grey10")
        self.maze_frame.place(x=0, y=160, bordermode="inside")
        
        self.loading_frame = CTkFrame(self, corner_radius=20, height=600, width=1000, bg_color="transparent", border_width=2, border_color="grey10")
        self.loading_frame.place(x=0, y=160, bordermode="inside")
        self.loading_frame.lower()
        self.maze_frame.lower()

        self.description_text.configure(text="Welcome to the Search Algorithms Visualizer!\n"
                                             "Get started by selecting a problem from the top menu and an algorithm of your choice\n"
                                             "and watch as the solution unfolds step by step.\n"
                                             "Happy exploring!", font=(None, 14))

    def update_description(self, problem):
        """
        Updates the description text based on the selected problem.

        Args:
            problem: The problem class (e.g., WolfGoatCabbage, EightPuzzle) to provide a description for.
        """
        if problem == WolfGoatCabbage:
            self.description_text.configure(text="The Wolf, Goat, and Cabbage problem is a classic river crossing puzzle\n"
                                                 "where a farmer must transport a wolf, a goat, and a cabbage across a river using a boat\n"
                                                 "that can only carry the farmer and one of the three items at a time.\n"
                                                 "The challenge is to devise a strategy that prevents the goat from eating the cabbage\n"
                                                 "and the wolf from eating the goat when the farmer is not present.", font=(None,14))
        if problem == EightPuzzle:
             self.description_text.configure(text="The Eight Puzzle.\n"
                                                  "Type in integers between 0-8 (0 representing the empty tile)."
                                                  "\nIt will auto place the last three digits to be solvable.\n"
                                                  "Press solve to see magic.")
    
    def setup_algorithm_dropdown(self):
        """
        Creates and configures a dropdown menu for selecting the search algorithm.
        """
        algorithms = ["Breadth First Search", 
                      "Depth First Search",
                      "Uniform Cost Search",
                      "Best First Search",
                      "A* Search"]
        self.placeholder = StringVar(value="Select an algorithm")
        self.algorithm_dropdown = CTkComboBox(self.top_frame, variable=self.placeholder, command=self.on_algorithm_selected, values=algorithms, state='readonly', width=160)
        self.algorithm_dropdown.place(x=10, rely=0.5, anchor="w")
    
    def setup_interaction_buttons(self):
        """
        Creates buttons for problem selection, solving, resetting, and exiting the application.
        """
        top_frame_button_setup = [("Wolf Goat and Cabbage", 180, self.controller.on_wcg_selected),
                                  ("Eight Puzzle", 340, self.controller.on_eightpuzzle_selected),
                                  ("Maze", 500, self.controller.on_maze_selected),
                                  ("Eigth Queens", 660, self.controller.on_eightqueens_selected)]
        for text, x, command in top_frame_button_setup:
            button = CTkButton(self.top_frame, text=text, font=("Consolas", 12), width=150, command=command)
            button.place(x=x, rely=0.5, anchor="w")
        
        bottom_frame_button_setup = [("Solve", 670, self.controller.execute_problem_solution),
                                     ("Reset", 830, self.controller.reset),
                                     ("EXIT", 990, self.controller.exit)]
        for text, x, command in bottom_frame_button_setup:
            button = CTkButton(self.result_frame, text=text, font=("Consolas", 12), width=150, command=command)
            button.place(x=x, rely=0.5, anchor="e")
    
    def display_error_message(self, error):
        """
        Displays a pop-up window with an error message.

        Args:
            error_message (str): The error message to display.
        """
        center_x, center_y = self.view_center()
        self.error = CTkToplevel(self)
        self.error.title("Error")
        self.error.geometry(f"{200}x{100}+{center_x}+{center_y}")
        self.error.attributes('-topmost', True)
        error_text = CTkLabel(self.error, text=error, font=(None, 16))
        error_text.pack(pady=5)
        close_button = CTkButton(self.error, text="Close", command=self.error_destroy, font=(None, 16))
        close_button.pack(pady=5)
            
    def view_center(self):
        main_window_width = self.winfo_width()
        main_window_height = self.winfo_height()
        main_window_x = self.winfo_x()
        main_window_y = self.winfo_y()

        error_width = 200
        error_height = 100

        center_x = main_window_x + (main_window_width - error_width) // 2
        center_y = main_window_y + (main_window_height - error_height) // 2
        return center_x, center_y

    def error_destroy(self):
        """
        Destroy current error window
        """
        self.error.destroy()   
    
    def on_algorithm_selected(self, selection):
        """
        Callback function for when an algorithm is selected from the dropdown menu.

        Args:
            selection (str): The selected algorithm.
        """
        selection = self.algorithm_dropdown.get()
        self.controller.set_algorithm(selection)
    
    def lift_frames(self, frame):
        """
        Bring the frame forward
        """
        frame.lift()
        
    def init_states(self):
        """
        Initializes and places labels for 'Initial State', 'Goal State', and 'Solution' areas, 
        along with action and result of solution labels within the GUI.
        """
        self.initial_state_text = CTkLabel(self.initial_frame, text="Initial State", corner_radius=10, font=("Consolas", 16), height=28, width=150)
        self.initial_state_text.place(relx=0.5,y=20,anchor=CENTER)
        self.goal_state_text = CTkLabel(self.goal_frame, text="Goal State", corner_radius=10, font=("Consolas", 16), height=28, width=150)
        self.goal_state_text.place(relx=0.5, y=20,anchor=CENTER)
        self.solution_text = CTkLabel(self.solution_frame, text="Solution", corner_radius=10, font=("Consolas", 16), height=28, width=150)
        self.solution_text.place(relx=0.5, y=20,anchor=CENTER)
        self.solution_action = CTkLabel(self.solution_frame, text="", corner_radius=10, font=("Consolas", 16), height=80,width=250)
        self.solution_action.place(relx=0.5, rely=0.75, anchor=CENTER)
        self.result_of_solution = CTkLabel(self.solution_frame, text="", corner_radius=10, font=("Consolas", 16), height=40,width=250)
        self.result_of_solution.place(relx=0.5, rely=0.88, anchor="center")
        
    def setup_background_frame_wsg(self, parent_frame,image_size=(150,220), placement=0.5):
        """
        Creates a background frame for the Wolf, Goat, and Cabbage problem using a specified image.

        Args:
            parent_frame: The parent frame where the background image will be placed.
            image_size (tuple, optional): The size of the background image. Defaults to (150,220).
            placement (float, optional): The relative placement of the image within the parent frame. Defaults to 0.5.
        """
        river_bg = CTkImage(light_image=Image.open(bg_wcg_image_path), size=image_size)
        background_label = CTkLabel(parent_frame, image=river_bg, text="", fg_color="transparent")
        background_label.place(relx=0.5, rely=placement, anchor="center")
          
    def setup_board_wsg(self, frame_name, parent_frame, label_width=60, label_height=20, font_size=14):
        """
        Creates and places widgets on the board for the Wolf, Goat and Cabbage problem.

        Args:
            frame_name (str): The name of the frame to create the board in.
            parent_frame: The parent frame object where the board will be created.
            widget_type (str): Type of widgets to create ('initial', 'goal', 'solution').
            label_width (int): Width of each label/widget.
            label_height (int): Height of each label/widget.
            font_size (int): Font size for the label text.
        """
        widget_list = []
        character = ["Farmer","Wolf","Goat","Cabbage"]
        y_loc = 0.2
        for i in range(4):
            if frame_name == "initial_frame":
                new_widget = CTkLabel(parent_frame, width=label_width, height=label_height, 
                                        text=character[i], fg_color="grey10", corner_radius=10)
                new_widget.place(relx=0.25, rely=y_loc,anchor=CENTER)
                y_loc += 0.2
            if frame_name == "goal_frame":
                new_widget = CTkLabel(parent_frame, width=label_width, height=label_height, text=character[i], fg_color="grey10", corner_radius=10)
                new_widget.place(relx=0.75, rely=y_loc,anchor=CENTER)
                y_loc += 0.2
            if frame_name == "solution_frame":
                new_widget = CTkLabel(parent_frame, width=60, height=30, text=character[i], font=(None, 18), fg_color="grey10", corner_radius=10)
                new_widget.place(relx=0.20, rely=y_loc,anchor=CENTER)
                y_loc += 0.12
                widget_list.append(new_widget) 
        if frame_name == "solution_frame": # return list of widgets for manipulation when solving
            return widget_list 
        
    def init_frames_wsg(self, frames):
        """
        Initializes frames for the Wolf, Goat, and Cabbage problem, setting up the board and placing characters.

        Args:
            frames (list): A list of frame names to be initialized and set up.
        """
        for frame in frames:
            parent_frame = getattr(self, frame)
            if frame != "solution_frame":
                self.setup_background_frame_wsg(parent_frame)
                self.setup_board_wsg(frame, parent_frame) 
            else:
                self.setup_background_frame_wsg(parent_frame, (200,300), 0.4)
                self.controller.moveable_entities = self.setup_board_wsg(frame, parent_frame)
            self.lift_frames(parent_frame)
           
    def init_frames_eightpuzzle(self, frames):   
        """
        Initializes frames for the Eight Puzzle problem, creating entry fields for the initial state, 
        labels for the goal state, and preparing the solution visualization.

        Args:
            frames (list): A list of frame names to be initialized for the puzzle setup.
        """
        for frame in frames:
            parent_frame = getattr(self, frame)
            self.lift(parent_frame)
        self.entries = self.create_board_eightpuzzle("entries")
        self.goal_representation = self.create_board_eightpuzzle("goal_labels")
        self.controller.validate_eightpuzzle_input()
    
    def create_board_eightpuzzle(self, type="", widget_size=30, font_size=20):
        """
        Creates and places widgets on the board for the Eight Puzzle problem.

        Args:
            type (str): The name of the frame to create the board in.
            widget_size (int): Width/Height of each label/widget.
            font_size (int): Font size for the label text.
        """
        widget_list = []
        yloc,yloc_solution = 0.3, 0.2
        for i in range(3):
            xloc = 0.4
            xloc_solution = 0.35
            row_entries = []
            for j in range(3):
                if type == "entries": 
                    new_widget = CTkEntry(self.initial_frame, width=widget_size, height=widget_size)
                    new_widget.place(relx=xloc, rely=yloc, anchor="center") # Added logic to make the board nice and neat   
                elif type == "goal_labels": 
                    new_widget = CTkLabel(self.goal_frame, text=f"{self.goal_state[i][j]}",
                                                                width=widget_size, height=widget_size, font=(None, font_size), fg_color="grey10", corner_radius=5)
                    new_widget.place(relx=xloc, rely=yloc, anchor="center") # Added logic to make the board nice and neat   
                row_entries.append(new_widget)
                xloc += 0.1
                xloc_solution += 0.15
            widget_list.append(row_entries)
            yloc += 0.2
            yloc_solution += 0.15            
        return widget_list
    
    def solution_board_eightpuzzle(self):
        """
        Creates and places labels for the Eight Puzzle solution board, mapping each number to a widget.

        Returns:
            dict: A dictionary mapping each number to its corresponding widget on the solution board.
        """
        widgets = {}
        index = 0
        y = 0.2
        for i in range(3):
            x = 0.35
            for j in range(3):
                number = self.controller.array[index]
                if index != self.controller.array.index(0):
                    new_widget = CTkLabel(self.solution_frame, text=self.controller.array[index], width=50, height=50, font=(None, 40), fg_color="grey10", corner_radius=5)
                    new_widget.place(relx=x, rely=y, anchor="center") # Added logic to make the board nice and neat
                    widgets[number] = new_widget
                x += 0.15
                index += 1
            y += 0.15
        return widgets
        


