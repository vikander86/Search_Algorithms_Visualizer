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
        Initializing window
        """
        super().__init__()
        self.controller = controller
        self.geometry("1000x800")
        self.title("Search Algorithms Visualizer")
        self.resizable(False, False)

    def create_main_frames(self):
        """Creates frames for the entire initial window
        """
        self.top_frame = CTkFrame(self,corner_radius=0, height=40, width=1000, fg_color="transparent")
        self.top_frame.place(x=0,y=0)
        
        self.result_frame = CTkFrame(self, corner_radius=0, height=40,width=1000, fg_color="transparent", bg_color="transparent")
        self.result_frame.place(x=0, y=760)
        
        self.description_frame = CTkFrame(self, corner_radius=0, height=120, width=1000, fg_color="transparent", bg_color="transparent")
        self.description_frame.place(x=0,y=40, bordermode="inside")
        
        self.description_text = CTkLabel(self.description_frame, text="Search Algorithm Visualizer", fg_color="transparent", font=(None, 20))
        self.description_text.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        self.initial_frame = CTkFrame(self, corner_radius=20, bg_color="transparent", height=300, width=500, border_width=2, border_color="grey10")
        self.initial_frame.place(x=0,y=160 , bordermode="inside")
        
        self.goal_frame = CTkFrame(self, corner_radius=20, bg_color="transparent",  height=300, width=500, border_width=2, border_color="grey10")
        self.goal_frame.place(x=0,y=460, bordermode="inside")
        
        self.solution_frame = CTkFrame(self, corner_radius=20, bg_color="transparent", height=600, width=500, border_width=2, border_color="grey10")
        self.solution_frame.place(x=500,y=160, bordermode="inside")
        
        self.maze_frame = CTkFrame(self, corner_radius=20, height=600, width=1000, bg_color="transparent", border_width=2, border_color="grey10")
        self.maze_frame.place(x=0, y=160, bordermode="inside")

    
    def description(self, problem):
        if problem == WolfGoatCabbage:
            self.description_text.configure(text="The Wolf, Goat, and Cabbage problem is a classic river crossing puzzle\n"
                                                 "where a farmer must transport a wolf, a goat, and a cabbage across a river using a boat\n"
                                                 "that can only carry the farmer and one of the three items at a time.\n"
                                                 "The challenge is to devise a strategy that prevents the goat from eating the cabbage\n"
                                                 "and the wolf from eating the goat when the farmer is not present.", font=(None,14)) 
    
    def create_dropbox(self):
        """
        Create ComboBox for users algorithm choice
        """
        algorithms = ["Breadth First Search", 
                      "Depth First Search",
                      "Uniform Cost Search",
                      "Best First Search",
                      "A* Search"]
        self.placeholder = StringVar(value="Select an algorithm")
        self.algorithm_dropdown = CTkComboBox(self.top_frame, variable=self.placeholder, command=self.on_algorithm_selected, values=algorithms, state='readonly', width=160)
        self.algorithm_dropdown.place(x=10, rely=0.5, anchor="w")
    
    def create_buttons(self):
        """
        BUTTONS
            top bar:
                Wolf Goat and Cabbage: show initial state, goal state and solution
                Eight Puzzle: show initial state, goal state and solution
                Maze: show maze
                Eight Queens: show chessboard
            buttom bar:
                Reset: reset current problem
                Exit: exit app
        """
        top_frame_button_setup = [("Wolf Goat and Cabbage", 180, self.controller.on_wcg_selected),
                                  ("Eight Puzzle", 340, self.controller.on_eightpuzzle_selected),
                                  ("Maze", 500, self.controller.on_maze_selected),
                                  ("Eigth Queens", 660, self.controller.on_eightqueens_selected)]
        for text, x, command in top_frame_button_setup:
            button = CTkButton(self.top_frame, text=text, font=("Consolas", 12), width=150, command=command)
            button.place(x=x, rely=0.5, anchor="w")
        
        bottom_frame_button_setup = [("Solve", 670, self.controller.solve_problem),
                                     ("Reset", 830, self.controller.reset),
                                     ("EXIT", 990, self.controller.exit)]
        for text, x, command in bottom_frame_button_setup:
            button = CTkButton(self.result_frame, text=text, font=("Consolas", 12), width=150, command=command)
            button.place(x=x, rely=0.5, anchor="e")
            
    def on_algorithm_selected(self, selection):
        """Get user choice from ComboBox

        Args:
            selection (algorithm): sets the current search algorithm for problems
        """
        selection = self.algorithm_dropdown.get()
        self.controller.set_algorithm(selection)
    
    def lift_frames(self, frame):
        frame.lift()
        
    def init_states(self):
        self.initial_state_text = CTkLabel(self.initial_frame, text="Initial State", corner_radius=10, font=("Consolas", 16), height=28, width=150)
        self.initial_state_text.place(relx=0.5,y=20,anchor=CENTER)
        self.goal_state_text = CTkLabel(self.goal_frame, text="Goal State", corner_radius=10, font=("Consolas", 16), height=28, width=150)
        self.goal_state_text.place(relx=0.5, y=20,anchor=CENTER)
        self.solution_text = CTkLabel(self.solution_frame, text="Solution", corner_radius=10, font=("Consolas", 16), height=28, width=150)
        self.solution_text.place(relx=0.5, y=20,anchor=CENTER)
        self.solution_action = CTkLabel(self.solution_frame, text="", corner_radius=10, font=("Consolas", 16), height=80,width=250)
        self.solution_action.place(relx=0.5, rely=0.8, anchor=CENTER)
        
    def init_wcg(self):
        pass
    
    def frame_builder_wsg(self, parent_frame,image_size=(150,220), placement=0.5):
        river_bg = CTkImage(light_image=Image.open(bg_wcg_image_path), size=image_size)
        background_label = CTkLabel(parent_frame, image=river_bg, text="", fg_color="transparent")
        background_label.place(relx=0.5, rely=placement, anchor="center")
    
    def init_frames_wsg(self, frames):
        self.action_text = CTkLabel(self.solution_action, text="test", font=(None, 16))
        self.action_text.place(relx=0.5, rely=0.5, anchor="center")
        for frame in frames:
            parent_frame = getattr(self, frame)
            if frame != "solution_frame":
                self.frame_builder_wsg(parent_frame)
                self.controller.moveable_objects = self.create_board_wsg(frame, parent_frame)
            else:
                self.frame_builder_wsg(parent_frame, (200,300), 0.4)
                self.create_board_wsg(frame, parent_frame) 
            self.lift_frames(parent_frame)
            
    def create_board_wsg(self, frame_name, parent_frame, label_width=60, label_height=20, font_size=14):
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
                widget_list.append(new_widget)   
                y_loc += 0.2
            if frame_name == "solution_frame":
                new_widget = CTkLabel(parent_frame, width=60, height=30, text=character[i], font=(None, 18), fg_color="grey10", corner_radius=10)
                new_widget.place(relx=0.20, rely=y_loc,anchor=CENTER)
                y_loc += 0.12
        if frame_name == "solution_frame": # return list of widgets for manipulation when solving
            return widget_list 
        


