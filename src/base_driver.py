from abc import ABC, abstractmethod
import os
import cv2
import time
from input_handler import InputHandler

from laymo.car import Car
from laymo.camera_manager import CameraManager

class BaseDriver(ABC):
    """
    Base class for a driving and data logging loop
    
    Implementing classes must implement the abstract method _get_steering
    """
    def __init__(self, car: Car, camera: CameraManager, data_dir: str):
        self._car = car
        self._camera = camera
        self._stop_flag = False
        self._iteration = 0
        self._steering_cmd = 0
        self._throttle_cmd = 0
        self._input_handler = None # Only initialize this once run is called
        self._latest_camera_frame = None
        
        expert_dir = os.path.join(data_dir, "expert")
        self._expert_paths = {
            "labels": os.path.join(expert_dir, "labels.csv"),
            "images": os.path.join(expert_dir, "images")
        }
        self._setup_data_dir()
        
    def run(self):
        """Begin Driving Control Loop"""
        self._input_handler = InputHandler()
        try:
            while not self._stop_flag:
                    self._latest_camera_frame = self._camera.get_latest_frame()
                    self._set_car_speed()
                    self._car.set_steering(self._steering_cmd)
                    
                    self._steering_cmd = self._get_steering()
                    self._iteration += 1
                    
                    self._log_data()
        finally:
            self._input_handler.restore()
            self._car.set_speed(0)
                     
    @abstractmethod
    def _get_steering(self) -> float:
        pass
    
    def _get_keyboard_steering_input(self, key: str) -> float:
        """ Return a steering command based on a keyboard input """
        if key == "a":
            return max(-1, self._steering_cmd - 0.1)
        elif key == "d":
            return min(1, self._steering_cmd + 0.1)
        elif key =="s":
            return self._shrink_toward_zero(self._steering_cmd)
        else:
            return self._steering_cmd
        
    def _shrink_toward_zero(self, val: float, step=0.05) -> float:
        """Brings val closer to zero by step (default 0.2)."""
        if abs(val) <= step:
            return 0
        return val - step if val > 0 else val + step

    def _set_car_speed(self):
        ON_SPEED = 0 #0.23 is minimum possible that will go forward
        self._throttle_cmd = (ON_SPEED if self._iteration//10 % 3 == 0 else 0.0)
        self._car.set_speed(self._throttle_cmd)

    def force_stop(self, signum=None, frame=None):
        self._stop_flag = True

    def _log_data(self, output_paths: dict):
        """Write the current camera frame and steering command."""
        timestamp = int(time.time() * 1000)
        throttle_on = 1 if self._throttle_cmd > 0 else 0
        
        img_filename = f"{timestamp}.jpg"
        cv2.imwrite(os.path.join(output_paths["images"], img_filename), self._latest_camera_frame)
        with open(output_paths["labels"], "a", encoding="utf-8") as f:
            f.write(f"{timestamp}, {throttle_on}, {self._steering_cmd}\n")
    
    def _setup_data_dir(self):
        """Create empty directory and labels file for data."""
        os.makedirs(self._expert_paths["images"], exist_ok=False)
        with open(self._expert_paths["labels"], "a", encoding="utf-8") as f:
            f.write("timestamp, throttle_on, steering_command\n")
            