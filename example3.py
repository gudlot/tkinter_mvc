#!/usr/bin/env python3

from matplotlib import pyplot as plt
from toydaq import Motor, Diode, scan_iter


mot1 = Motor("MY-LARGE-MOTOR", units="m")
mot2 = Motor("MY-TINY-MOTOR", units="nm")
dio = Diode("MY-DIODE")


img = []
for pos1 in scan_iter(mot1, 0, 20, 1, show_progress=True):
    line = []
    for pos2 in scan_iter(mot2, 0, 20, 1, show_progress=True):
        line.append(dio.get())
    img.append(line)


plt.imshow(img)
plt.show()



