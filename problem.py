from game_config import *

class Problem:
    def __init__(self, file_path):
        """
        Initializes the problem by loading the maze and setting initial values.
        """
        self.maze = []
        self.initial_state = None
        self.food_locations = []
        self.visited_cells = set()
        self.power_steps = 0
        self.load_maze(file_path)
    
    def load_maze(self, file_path):
        """
        Loads the maze from a file and identifies the initial state and food locations.
        """
        with open(file_path, 'r') as f:
            self.maze = [list(line.strip()) for line in f.readlines()]
        
        for x, row in enumerate(self.maze):
            for y, cell in enumerate(row):
                if cell == 'P':
                    self.initial_state = (x, y)
                elif cell == '.':
                    self.food_locations.append((x, y))
    
    def get_actions(self, state, current_power):
        """
        Returns the possible actions (next states) Pac-Man can take.
        """
        x, y = state
        directions = [UP, DOWN, LEFT, RIGHT]
        actions = []
        corners = self.get_corner_positions()

        # If Pac-Man is in a corner, allow teleportation to opposite corners
        if state in corners:
            opposite_corners = list(self.get_opposite_corners(state))
            actions.extend(opposite_corners)

        # Check adjacent cells for valid movement
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < len(self.maze) and 0 <= new_y < len(self.maze[0]):
                cell = self.maze[new_x][new_y]
                
                if cell != '%' or current_power > 0:
                    actions.append((new_x, new_y))
        
        return actions

    def get_corner_positions(self):
        """
        Returns the set of corner positions in the maze.
        """
        row_len = len(self.maze)
        col_len = len(self.maze[0])
        return {(1, 1), (1, col_len - 2), (row_len - 2, 1), (row_len - 2, col_len - 2)}

    def get_opposite_corners(self, current_corner):
        """
        Returns the opposite corners that Pac-Man can teleport to.
        """
        corners = self.get_corner_positions()
        
        # Filter corners to exclude the current corner and the diagonal corner
        return {corner for corner in corners 
                if corner != current_corner and (corner[0] == current_corner[0] or corner[1] == current_corner[1])}
