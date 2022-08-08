from toydaq import Motor, Diode, Camera, scan_iter


import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import *

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import cm

from matplotlib import pyplot as plt
#from threading import Thread
from tqdm import tqdm
import numpy as np
 
class Model():
    """ The model for our beamline. It contains our hardware, i.e. diodes, cameras, motors."""
    
    # Configuration of our beamline. Ex[ected parameters for the hardware.
    valid_units = ["m", "nm", "mm"]
    valid_diode_names=["INTENSITY", "COUNTER", "SIGNAL", "XRF"]
    valid_camera_names=["MY-CAMERA"]
    
    def __init__(self):
        """
        Make motors, diodes, cameras available in the model with their methods and attributes.
        better in the future: load from a config file
        """
        self.motors = {}
        self.diodes = {}
        self.cameras = {}

    def _check_valid_units(self, units):
        """
        Ensure the user has provided a valid unit name
        """
        if units not in self.valid_units:
            options = ", ".join(self.valid_units)
            raise ValueError(f"{units} is not a known unit type. Options are {options}")

    def add_motor(self, name, units):
        """
        Add a motor to the model
        """
        if name in self.motors:
            raise ValueError(
                f"Motor names must be unique: {name} is already a defined motor."
            )

        # Allow any casing
        units = units.lower()
        self._check_valid_units(units)
        print(f"Adding motor {name} with units {units}")
        self.motors[name] = Motor(name, units)

    def _check_valid_diode_names(self, diode_name):
        """
        Ensure the user has provided a valid diode name
        """   
        if diode_name not in self.valid_diode_names:
            options = ", ".join(self.valid_diode_names)
            raise ValueError(f"{diode_name} is not a known sensor diode name. Options are {options}")

    def add_diode(self, diode_name):
        """
        Add a diode to the model
        """
        if diode_name in self.diodes:
            raise ValueError(
                f"Diode names must be unique: {diode_name} is already a defined diode."
            )
        
        self._check_valid_diode_names(diode_name)
        print(f"Adding diode {diode_name}")
        self.diodes[diode_name]=Diode(diode_name)

    def _check_valid_camera_names(self, camera_name):
        """
        Ensure the user has provided a valid camera name
        """   
        if camera_name not in self.valid_camera_names:
            options = ", ".join(self.valid_camera_names)
            raise ValueError(f"{camera_name} is not a known sensor diode name. Options are {options}")


    def add_camera(self, camera_name):
        """Add a camera to the model"""

        if camera_name in self.cameras:
            raise ValueError(f"Camera names must be unique: {camera_name} is already a defined camera.")
        self._check_valid_camera_names(camera_name)
        print(f"Adding camera {camera_name}")
        self.cameras[camera_name]=Camera(camera_name)

  
    def diode_names(self):
        """ Return names of all available diodes """
        return [self.diodes[label].name for label in self.diodes]

    def motor_names(self):
        """ Return names of all available motors """
        return [self.motors[label].name for label in self.motors]

    def camera_names(self):
        """ Return names of all available cameras """
        return [self.cameras[label].name for label in self.cameras]