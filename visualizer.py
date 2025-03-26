import pygame
import math

from game_config import *

class MazeVisualizer:
    def __init__(self, problem):
        """
        Initializes the visualizer with the given problem.
        """
        self.problem = problem
        pygame.init()
        self.width = len(problem.maze[0]) * CELL_SIZE
        self.height = len(problem.maze) * CELL_SIZE
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.frame_count = 0
        self.pacman_mouth_open = False  # Track Pac-Man's mouth state
    
    def toggle_pacman_mouth(self):
        """
        Toggles Pac-Man's mouth open and closed.
        """
        self.pacman_mouth_open = not self.pacman_mouth_open

    def draw_pacman(self, pacman_pos, direction):
        """
        Draws Pac-Man at the given position facing the specified direction.
        """
        x = pacman_pos[1] * CELL_SIZE + CELL_SIZE // 2
        y = pacman_pos[0] * CELL_SIZE + CELL_SIZE // 2
        
        mouth_opening = PACMAN_MOUTH_ANGLE if self.pacman_mouth_open else 0
        
        # Adjust Pac-Man's mouth direction
        if direction == RIGHT:
            start_angle = 360 - mouth_opening / 2
            end_angle = mouth_opening / 2
        elif direction == UP:
            start_angle = 90 - mouth_opening / 2
            end_angle = 90 + mouth_opening / 2
        elif direction == LEFT:
            start_angle = 180 - mouth_opening / 2
            end_angle = 180 + mouth_opening / 2
        else:  # DOWN
            start_angle = 270 - mouth_opening / 2
            end_angle = 270 + mouth_opening / 2
        
        pygame.draw.circle(self.screen, PACMAN_COLOR, (x, y), PACMAN_RADIUS)
        
        pygame.draw.arc(
            self.screen, BG_COLOR, 
            (x - PACMAN_RADIUS, y - PACMAN_RADIUS, CELL_SIZE, CELL_SIZE),
            math.radians(start_angle), math.radians(end_angle), PACMAN_RADIUS
        )
        
        # Draw Pac-Man's mouth lines
        mouth_x1 = x + math.cos(math.radians(start_angle)) * PACMAN_RADIUS
        mouth_y1 = y - math.sin(math.radians(start_angle)) * PACMAN_RADIUS
        pygame.draw.line(self.screen, BG_COLOR, (x, y), (mouth_x1, mouth_y1), WALL_BORDER_THICKNESS)

        mouth_x2 = x + math.cos(math.radians(end_angle)) * PACMAN_RADIUS
        mouth_y2 = y - math.sin(math.radians(end_angle)) * PACMAN_RADIUS
        pygame.draw.line(self.screen, BG_COLOR, (x, y), (mouth_x2, mouth_y2), WALL_BORDER_THICKNESS)
    
    def draw(self, pacman_pos, direction):
        """
        Draws the game board, including walls, food, power-ups, and Pac-Man.
        """
        self.screen.fill(BG_COLOR)
        pulse_radius = PULSE_MIN_RADIUS + PULSE_VARIATION * math.sin(self.frame_count * 1)

        for x, row in enumerate(self.problem.maze):
            for y, cell in enumerate(row):
                rect = pygame.Rect(y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if cell == WALL_CHAR:  # Wall
                    pygame.draw.rect(self.screen, WALL_COLOR, rect, border_radius=8)
                    pygame.draw.rect(self.screen, BORDER_COLOR, rect, WALL_BORDER_THICKNESS, border_radius=8)
                elif cell == FOOD_CHAR:  # Food
                    pygame.draw.circle(self.screen, FOOD_COLOR, rect.center, int(pulse_radius))
                elif cell == PIE_CHAR:  # Pie
                    pygame.draw.polygon(self.screen, DIAMOND_COLOR, [
                        (rect.centerx, rect.top + CELL_SIZE * DIAMOND_SHRINK_FACTOR),
                        (rect.right - CELL_SIZE * DIAMOND_SHRINK_FACTOR, rect.centery),
                        (rect.centerx, rect.bottom - CELL_SIZE * DIAMOND_SHRINK_FACTOR),
                        (rect.left + CELL_SIZE * DIAMOND_SHRINK_FACTOR, rect.centery)
                    ])
                elif (x, y) not in self.problem.visited_cells:
                    pygame.draw.circle(self.screen, DOT_COLOR, rect.center, SMALL_DOT_RADIUS)

        self.draw_pacman(pacman_pos, direction)
        
        pygame.display.flip()
        self.frame_count += 1
