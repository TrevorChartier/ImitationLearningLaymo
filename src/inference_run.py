from datetime import datetime
import signal

from pathlib import Path
import time

from laymo.car import Car
from laymo.camera_manager import CameraManager
from inference_driver import InferenceDriver
from model import Model


def get_data_dir() -> str:
    """Return the directory to the data folder relative to this script"""
    parent_dir = Path(__file__).parent.parent
    date_dir = datetime.now().strftime("%b_%d_%Y")
    data_dir_name = "trial_" + datetime.now().strftime("%I:%M:%S_%p")
    full_data_dir = parent_dir / "data" / "trials" / date_dir / data_dir_name
    print (str(full_data_dir))
    return str(full_data_dir)

def print_instructions():
    print("\n\nWelcome to Laymo RC Inference Time!")
    print("Take over at any point using the keyboard")
    print("Press the 'a' key to go left, the 's' key to go straight and the 'd' key to go right")
    print("Return control to autonomous mode using the 'f' key")
    print("Stop the car and data collection at any point by pressing 'w'")
    
    ready = False
    while not ready:
        ready = input("Press 'r' to begin the run.") == 'r'
        
    print("Beginning Run")

if __name__ == "__main__":
    # PCA9685 pins
    THROTTLE_PIN = 0
    STEERING_PIN = 1

    # Initialize the car and camera manager
    laymo = Car(STEERING_PIN, THROTTLE_PIN)
    cam = CameraManager()
    model = Model()
    data_collector = InferenceDriver(laymo, cam, model, get_data_dir())

    # Set signal handlers in case of ^C or program failure, car stops
    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
        signal.signal(sig, data_collector.force_stop)

    print_instructions()
    time.sleep(0.5)
    data_collector.run()