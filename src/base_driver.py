from abc import ABC, abstractmethod
from input_handler import InputHandler

class BaseDriver(ABC):
    """
    Base class for a driving and data logging loop
    
    Implementing classes must implement the abstract method _get_steering
    """
    def __init__(self, car, camera):
        self._car = car
        self._camera = camera
        self._stop_flag = False
        self._iteration = 0
        self._steering_cmd = 0
        self._throttle_cmd = 0
        
        self._input_handler = None
        
    def run(self):
        """Begin Driving Control Loop"""
        self._input_handler = InputHandler()
        try:
            while not self._stop_flag:
                
                    self._set_car_speed()
                    self._car.set_steering(self._steering_cmd)
                    
                    self._steering_cmd = self._get_steering()
                    self._iteration += 1
                    
                    self._log_data()
        finally:
            self._input_handler.restore()
            self._car.set_speed(0)
                     
    @abstractmethod
    def _get_steering(self):
        pass
    
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

    def _set_car_speed(self):
        ON_SPEED = 0 #0.23 is minimum possible that will go forward
        self._throttle_cmd = (ON_SPEED if self._iteration//10 % 3 == 0 else 0.0)
        self._car.set_speed(self._throttle_cmd)

    def force_stop(self, signum=None, frame=None):
        self._stop_flag = True

    def _log_data(self):
        pass  # Optional, override in data collection subclass
            