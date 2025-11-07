"""This module defines a script to collect data for behavior cloning.

It allows for teleoperation (RC control) of the Laymo car while recording camera frames
and the associated teleoperation inputs. 

To Use:
python rc_data_collection.py

Follow the on-screen instructions. 
Press 'r' to begin (Warning, the car will begin moving at a constant speed)
Use 'a' to move left and 'd' to move right.

Data is written to csv files within the directory data/
"""
