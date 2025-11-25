import signal
import time
from datetime import datetime
from pathlib import Path

from typing import Callable

from laymo.car import Car
from laymo.camera_manager import CameraManager

from base_driver import BaseDriver


def run_driver(driver_cls: BaseDriver, model_args: list, instructions_fn: Callable[[], None]):
    # PCA9685 pins
    THROTTLE_PIN = 0
    STEERING_PIN = 1

    # Initialize the car and camera manager
    laymo = Car(STEERING_PIN, THROTTLE_PIN)
    cam = CameraManager()
    
    driver = driver_cls(laymo, cam, *model_args, _get_data_dir(len(model_args)))

    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
        signal.signal(sig, driver.force_stop)

    instructions_fn()
    _await_ready()
    time.sleep(0.5)
    driver.run()


def _get_data_dir(num_model) -> str:
    """Return the directory to the data folder relative to this script"""
    parent_dir = Path(__file__).parent.parent
    date_dir = datetime.now().strftime("%b_%d_%Y")
    
    DAgger = ""
    if num_model > 0:
        DAgger = "dagger_" # Trials run with a policy should indicate it in their name
        

    data_dir_name = DAgger + "trial_" + datetime.now().strftime("%I:%M:%S_%p")
    full_data_dir = parent_dir / "data" / "trials" / date_dir / data_dir_name
    print (str(full_data_dir))
    return str(full_data_dir)


def print_rc_instructions():
    print("\n\nWelcome to Laymo RC Data Collection!")
    print("During your run, press the 'a' key to go left and the 'd' key to go right")
    print("Stop the car and data collection at any point by pressing 'w'")


def print_inference_instructions():
    print("\n\nWelcome to Laymo RC Inference Time!")
    print("Take over at any point using the keyboard")
    print("Press the 'a' key to go left, the 's' key to go straight and the 'd' key to go right")
    print("Return control to autonomous mode using the 'f' key")
    print("Stop the car and data collection at any point by pressing 'w'")


def _await_ready():
    ready = False
    while not ready:
        ready = input("Press 'r' to begin the run.\n") == 'r' 
    print("Beginning Run")
    
    
