"""
Login and registration screen
"""
import pygame
from config import *
from UI import Button, InputBox, MessageBox
from database import Database


class LoginScreen:
    def __init__(self, screen):
        self.screen = screen
        self.db = Database()
        
        # Fonts
        self.title_font = pygame.font.Font(None, 72)
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # UI Components
        center_x = SCREEN_WIDTH // 2
        
        self.username_input = InputBox(center_x - 150, 200, 300, 40, "Username")
        self.password_input = InputBox(center_x - 150, 260, 300, 40, "Password", password=True)
        
        self.login_button = Button(center_x - 100, 330, 200, 50, "Login")
        self.register_button = Button(center_x - 100, 390, 200, 50, "Register", GREEN)
        self.exit_button = Button(center_x - 100, 450, 200, 50, "Exit", RED)
        
        self.message_box = MessageBox(center_x - 150, 520, 300, 40)
        
        self.current_user_id = None
        self.current_username = None
        self.running = True
    
    def handle_events(self, events):
        """Handle login screen events"""
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                return "quit"

            # If logged in, check start button
            if self.current_user_id:
                start_button = Button(SCREEN_WIDTH // 2 - 100, 350, 200, 50, "Start Game", GREEN)
                if start_button.handle_event(event):
                    return "start_game"

            # Input boxes (only when not logged in)
            if not self.current_user_id:
                if self.username_input.handle_event(event):
                    self.password_input.active = True
                    self.password_input.color = BLUE

                if self.password_input.handle_event(event):
                    self.attempt_login()

                # Buttons
                if self.login_button.handle_event(event):
                    self.attempt_login()

                if self.register_button.handle_event(event):
                    self.attempt_register()

            if self.exit_button.handle_event(event):
                self.running = False
                return "quit"

        return None
    
    def attempt_login(self):
        """Try to log in with provided credentials"""
        username = self.username_input.get_text()
        password = self.password_input.get_text()
        
        if not username or not password:
            self.message_box.show("Please fill in all fields", RED)
            return
        
        user_id = self.db.login_user(username, password)
        
        if user_id:
            self.current_user_id = user_id
            self.current_username = username
            self.message_box.show("Login successful!", GREEN)
        else:
            self.message_box.show("Invalid credentials", RED)
            self.password_input.clear()
    
    def attempt_register(self):
        """Try to register a new user"""
        username = self.username_input.get_text()
        password = self.password_input.get_text()
        
        success, message = self.db.register_user(username, password)
        
        if success:
            self.message_box.show(message, GREEN)
            self.username_input.clear()
            self.password_input.clear()
        else:
            self.message_box.show(message, RED)
    
    def draw(self):
        """Draw the login screen"""
        self.screen.fill(WHITE)
        
        # Title
        title = self.title_font.render("Platform Game", True, BLUE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        # If logged in, show user info
        if self.current_user_id:
            self.draw_user_info()
        else:
            # Input boxes
            self.username_input.draw(self.screen, self.font)
            self.password_input.draw(self.screen, self.font)
            
            # Buttons
            self.login_button.draw(self.screen, self.font)
            self.register_button.draw(self.screen, self.font)
        
        self.exit_button.draw(self.screen, self.font)
        
        # Message box
        self.message_box.update()
        self.message_box.draw(self.screen, self.small_font)
    
    def draw_user_info(self):
        """Draw user information and high scores"""
        center_x = SCREEN_WIDTH // 2

        # Welcome message
        welcome = self.font.render(f"Welcome, {self.current_username}!", True, BLACK)
        welcome_rect = welcome.get_rect(center=(center_x, 200))
        self.screen.blit(welcome, welcome_rect)

        # User high score
        user_high = self.db.get_user_high_score(self.current_user_id)
        user_score_text = self.small_font.render(f"Your High Score: {user_high}", True, BLACK)
        user_score_rect = user_score_text.get_rect(center=(center_x, 250))
        self.screen.blit(user_score_text, user_score_rect)

        # Global high score
        global_high, top_player = self.db.get_global_high_score()
        global_text = self.small_font.render(f"Global High Score: {global_high} by {top_player}", True, BLACK)
        global_rect = global_text.get_rect(center=(center_x, 290))
        self.screen.blit(global_text, global_rect)

        # Start button
        start_button = Button(center_x - 100, 350, 200, 50, "Start Game", GREEN)
        start_button.is_hovered = start_button.rect.collidepoint(pygame.mouse.get_pos())
        start_button.draw(self.screen, self.font)
    
    def run(self):
        """Main login screen loop"""
        clock = pygame.time.Clock()

        while self.running:
            # Get all events once
            events = pygame.event.get()

            # Handle events
            result = self.handle_events(events)

            if result == "quit":
                return None, None
            elif result == "start_game":
                return self.current_user_id, self.current_username

            self.draw()

            pygame.display.flip()
            clock.tick(FPS)

        return None, None