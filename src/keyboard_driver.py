from laymo.car import Car
from laymo.camera_manager import CameraManager

from base_driver import BaseDriver

class KeyboardDriver(BaseDriver):
    def __init__(self, car: Car, camera: CameraManager, data_dir: str):
        super().__init__(car, camera, data_dir)

    def _get_steering(self) -> float:
        key, _ = self._input_handler.get_key()
        if key == "w":
            self.force_stop()
        else:
            return self._get_keyboard_steering_input(key)

    def _log_data(self):
        """Write the current camera frame and steering command."""
        super()._log_data(self._expert_paths)

    

