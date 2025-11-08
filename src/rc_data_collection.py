"""This module defines a script to collect data for behavior cloning.

It allows for teleoperation (RC control) of the Laymo car while recording camera frames
and the associated teleoperation inputs. 

To Use:
python rc_data_collection.py

Follow the on-screen instructions. 
Press 'r' to begin (Warning, the car will begin moving at a constant speed)
Use 'a' to move left and 'd' to move right.

Data is written to folders within the directory data/ at the root of the repo
"""
from datetime import datetime
import signal

from pathlib import Path
import time

from laymo.car import Car
from laymo.camera_manager import CameraManager
from data_collector import DataCollector


def get_data_dir() -> str:
    """Return the directory to the data folder relative to this script"""
    parent_dir = Path(__file__).parent.parent
    data_dir_name = "trial_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    full_data_dir = parent_dir / "data" / data_dir_name
    return str(full_data_dir)

def print_instructions():
    print("\n\nWelcome to Laymo RC Data Collection!")
    print("During your run, press the 'a' key to go left and the 'd' key to go right")
    print("Stop the car and data collection at any point by pressing 's'")
    
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
    data_collector = DataCollector(laymo, cam, get_data_dir())

    # Set signal handlers in case of ^C or program failure, car stops
    # for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
    #     signal.signal(sig, data_collector.force_stop)

    print_instructions()
    time.sleep(0.5)
    data_collector.run()
