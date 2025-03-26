import time
import pygame

from problem import Problem
from visualizer import MazeVisualizer
from astar import AStar
from game_config import *

class Game:
    def __init__(self, maze_file):
        self.problem = Problem(maze_file)
        self.visualizer = MazeVisualizer(self.problem)
    
    def run(self):
        """
        Main game loop that moves Pac-Man toward food locations.
        """
        last_pos = self.problem.initial_state
        
        while self.problem.food_locations:
            # Find the nearest food location using the heuristic function
            nearest_food = min(
                self.problem.food_locations, 
                key=lambda f: AStar.heuristic(self.problem.initial_state, f)
            )
            
            path = AStar.search(self.problem, nearest_food)
            
            if path:
                for step in path:
                    direction = (step[0] - last_pos[0], step[1] - last_pos[1])  # Get movement direction
                    last_pos = step
                    self.problem.visited_cells.add(step)
                    
                    # Update the maze when Pac-Man eats food or pie
                    if self.problem.maze[step[0]][step[1]] == FOOD_CHAR:
                        self.problem.maze[step[0]][step[1]] = EXPLORED_CHAR
                        self.problem.food_locations.remove(step)
                    elif self.problem.maze[step[0]][step[1]] == PIE_CHAR:
                        self.problem.maze[step[0]][step[1]] = EXPLORED_CHAR

                    # Update the visualizer and add a small delay
                    self.visualizer.toggle_pacman_mouth()
                    self.visualizer.draw(step, direction)
                    time.sleep(SLEEP_DURATION)
            
            # Update Pac-Man's current position
            self.problem.initial_state = nearest_food
        
        pygame.quit()