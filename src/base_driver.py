from abc import ABC, abstractmethod
import os
import cv2
import time
from collections import deque

from input_handler import InputHandler
from buffer import Buffer

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
        
        self._steering_buffer = Buffer(100)
        
        self._THROTTLE_STEP_LEN = 15 # How many iterations in a cycle
        self._THROTTLE_CYCLE = 4 # How many cycles in period. Throttle is on for one of the cycles in period
        self._THROTTLE_PERIOD = self._THROTTLE_CYCLE * self._THROTTLE_STEP_LEN
        
        expert_dir = os.path.join(data_dir, "expert")
        self._expert_paths = {
            "labels": os.path.join(expert_dir, "labels.csv"),
            "images": os.path.join(expert_dir, "images")
        }
        self._setup_data_dir()
        
    def run(self):
        """Begin Driving Control Loop"""
        self._input_handler = InputHandler()
        start_time = time.time()
        try:
            while not self._stop_flag:
                    self._latest_camera_frame = self._camera.get_latest_frame()
                    self._set_car_speed()
                    self._car.set_steering(self._steering_cmd)
                    
                    self._steering_cmd = self._get_steering()
                    if self._iteration % 2 == 0:
                        self._log_data()
                    self._steering_buffer.add(self._steering_cmd)
                    self._iteration += 1        
        finally:
            duration = time.time() - start_time
            self._input_handler.restore()
            self._car.set_speed(0)
            print("Control Frequency: ", round(self._iteration / (duration)), "hz")
                     
    @abstractmethod
    def _get_steering(self) -> float:
        pass
    
    def _get_keyboard_steering_input(self, key: str) -> float:
        """ Return a steering command based on a keyboard input """
        if key == "a":
            return -1
        elif key == "d":
            return 1
        elif key =="s":
            return 0
        else:
            return self._steering_cmd
        
    def _shrink_toward_zero(self, val: float, step=0.05) -> float:
        """Brings val closer to zero by step (default 0.2)."""
        if abs(val) <= step:
            return 0
        return val - step if val > 0 else val + step

    def _set_car_speed(self):
        ON_SPEED = 0.25 #0.23 is minimum possible that will go forward
        self._throttle_cmd = (ON_SPEED if self._iteration//self._THROTTLE_STEP_LEN % self._THROTTLE_CYCLE == 0 else 0.0)
        self._car.set_speed(self._throttle_cmd)

    def force_stop(self, signum=None, frame=None):
        self._stop_flag = True

    def _log_data(self, output_paths: dict):
        """Write the current camera frame and steering command."""
        timestamp = int(time.time() * 1000)
        
        steering_lookback = self._steering_buffer.get()
        steering_lookback_str = ";".join(map(str, steering_lookback))
        
        throttle_pulse_idx = self._iteration % self._THROTTLE_PERIOD
        
        img_filename = f"{timestamp}.jpg"
        cv2.imwrite(os.path.join(output_paths["images"], img_filename), self._latest_camera_frame)
        with open(output_paths["labels"], "a", encoding="utf-8") as f:
            f.write(f"{timestamp}\t{steering_lookback_str}\t{throttle_pulse_idx}\t{self._steering_cmd}\n")
    
    def _setup_data_dir(self):
        """Create empty directory and labels file for data."""
        os.makedirs(self._expert_paths["images"], exist_ok=False)
        with open(self._expert_paths["labels"], "a", encoding="utf-8") as f:
            f.write("timestamp\tsteering_lookback\tthrottle_pulse_idx\tsteering_command\n")
            