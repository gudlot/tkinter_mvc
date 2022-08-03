from threading import Thread

from tqdm import tqdm
import numpy as np

from .tricks import sets_motor_range


SCAN_DOCS = """
    scans motor mot from start to stop doing steps of step
    supplied callback function cb is called after each motor change
    a tqdm progress bar can be enabled by setting show_progress to True
"""


def scan_thread(mot, start, stop, step, cb=None, show_progress=False):
    """
    Scan Thread
    """
    args = (mot, start, stop, step)
    kwargs = dict(cb=cb, show_progress=show_progress)
    t = Thread(target=scan, args=args, kwargs=kwargs)
    t.start()
    return t


def scan(mot, start, stop, step, cb=None, show_progress=False):
    """
    Scan Function
    """
    return [rb for rb in scan_iter(mot, start, stop, step, cb=cb, show_progress=show_progress)]


@sets_motor_range
def scan_iter(mot, start, stop, step, cb=None, show_progress=False):
    """
    Scan Iterator
    """
    total_range = stop - start
    nsteps = int(round(total_range / step))
    vals = np.linspace(start, stop, nsteps)

#    print(start, stop, step, "->", total_range, nsteps)
#    print(vals)

    if show_progress:
        vals = tqdm(vals)

    for x in vals:
        mot.set(x)
        if cb is not None:
            cb()
        yield mot.get()

    if show_progress:
        print()



# attach the generic docstring to each of the individual scan methods
for f in (scan_thread, scan, scan_iter):
    f.__doc__ += SCAN_DOCS



