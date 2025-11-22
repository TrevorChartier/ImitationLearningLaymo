from base_driver import BaseDriver
from input_handler import InputHandler

# Probably want to capture camera frame once and store as instance variable
class InferenceDriver(BaseDriver):
    def __init__(self, car, camera, model):
        super().__init__(car, camera)
        self._model = model
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
