from abc import ABC, abstractmethod
import time

class BaseDriver(ABC):
    def __init__(self, car, camera):
        self.__car = car
        self.__camera = camera
        self.__stop_flag = False
        self.__iteration = 0
        self.__steering_cmd = 0
        
    def run(self):
        """Begin Driving Control Loop"""
        while not self.__stop_flag:
            try:
                self.__set_car_speed()
                self.__car.set_steering(self.__steering_cmd)
                
                self.__steering_cmd = self.__get_steering()
            finally:
                self.__car.set_speed(0)
                
    @abstractmethod
    def __get_steering(self):
        pass

    def __set_car_speed(self):
        self.__car.set_speed(0.23 if self.__iteration//10 % 3 == 0 else 0.0)

    def force_stop(self):
        self._stop_flag = True

    def __log_data(self):
        pass  # Optional, override in data collection subclass
            