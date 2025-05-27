"""
Menu View
---------
Defines the Menu class for the WebStore application UI.
"""

from blessed import Terminal
import time

class Menu:
    def __init__(self, title, options):
        self.term = Terminal()
        self.title = title
        self.options = options
        self.current_option = 0
    
    def display(self):
        with self.term.fullscreen(), self.term.cbreak(), self.term.hidden_cursor():
            while True:
                print(self.term.clear)
                print(self.term.move_y(2) + self.term.center(self.term.bold(self.title)))
                print()
                
                # Display menu options with proper spacing
                for i, option in enumerate(self.options):
                    if i == self.current_option:
                        # Orange background with black text for selected option
                        print(self.term.center(self.term.black_on_orange(f" {option} ")))
                    else:
                        print(self.term.center(f" {option} "))
                
                print()
                print(self.term.center("(Use ↑/↓ arrow keys, j/k, or w/s to navigate, Enter to select, q to quit)"))
                
                # Handle keyboard input with improved key detection for multiple environments
                key = self.term.inkey(timeout=0.5)
                
                # Enhanced multi-key support for better compatibility across platforms and terminals
                if (key.name == 'KEY_UP' or key.code == 259 or key == 'k' or key == 'K' or 
                    key == 'w' or key == 'W' or key.code == 65 or key.code == 450):
                    self.current_option = (self.current_option - 1) % len(self.options)
                elif (key.name == 'KEY_DOWN' or key.code == 258 or key == 'j' or key == 'J' or 
                      key == 's' or key == 'S' or key.code == 66 or key.code == 456):
                    self.current_option = (self.current_option + 1) % len(self.options)
                elif (key.name == 'KEY_ENTER' or key == '\n' or key == '\r' or 
                      key.code == 10 or key.code == 13 or key == ' '):
                    return self.current_option
                elif key.lower() == 'q' or key.name == 'KEY_ESCAPE' or key.code == 27:
                    return None
                
                # Small delay to prevent cpu usage spikes
                time.sleep(0.05)

    @staticmethod
    def get_centered_input(term, prompt_text):
        """Get input with centered prompt"""
        # Calculate centering
        width = term.width
        prompt_length = len(prompt_text) + 20  # Add some padding for input
        left_padding = (width - prompt_length) // 2
        
        # Create centered prompt
        print(term.move_x(left_padding) + prompt_text + " ", end="")
        
        # Get input
        user_input = input()
        return user_input
