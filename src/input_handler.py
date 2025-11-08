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
        """Return the last key pressed, or update it if a new key is pressed."""
        dr, _, _ = select.select([sys.stdin], [], [], 0)
        if dr:
            key = sys.stdin.read(1)
            self.last_key = key
        return self.last_key

    def restore(self):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.orig_settings)
