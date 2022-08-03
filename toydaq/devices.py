from random import random
from time import sleep

from tqdm import tqdm
import numpy as np

from .tricks import MotorTricks, get_current_intensity, ImageGenerator


class Named:

    def __repr__(self):
        tn = type(self).__name__
        n = repr(self.name)
        val = self.get()
        return f"{tn} {n} at {val}"



class Motor(Named, MotorTricks):

    def __init__(self, name, units=None):
        super().__init__()
        self.name = name
        self.units = units
        self._value = 0

    def __repr__(self):
        res = super().__repr__()
        return f"{res} {self.units}"

    def get(self):
        """
        Get the current position of the motor
        """
        jitter = random() / 10 #TODO: how much jitter?
        return self._value + jitter


    def set(self, value, show_progress=False):
        """
        Set the target position of the motor
        a tqdm progress bar can be enabled by setting show_progress to True
        """
        start = self._value
        if start == value:
            return

        vals = np.linspace(start, value, 10) #TODO: number of steps?

        if show_progress:
            vals = tqdm(vals)

        for x in vals:
            self._value = x
#            sleep(0.1) #TODO: uncomment



class Sensor(Named):

    def __init__(self, name):
        self.name = name



class Diode(Sensor):

    def get(self):
        """
        Get the current signal from the diode
        """
        return get_current_intensity()



class Camera(Sensor):

    def __init__(self, name):
        super().__init__(name)
        self._ig = ImageGenerator(100, 100) #TODO: size?

    def get(self):
        """
        Get the current image from the camera
        """
        img = self._ig.get_current_image()
        return get_current_intensity() * img



