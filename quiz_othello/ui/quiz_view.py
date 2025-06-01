"""
Quiz screen display module
"""

import pygame
from .components import Button, TextBox, ProgressBar
from game.constants import QUIZ_TIMER_SECONDS


class QuizView:
    """Class to display the quiz screen"""
    
    def __init__(self, quiz_manager, screen_width=800, screen_height=600):
        """
        Initialize the quiz screen
        
        Args:
            quiz_manager: Quiz manager object
            screen_width (int): Screen width
            screen_height (int): Screen height
        """
        self.quiz_manager = quiz_manager
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Initialize fonts
        pygame.font.init()
        try:
            # Try to use a font that supports Japanese characters
            self.font = pygame.font.Font(None, 24)  # Use default font
            self.large_font = pygame.font.Font(None, 36)  # Use default font
        except:
            # Fallback to SysFont
            self.font = pygame.font.SysFont(None, 24)
            self.large_font = pygame.font.SysFont(None, 36)
        
        # Define colors
        self.bg_color = (240, 240, 240)
        self.text_color = (0, 0, 0)
        self.timer_color = (255, 0, 0)
        
        # Quiz display area
        self.quiz_area = pygame.Rect(
            screen_width * 0.1,
            screen_height * 0.1,
            screen_width * 0.8,
            screen_height * 0.8
        )
        
        # Timer
        self.timer_bar = ProgressBar(
            self.quiz_area.left,
            self.quiz_area.top,
            self.quiz_area.width,
            20,
            QUIZ_TIMER_SECONDS,
            (0, 200, 0),
            (200, 200, 200)
        )
        
        # Option buttons
        self.option_buttons = []
    
    def draw(self, screen, quiz, remaining_time):
        """
        Draw the quiz screen
        
        Args:
            screen (pygame.Surface): Screen to draw on
            quiz (dict): Quiz data
            remaining_time (float): Remaining time (seconds)
        """
        if not quiz:
            return
        
        # Draw background
        screen.fill(self.bg_color)
        
        # Draw quiz area background
        pygame.draw.rect(screen, (255, 255, 255), self.quiz_area)
        pygame.draw.rect(screen, (0, 0, 0), self.quiz_area, 2)
        
        # Update and draw timer
        self.timer_bar.update(remaining_time)
        self.timer_bar.draw(screen)
        
        # Display question
        self.draw_question(screen, quiz["question"])
        
        # Display options
        self.draw_options(screen, quiz["options"])
    
    def draw_question(self, screen, question):
        """
        Display the question
        
        Args:
            screen (pygame.Surface): Screen to draw on
            question (str): Question text
        """
        try:
            # Draw question text
            question_surface = self.large_font.render(question, True, self.text_color)
            question_rect = question_surface.get_rect(
                center=(self.screen_width // 2, self.quiz_area.top + 80)
            )
            screen.blit(question_surface, question_rect)
        except:
            # Fallback for rendering issues
            # Draw a text box with "Question" text
            text_box = TextBox(
                self.quiz_area.left + 20,
                self.quiz_area.top + 60,
                self.quiz_area.width - 40,
                40,
                "Question: " + question,
                (255, 255, 255),
                (0, 0, 0),
                "center"
            )
            text_box.draw(screen, self.font)
    
    def draw_options(self, screen, options):
        """
        Display the options
        
        Args:
            screen (pygame.Surface): Screen to draw on
            options (list): List of options
        """
        # Initialize option buttons
        if not self.option_buttons or len(self.option_buttons) != len(options):
            self.option_buttons = []
            
            button_width = self.quiz_area.width * 0.8
            button_height = 50
            button_margin = 20
            
            start_y = self.quiz_area.top + 150
            
            for i, option in enumerate(options):
                button = Button(
                    self.quiz_area.left + (self.quiz_area.width - button_width) // 2,
                    start_y + i * (button_height + button_margin),
                    button_width,
                    button_height,
                    option,
                    (100, 100, 200),
                    (150, 150, 255)
                )
                self.option_buttons.append(button)
        
        # Draw option buttons
        for i, button in enumerate(self.option_buttons):
            if i < len(options):
                button.text = options[i]
                button.draw(screen, self.font)
    
    def handle_click(self, pos):
        """
        Process click events
        
        Args:
            pos (tuple): Click position (x, y)
            
        Returns:
            int: Index of the selected option, -1 if none selected
        """
        for i, button in enumerate(self.option_buttons):
            if button.is_clicked(pos, True):
                return i
        
        return -1
    
    def update(self, mouse_pos):
        """
        Update the quiz screen state
        
        Args:
            mouse_pos (tuple): Mouse position (x, y)
        """
        # Update button hover states
        for button in self.option_buttons:
            button.update(mouse_pos)
