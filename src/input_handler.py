import sys
import select
import termios
import tty

class InputHandler:
    """Non-blocking terminal key reader that remembers the last key pressed."""
    def __init__(self):
        self.orig_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin)  # raw mode
        self.last_key = None

    def get_key(self):
        """
        Return the last key pressed, or update it if a new key is pressed.
        Also returns a boolean indicating whether a new key was pressed.
        """
        readable, _, _ = select.select([sys.stdin], [], [], 0)
        if readable:
            key_pressed = True
            key = sys.stdin.read(1)
            self.last_key = key
        else:
            key_pressed = False
        return self.last_key, key_pressed

    def restore(self):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.orig_settings)
