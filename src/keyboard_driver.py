import time
import cv2
import os

from base_driver import BaseDriver

class KeyboardDriver(BaseDriver):
    def __init__(self, car, camera, data_dir):
        super().__init__(car, camera, data_dir)

    def _get_steering(self):
        key, _ = self._input_handler.get_key()
        if key == "w":
            self.force_stop()
        else:
            return self._get_keyboard_steering_input(key)

    def _log_data(self):
        """Write the current camera frame and steering command."""
        super()._log_data(self._expert_paths)

    

