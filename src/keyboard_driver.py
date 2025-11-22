import time
import cv2
import os


from base_driver import BaseDriver

class KeyboardDriver(BaseDriver):
    def __init__(self, car, camera, data_dir):
        super().__init__(car, camera)
        self._data_dir = data_dir
        self._labels_path = os.path.join(self._data_dir, "labels.csv")
        self._img_path = os.path.join(self._data_dir, "images")
        self._setup_data_dir()

        
    def _get_steering(self):
        key, _ = self._input_handler.get_key()
        if key == "w":
            self.force_stop()
        else:
            return self._get_keyboard_steering_input(key)


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

