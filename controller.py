# controller.py

from itertools import permutations
from gui import GUI
from problems import WolfGoatCabbage, EightPuzzle, Maze
from algorithms import Search_Algorithms
from utils import *

class AppController:
    """
    Controls the application logic, interfacing between the GUI and the problem-solving algorithms.
    
    This controller manages user interactions, problem selection, algorithm execution, 
    and updates the GUI based on the state of the problem-solving process.
    """
    def __init__(self):
        """
        Initializes the AppController with default settings.
        
        Sets up the connection to the GUI, initializes variables to manage the selected algorithm,
        the current problem, the animation state, and movable entities for visualization.
        """
        self.view = GUI(self)
        self.algorithm = None
        self.problem = None
        self.game_on = False
        self.moveable_entities = None
        self.maze = maze_one
        
    """
    initializaion
    """
    def run(self):
        """
        Initiates the main application loop, starting the GUI event listening loop.
        """
        self.view.mainloop()
        
    def setup_initial_gui_state(self): 
        """
        Sets up the initial state of the GUI by creating main frames, dropdowns, and buttons.
        """
        self.view.create_main_frames()
        self.view.setup_algorithm_dropdown()
        self.view.setup_interaction_buttons()

    def set_algorithm(self, algorithm):
        """
        Sets the current algorithm based on user selection from the GUI.

        Args:
            algorithm (str): The name of the algorithm selected by the user.
        """
        if algorithm == "Breadth First Search": self.algorithm = "BFS"
        if algorithm == "Depth First Search": self.algorithm = "DFS"
        if algorithm == "Uniform Cost Search": self.algorithm = "UFC"
        if algorithm == "Best First Search": self.algorithm = "BeFE"
        if algorithm == "A* Search": self.algorithm = "Astar"

    def destroy_moveable_enties(self):
        """
        Destroys all moveable entities/widgets to clear the GUI before initializing a new problem or resetting.
        """
        if self.moveable_entities != None:
            for entry in self.moveable_entities: entry.destroy()

    
    def prepare_problem_base_state(self):
        """
        Prepares the base GUI state for problem visualization by resetting frames, destroying moveable entities, and initializing state descriptions.
        """
        if self.problem == WolfGoatCabbage or self.problem == EightPuzzle:
            self.reset_frames()
            self.view.init_states()
            self.show_loading_screen()
        if self.problem == Maze:
            self.reset_frames()
            self.view.init_frames_maze()
            self.show_loading_screen()
            
    """
    Problem Selection Handlers
    """
    def on_wcg_selected(self):
        """
        Handler for when the Wolf, Goat, and Cabbage problem is selected.
        Prepares the GUI for this specific problem and loads its description.
        """
        self.problem = WolfGoatCabbage
        self.view.init_problem_board()
        self.view.init_frames_wsg(["initial_frame","solution_frame","goal_frame"])
        self.view.update_description(self.problem)

    def on_eightpuzzle_selected(self):
        """
        Handler for when the Eight Puzzle problem is selected.
        Prepares the GUI for this specific problem, resets number entries, and initializes the problem's frames.
        """
        self.problem = EightPuzzle
        self.view.init_problem_board()
        self.view.init_frames_eightpuzzle(["initial_frame","solution_frame","goal_frame"])
        self.view.update_description(self.problem)
        self.numbers_entered = []
        self.numbers_left = [0,1,2,3,4,5,6,7,8]

    def on_maze_selected(self):
        self.problem = Maze
        self.view.init_problem_board()
        self.view.init_frames_maze()        
    
    def on_eightqueens_selected(self):
        pass
    
    
    """
    Algorithm Setup and Execution
    """
    def convert_entries_to_matrix(self):    
        """
        Converts the user entries from the Eight Puzzle GUI into a matrix format suitable for the problem algorithm.
        
        Returns:
            list: A matrix representation of the Eight Puzzle based on user input.
        """
        self.matrix = []
        for row in self.view.entries:
            row_list = []
            for column in row:
                number = column.get()
                row_list.append(int(number))
            self.matrix.append(row_list)
        return self.matrix
    
    def flatten_matrix_to_array(self):
        """
        Flattens the matrix of user entries for the Eight Puzzle into a single list (array) for easy processing.
        """
        array = []
        for obj in self.view.entries:
            for entry in obj:
                number = entry.get()
                array.append(int(number))
        return array
    
    def get_search_results(self):
        """
        Executes the selected search algorithm on the currently selected problem and retrieves the solution path and actions.

        Returns:
            tuple: Contains the list of actions to solve the problem, the solution path, and the result node.
        """
        if self.problem == EightPuzzle:
            matrix = self.convert_entries_to_matrix()
            array = self.flatten_matrix_to_array()
            problem = self.problem(matrix)
            self.moveable_entities = self.view.solution_board_eightpuzzle(array)
        elif self.problem == WolfGoatCabbage:    
            problem = self.problem()
        elif self.problem == Maze:
            problem = self.problem()
            problem.maze = maze_one
            
        solver = Search_Algorithms(problem)
        algorithm = getattr(solver, self.algorithm, None)
        result = algorithm()
        solution = problem.reverse_steps(result)                # Return a list with initial state to goal state
        actions = problem.reverse_actions(result)
        
        return actions, solution, result
    

    def execute_problem_solution(self):
        """
        Executes the solution animation for the selected problem based on the search results obtained from the selected algorithm.
        """
        if self.algorithm is None:
            self.view.display_error_message("Choose algorithm first")
            return
        self.text_size = 10 if self.problem == WolfGoatCabbage else 20
        self.game_on = True
            
        actions, solution, result = self.get_search_results()

        if self.problem == WolfGoatCabbage:
            self.view.after(5, lambda: self.view.result_of_solution.configure(text=f"Path Length: {len(solution)}\n"
                                                                                    f"Nodes Explored: {result.explored}"))
            actions.append(("", {None,"Finished"}))
            self.view.after(1000, lambda: self.animate_solution_wgc(solution, actions))
        elif self.problem == EightPuzzle:
            self.view.after(5, lambda: self.view.result_of_solution.configure(text=f"Path Length: {len(solution)}\n"
                                                                                    f"Nodes Explored: {result.explored}"))
            actions.append("SUCCESS")
            self.view.after(1000, lambda: self.animate_solution_eightpuzzle(solution, actions))
        elif self.problem == Maze:
            solution.reverse()
            self.view.after(1000, lambda: self.animate_path_maze(result, solution, actions))

    """
    GUI State Management
    """
    def reset(self):
        """
        Resets the current problem visualization to its initial state, clearing any moveable entities or selections made.
        """
        self.game_on = False
        if self.problem == WolfGoatCabbage:
            for widget  in self.moveable_entities:
                widget.destroy()
            self.view.after(500, lambda: self.view.init_frames_wsg(["solution_frame"]))
        if self.problem == EightPuzzle:
            for widget in self.moveable_entities.values():
                widget.destroy()
            self.view.init_frames_eightpuzzle(["solution_frame"])
            self.numbers_left = [1,2,3,4,5,6,7,8,0]
            self.numbers_entered = []
        if self.problem == Maze:
            self.view.maze_frame.destroy()
            self.view.init_problem_board()
            self.view.init_frames_maze()
            
            return
        self.view.solution_action.configure(text="")
        self.view.result_of_solution.configure(text="")

    def reset_frames(self, frame=None):
        """
        Clears all widgets from the main frames (initial, goal, and solution frames) in preparation for a new problem or reset.
        """
        for widget in self.view.problem_board.winfo_children(): widget.destroy()
        self.game_on = False
        
    def show_loading_screen(self):
        """
        Displays an empty screen briefly before visualizing the solution to simulate processing time.
        """
        self.view.loading_frame.lift()
        self.view.after(500, lambda: self.view.loading_frame.lower())        
        
    def exit(self):
        """
        Closes the application window and terminates the program.
        """
        self.view.destroy()


    """
    GUI Updates and Animations
    """
    def expand_text(self, action, start_size=10,size=25):
        """
        Gradually increases the font size of solution action text for visual emphasis.

        Args:
            action (dict): The current action being animated or highlighted.
            start_size (int, optional): Starting text size. Defaults to 10.
            size (int, optional): Decrement in text size. Defaults to 25.
        """
        if self.text_size < size:
            self.text_size += 0.3
            self.view.solution_action.configure(font=(None, self.text_size))
            self.view.after(5, lambda: self.expand_text(action,start_size, size))
        else:
            self.text_size = start_size
            
    def move_characters_wsg(self,state, direction, x):
        """
        Moves characters in the Wolf, Goat, and Cabbage problem animation based on the specified direction.

        Args:
            state (widget): The character widget to be moved.
            direction (str): The direction in which to move the character ("Left" or other implies "Right").
            x (float): The starting relative x-position of the character widget.
        """
        if not self.game_on:
            return
        if direction == "Left":
            if x > 0.20:
                x -= 0.005
                state.place(relx=x)
                self.view.after(5, lambda: self.move_characters_wsg(state,direction,x))
        else:
            if x < 0.80:
                x += 0.005
                state.place(relx=x)
                self.view.after(5, lambda: self.move_characters_wsg(state,direction,x))

    def animate_solution_wgc(self, solution, actions, step_index=0):
        """
        Animates the solution steps for the Wolf, Goat, and Cabbage problem.

        Args:
            solution (list): The sequence of states from the initial to the goal state.
            actions (list): The actions taken to move from one state to the next.
            step_index (int, optional): The current step in the animation sequence. Defaults to 0.
        """
        if step_index >=len(solution) or self.game_on == False:
            return
        
        time = 1500
        action = actions[step_index+1] # init action to current state
        self.game_on = True

        direction, act  = action
        for i in range(len(self.moveable_entities)):
            if "Farmer" in act and i == 0:
                if direction == "Left":
                    self.move_characters_wsg(self.moveable_entities[i], "Left", 0.80)
                else:
                    self.move_characters_wsg(self.moveable_entities[i], "Right", 0.20)
            if "Wolf" in act and i == 1:
                if direction == "Left":
                    self.move_characters_wsg(self.moveable_entities[i], "Left", 0.80)
                else:
                    self.move_characters_wsg(self.moveable_entities[i], "Right", 0.20)       
            if "Goat" in act and i == 2:
                if direction == "Left":
                    self.move_characters_wsg(self.moveable_entities[i], "Left", 0.80)
                else:
                    self.move_characters_wsg(self.moveable_entities[i], "Right", 0.2)         
            if "Cabbage" in act and i == 3:
                if direction == "Left":
                    self.move_characters_wsg(self.moveable_entities[i], "Left", 0.80)
                else:
                    self.move_characters_wsg(self.moveable_entities[i], "Right", 0.20)
            left,right=act
            self.x_left, self.x_right = 0.80,0.20
            if None in act:
                not_none = left if left != None else right
                self.view.solution_action.configure(text=f"{not_none}\n"
                                                         f"{direction}")
            else:
                self.view.solution_action.configure(text=f"{left} & {right}\n"
                                                    f"{direction}")
        self.expand_text(action,10,25)
        self.text_size = 10
        self.view.after(time, lambda: self.animate_solution_wgc(solution,actions, step_index + 1))
        

    
    def move_tile_eightpuzzle(self,action, increment):
        """Move tile in EightPuzzle based on action

        Args:
            action (string): Contains obj that performs the action, and direction of action
            increments (int): _description_
        """
        if action == "SUCCESS":
            return
        tile = self.moveable_entities[action[0]]
        placement_info = tile.place_info()
        new_x = float(placement_info.get("relx", 0))
        new_y = float(placement_info.get("rely", 0))
        if increment <= 0.15 and increment >= 0:
            if action[1] == "left":
                new_x -= 0.005
                tile.place(relx=new_x, rely=new_y)
            if action[1] == "right":
                new_x += 0.005
                tile.place(relx=new_x, rely=new_y)
            if action[1] == "up":
                new_y -= 0.005
                tile.place(relx=new_x, rely=new_y)
            if action[1] == "down":
                new_y += 0.005
                tile.place(relx=new_x, rely=new_y)
            increment -= 0.005
            self.view.after(5, lambda: self.move_tile_eightpuzzle(action, increment))
            
    def animate_solution_eightpuzzle(self, solution, actions, step_index=0):
        """      
        Animates the solution steps for the Wolf, Goat, and Cabbage problem.     

        Args:
            solution (list): The sequence of states from the initial to the goal state.
            actions (list): The actions taken to move from one state to the next.
            step_index (int, optional): The current step in the animation sequence. Defaults to 0.
        """
        if step_index >=len(solution) or self.game_on == False:
            return
        time = 1000 if self.algorithm != "DFS" else 1 # Set time 1000ms, unless Depth First Search
        action = actions[step_index + 1] # init action to current state
        self.move_tile_eightpuzzle(action, 0.15)

        if self.algorithm != "DFS": # Print performed action on given tile
            if len(action) == 2:
                tile, move = action
                self.view.solution_action.configure(text=f"{tile} {move}")
            else:
                self.view.solution_action.configure(text=f"SUCCESS")
            self.expand_text(action, 20, 35) # expand_text action effect
            self.text_size = 20

        self.view.after(time, lambda : self.animate_solution_eightpuzzle(solution, actions, step_index+1)) # Iterate through solution

    def animate_path_maze(self, result, solution, actions, step_index=0):
        """      
        Animates the solution steps for the Wolf, Goat, and Cabbage problem.     

        Args:
            solution (list): The sequence of states from the initial to the goal state.
            actions (list): The actions taken to move from one state to the next.
            step_index (int, optional): The current step in the animation sequence. Defaults to 0.
        """
        if not self.game_on:
            return
        time = 150
        self.view.result_of_solution.configure(text=f"Nodes Explored: {step_index}\n"
                                                    f"Path Length: {0}")
        if result.visit_list:
            loc = result.visit_list.pop(0)
        else:
            nodes_explored = step_index
            self.view.after(500, lambda: self.animate_solution_maze(solution, result, solution_step=0, step_index=nodes_explored))
            return

        if (loc) in result.frontier_order:
            self.colour_change_frontier(self.view.maze_representation[(loc)], 0)
        else:
            self.colour_change_explored(self.view.maze_representation[(loc)], 0)

        self.view.after(time, lambda : self.animate_path_maze(result,solution, actions, step_index+1)) # Iterate through solution
    
    def colour_change_solution(self, tile, index):
        if not self.game_on:
            return
        shades = ["grey10","grey18","grey26","grey34","grey42","grey50","grey58","grey66","grey74","grey82","grey92"]
        if index < 10:
            tile.configure(text_color="#3471ac", fg_color=shades[index])
            self.view.after(50, lambda : self.colour_change_solution(tile, index+1))
    
    def colour_change_explored(self, tile, index):
        if not self.game_on:
            return
        shades = ['#2e6599','#25517a','#1e4162','#18344e','#13293f','#0f2132','#0c1a28','#0a1520','#08111a','#060e15']
        if index < 10:
            tile.configure(fg_color=shades[index])
            self.view.after(50, lambda : self.colour_change_explored(tile,index+1))
            
    def colour_change_frontier(self, tile, index):
        if not self.game_on:
            return
        shades = ['#142c43','#16314a','#193652','#1c3c5b','#1f4366','#224a71','#26537d','#2a5c8b','#2f669b','#3471ac']
        if index < 10:
            tile.configure(fg_color=shades[index])
            self.view.after(50, lambda : self.colour_change_frontier(tile,index+1))

    def animate_solution_maze(self, solution,result,solution_step,step_index):
        if not self.game_on:
            return
        time = 50 # Set time 1000ms, unless Depth First Search
        if solution:
           loc = solution.pop(0)
           x,y = loc
           x,y = int(x),int(y)
        else:
            return
        self.view.result_of_solution.configure(text=f"Nodes Explored: {step_index}\n"
                                                    f"Path Length: {solution_step}")
        self.colour_change_solution(self.view.maze_representation[(x,y)], 0)
        self.view.after(time, lambda : self.animate_solution_maze(solution,result,solution_step+1,step_index)) # Iterate through solution

    """
    Validation and Helpers
    """ 
    def validate_eightpuzzle_input(self):
        """
        Sets up validation for each entry in the Eight Puzzle grid to ensure that all entries are unique,
        conform to puzzle rules, and are digits between 1 to 8 and 0 representing the empty tile. 
        This function does not return a value but configures each entry widget for on-the-fly validation.
        """
        for i, row_entries in enumerate(self.view.entries):
            for j, entry in enumerate(row_entries):
                def make_validate_command(i=i, j=j):
                    return self.view.register(lambda P, i=i, j=j: self.callback(P, i, j)), "%P"
                validate_cmd = make_validate_command(i, j)
                entry.configure(validate="key", validatecommand=validate_cmd)

    def callback(self, P, row, col):
        """
        Validates the input for each tile in the Eight Puzzle, ensuring no duplicates and that each entry is valid.
        Triggers autofill for the last three entries when applicable to ensure the puzzle remains solvable.

        Args:
            P (str): The entry value to validate.
            row (int): Row index of the entry being validated.
            col (int): Column index of the entry being validated.

        Returns:
            bool: True if the entry is valid, False otherwise.
        """
        # Return if input is not a digit, a sequence, or the number 9
        if not P.isdigit() or len(P) > 1 or P == "9":
            return False
        # Check if input already exists
        for i, row_entries in enumerate(self.view.entries):
            for j, entry in enumerate(row_entries):
                if i == row and j == col:
                    continue  # Skip the entry field
                if entry.get() == P:
                    return False  # Return if duplicate found
        self.numbers_left.remove(int(P))
        self.numbers_entered.append(int(P))
        if len(self.numbers_entered)==6:
            self.view.after(30, lambda: self.auto_fill_last_three())
        return True
    
    def inversion_counter(self,array):
        """
        Counts the number of inversions in the puzzle grid to determine if the puzzle is solvable.
        An inversion occurs when a higher number precedes a lower number in the puzzle sequence.
        For the puzzle to be solvable, the number of inversions must be even.

        Args:
            array (list): The puzzle grid represented as a flat list or 2D matrix of integers.

        Returns:
            bool: True if the number of inversions is even, indicating the puzzle is solvable.
        """
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

    def auto_fill_last_three(self):
        """
        Automatically fills in the last three empty tiles with the remaining numbers in a way that ensures
        the puzzle is solvable, based on the inversion count. This function directly updates the UI entries
        with the correct values to complete the puzzle setup.

        Uses permutations to test possible combinations of the remaining numbers and fills them in when a
        solvable configuration (even number of inversions) is found.
        """
        entry_array = [int(entry.get()) if entry.get() else "empty" for row in self.view.entries for entry in row]
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
            entry_array = [int(entry.get()) if entry.get() else "empty" for row in self.view.entries for entry in row]
        idx = 0  
        for i, row in enumerate(self.view.entries):
            for j, entry in enumerate(row):
                entry.configure(validate="none")
                entry.delete(0, "end")
                entry.insert(0, int(entry_array[idx]))
                idx += 1
                entry.configure(validate="key")