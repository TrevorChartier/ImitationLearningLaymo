import time
import cv2
import os

from input_handler import InputHandler
from base_driver import BaseDriver

class KeyboardDriver(BaseDriver):
    def __init__(self, car, camera, data_dir):
        super().__init__(car, camera)
        self._data_dir = data_dir
        self._labels_path = os.path.join(self._data_dir, "labels.csv")
        self._img_path = os.path.join(self._data_dir, "images")
        self._setup_data_dir()
        self._input_handler = InputHandler()
        
    def _get_steering(self):
        key = self._input_handler.get_key()
        if key == "w":
            self.force_stop()
        elif key == "a":
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

    def _log_data(self):
        """Write the current camera frame and steering command."""
        timestamp = int(time.time() * 1000)
        throttle_on = 1 if self._throttle_cmd > 0 else 0
        frame = self._camera.get_latest_frame()
        img_filename = f"{timestamp}.jpg"
        cv2.imwrite(os.path.join(self._img_path, img_filename), frame)
        with open(self._labels_path, "a", encoding="utf-8") as f:
            f.write(f"{timestamp}, {throttle_on}, {self._steering_cmd}\n")

    def _setup_data_dir(self):
        """Create empty directory and labels file for data."""
        print(f"Creating data directory at {self._data_dir}")
        os.makedirs(self._img_path, exist_ok=False)

        with open(self._labels_path, "a", encoding="utf-8") as f:
            f.write("timestamp, throttle_on, steering_command\n")
            
    def run(self):
        try:
            super().run()
        finally:
            self._input_handler.restore()
