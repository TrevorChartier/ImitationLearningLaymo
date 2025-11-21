from base_driver import BaseDriver
from input_handler import InputHandler

# Probably want to capture camera frame once and store as instance variable
class InferenceDriver(BaseDriver):
    def __init__(self, car, camera, model):
        super().__init__(car, camera)
        self._model = model
        self._input_handler = InputHandler() # Can refactor this into base class
        self._expert_override = False
    
    def _get_steering(self):
        key, new_press = self._input_handler.get_key()
        if new_press or self._expert_override:
            # Expert is in control
            self._expert_override = True
            if key == "w":
                self.force_stop()
            elif key == "f":
                # Expert gives back control to policy
                self._expert_override = False
            else:
                return self._get_keyboard_steering_input(key)
            
        # If nothing is returned already, policy is in control
        return self._model.predict(False)
            
    def _get_keyboard_steering_input(self, key):
        """ Return a steering command based on a keyboard input """
        if key == "a":
            return max(-1, self._steering_cmd - 0.1)
        elif key == "d":
            return min(1, self._steering_cmd + 0.1)
        elif key =="s":
            return self._shrink_toward_zero(self._steering_cmd)
        else:
            return self._steering_cmd
        
    def _shrink_toward_zero(self, val, step=0.05):
        """Brings val closer to zero by step (default 0.2)."""
        if abs(val) <= step:
            return 0
        return val - step if val > 0 else val + step
    
    def run(self):
        try:
            super().run()
        finally:
            self._input_handler.restore()