# This file contains a few internal tricks that allow e.g.
# the diodes to always return a motor position dependent signal.
# Best is to ignore most of it ;)


from functools import wraps
import numpy as np


MOTORS = set()


class MotorTricks:
    """
    mixin class that adds two functionalities:

    - each instance is added to a central set MOTORS
    - set/unset methods for the current range

    together these are used to calculate the current intensities for sensors
    """

    def __init__(self):
        MOTORS.add(self)
        self._unset_range()

    def _unset_range(self):
        self._start = self._stop = None

    def _set_range(self, start, stop):
        self._start = start
        self._stop = stop

    @property
    def _active(self):
        return self._start is not None and self._stop is not None



def get_current_intensity():
    """
    calculate the intensity for all sensors from the positions of all active motors
    """
    return np.prod([calc_intensity_for_motor(m) for m in MOTORS if m._active])

def calc_intensity_for_motor(m):
    """
    calculate an intensity from the position of a motor
    """
    return calc_intensity_for_range(m.get(), m._start, m._stop)

def calc_intensity_for_range(current, start, stop):
    """
    calculate an intensity from the current position, start and stop
    """
    center = (start + stop) / 2
    width = abs(stop - start) / 10 #TODO 10!?
    x = (current - center) / width
    return np.exp(-x**2)



def sets_motor_range(func):
    """
    decorator that wraps the generator function func such that it is iterated
    with setting the motor range before the generator is started
    and unsetting it after it is exhausted or has crashed.
    """
    @wraps(func)
    def wrapper(mot, start, stop, *args, **kwargs):
        mot._set_range(start, stop)
        try:
            yield from func(mot, start, stop, *args, **kwargs)
        finally:
            mot._unset_range()
    return wrapper



class ImageGenerator:

    def __init__(self, xdim, ydim):
        """
        generates images by applying a linear shift along the x axis and
        a sinusoidal distortion along the y axis
        """
        self.xdim = xdim
        self.ydim = ydim

        self.count = 0
        self.amplitude = ydim / 10
        self.width = 1 / xdim

        shape = (ydim, xdim)
        self.data = data = np.random.random(shape)
        data[50:55, ::5] *= 20 #TODO


    def __iter__(self):
        return self

    def __next__(self):
        return get_current_image()


    def get_current_image(self):
        self.count += 1
        img = self.data
        for i in range(img.shape[0]):
            img[:, i] = np.roll(img[:, i], self.shift(i, self.count))
        img[:] = np.roll(img, 1, axis=1)
        return img

    def shift(self, x, b):
        """
        calculate the shift needed for the sinusoidal distortion
        """
        res = self.amplitude * np.sin(2*np.pi * self.width * x + b)
        return int(round(res))



