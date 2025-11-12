"""
UI components for the game
"""
import pygame
from config import *


class Button:
    """Simple button class"""
    def __init__(self, x, y, width, height, text, color=BLUE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = (min(color[0] + 30, 255), min(color[1] + 30, 255), min(color[2] + 30, 255))
        self.is_hovered = False

    def draw(self, surface, font):
        """Draw the button"""
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)

        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        """Handle mouse events"""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class InputBox:
    """Text input box"""
    def __init__(self, x, y, width, height, placeholder='', password=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = GRAY
        self.text = ''
        self.placeholder = placeholder
        self.active = False
        self.password = password

    def handle_event(self, event):
        """Handle input events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = WHITE if self.active else GRAY

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                return True
            else:
                self.text += event.unicode
        return False

    def get_text(self):
        """Get the current text"""
        return self.text

    def clear(self):
        """Clear the text"""
        self.text = ''

    def draw(self, surface, font):
        """Draw the input box"""
        # Draw filled background
        background_color = (40, 40, 40) if self.active else (20, 20, 20)
        pygame.draw.rect(surface, background_color, self.rect)
        # Draw border
        pygame.draw.rect(surface, self.color, self.rect, 2)

        # Display asterisks if password field
        if self.password and self.text:
            display_text = '*' * len(self.text)
        else:
            display_text = self.text if self.text else self.placeholder

        text_color = WHITE if self.text else GRAY
        text_surface = font.render(display_text, True, text_color)
        surface.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))


class MessageBox:
    """Simple message box for displaying messages"""
    def __init__(self, x, y, width, height, message='', color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.message = message
        self.color = color
        self.visible = False

    def set_message(self, message, color=WHITE):
        """Set a new message and make visible"""
        self.message = message
        self.color = color
        self.visible = True

    def show(self, message, color=WHITE):
        """Show a message (alias for set_message)"""
        self.set_message(message, color)

    def hide(self):
        """Hide the message box"""
        self.visible = False

    def update(self):
        """Update the message box (placeholder for future animation)"""
        pass

    def draw(self, surface, font):
        """Draw the message"""
        if self.visible and self.message:
            text_surface = font.render(self.message, True, self.color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)
