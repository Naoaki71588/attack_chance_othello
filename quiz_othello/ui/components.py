"""
UI Common Components
"""

import pygame


class Button:
    """Button component"""
    
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=(255, 255, 255)):
        """
        Initialize button
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
            width (int): Width
            height (int): Height
            text (str): Button text
            color (tuple): Button color (R, G, B)
            hover_color (tuple): Hover color (R, G, B)
            text_color (tuple): Text color (R, G, B)
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
    
    def draw(self, surface, font):
        """
        Draw the button
        
        Args:
            surface (pygame.Surface): Surface to draw on
            font (pygame.font.Font): Font for text rendering
        """
        # Select color based on hover state
        current_color = self.hover_color if self.is_hovered else self.color
        
        # Draw button background
        pygame.draw.rect(surface, current_color, self.rect)
        
        # Draw button border
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        
        # Draw text
        try:
            text_surface = font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)
        except:
            # Fallback if text rendering fails
            # Draw a simple text indicator
            pygame.draw.line(surface, self.text_color, 
                            (self.rect.left + 10, self.rect.centery), 
                            (self.rect.right - 10, self.rect.centery), 2)
    
    def update(self, mouse_pos):
        """
        Update button state
        
        Args:
            mouse_pos (tuple): Mouse coordinates (x, y)
            
        Returns:
            bool: Whether hover state changed
        """
        old_hover = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return old_hover != self.is_hovered
    
    def is_clicked(self, mouse_pos, mouse_click):
        """
        Check if button is clicked
        
        Args:
            mouse_pos (tuple): Mouse coordinates (x, y)
            mouse_click (bool): Mouse click state
            
        Returns:
            bool: Whether button was clicked
        """
        return self.rect.collidepoint(mouse_pos) and mouse_click


class TextBox:
    """Text box component"""
    
    def __init__(self, x, y, width, height, text="", bg_color=(255, 255, 255), text_color=(0, 0, 0), align="left"):
        """
        Initialize text box
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
            width (int): Width
            height (int): Height
            text (str): Text to display
            bg_color (tuple): Background color (R, G, B)
            text_color (tuple): Text color (R, G, B)
            align (str): Text alignment ("left", "center", "right")
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.align = align
    
    def draw(self, surface, font):
        """
        Draw the text box
        
        Args:
            surface (pygame.Surface): Surface to draw on
            font (pygame.font.Font): Font for text rendering
        """
        # Draw background
        pygame.draw.rect(surface, self.bg_color, self.rect)
        
        # Draw border
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 1)
        
        # Draw text
        if self.text:
            try:
                text_surface = font.render(self.text, True, self.text_color)
                text_rect = text_surface.get_rect()
                
                # Set text position
                if self.align == "left":
                    text_rect.midleft = (self.rect.left + 5, self.rect.centery)
                elif self.align == "right":
                    text_rect.midright = (self.rect.right - 5, self.rect.centery)
                else:  # center
                    text_rect.center = self.rect.center
                
                surface.blit(text_surface, text_rect)
            except:
                # Fallback if text rendering fails
                pygame.draw.line(surface, self.text_color, 
                                (self.rect.left + 5, self.rect.centery), 
                                (self.rect.right - 5, self.rect.centery), 1)
    
    def set_text(self, text):
        """
        Set text
        
        Args:
            text (str): Text to display
        """
        self.text = text


class ProgressBar:
    """Progress bar component"""
    
    def __init__(self, x, y, width, height, max_value, color=(0, 255, 0), bg_color=(200, 200, 200)):
        """
        Initialize progress bar
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
            width (int): Width
            height (int): Height
            max_value (float): Maximum value
            color (tuple): Bar color (R, G, B)
            bg_color (tuple): Background color (R, G, B)
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.max_value = max_value
        self.current_value = max_value
        self.color = color
        self.bg_color = bg_color
    
    def draw(self, surface):
        """
        Draw the progress bar
        
        Args:
            surface (pygame.Surface): Surface to draw on
        """
        # Draw background
        pygame.draw.rect(surface, self.bg_color, self.rect)
        
        # Draw progress bar
        if self.current_value > 0:
            progress_width = int((self.current_value / self.max_value) * self.rect.width)
            progress_rect = pygame.Rect(self.rect.left, self.rect.top, progress_width, self.rect.height)
            pygame.draw.rect(surface, self.color, progress_rect)
        
        # Draw border
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 1)
    
    def update(self, value):
        """
        Update progress bar value
        
        Args:
            value (float): New value
        """
        self.current_value = max(0, min(value, self.max_value))
