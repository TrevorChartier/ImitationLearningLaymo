"""This module defines a script to collect data for behavior cloning.

It allows for teleoperation (RC control) of the Laymo car while recording camera frames
and the associated teleoperation inputs. 
"""
import os
import time

import cv2
import keyboard

from laymo.car import Car
from laymo.camera_manager import CameraManager

from input_handler import InputHandler

class DataCollector:
    def __init__(self, car, camera, data_dir):
        self.__car = car
        self.__camera = camera
        self.__data_dir = data_dir
        self.__stop_flag = False
        self.__iteration = 0
        self.__steering_cmd = 0

        self.__labels_path = os.path.join(self.__data_dir, "labels.csv")
        self.__img_path = os.path.join(self.__data_dir, "images")
        self.__setup_data_dir()

    def run(self):
        """Main control and data collection loop."""
        input_handler = InputHandler()
        try:
            while not self.__stop_flag:
                self.__set_car_speed()
                self.__car.set_steering(self.__steering_cmd)
                print(self.__steering_cmd)

                key = input_handler.get_key()
                if key == "w":
                    self.force_stop()
                elif key == "a":
                    self.__steering_cmd = max(-1, self.__steering_cmd - 0.1)
                elif key == "d":
                    self.__steering_cmd = min(1, self.__steering_cmd + 0.1)
                elif key =="s":
                    self.__steering_cmd = self.__shrink_toward_zero(self.__steering_cmd)

                self.__log_data()
                self.__iteration += 1
        finally:
            input_handler.restore()
            self.__car.set_speed(0)


    def force_stop(self, signum=None, frame=None):
        """Stop the car by setting flag. Useful for signal handlers."""
        self.__stop_flag = True

    def __setup_data_dir(self):
        """Create empty directory and labels file for data."""
        print(f"Creating data directory at {self.__data_dir}")
        os.makedirs(self.__img_path, exist_ok=False)

        with open(self.__labels_path, "a", encoding="utf-8") as f:
            f.write("timestamp, steering_command\n")

    def __shrink_toward_zero(self, val, step=0.05):
        """Brings val closer to zero by step (default 0.2)."""
        if abs(val) <= step:
            return 0
        return val - step if val > 0 else val + step

    def __set_car_speed(self):
        """Manually pulses the throttle on and off."""
        self.__car.set_speed(0.23 if self.__iteration//10 % 3 == 0 else 0.0)

    def __log_data(self):
        """Write the current camera frame and steering command."""
        timestamp = int(time.time() * 1000)
        frame = self.__camera.get_latest_frame()
        img_filename = f"{timestamp}.jpg"
        cv2.imwrite(os.path.join(self.__img_path, img_filename), frame)
        with open(self.__labels_path, "a", encoding="utf-8") as f:
            f.write(f"{timestamp}, {self.__steering_cmd}\n")
