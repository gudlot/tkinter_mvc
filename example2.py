#!/usr/bin/env python3

from matplotlib import pyplot as plt
from toydaq import Motor, Diode, scan_iter


mot1 = Motor("MY-LARGE-MOTOR", units="m")
mot2 = Motor("MY-TINY-MOTOR", units="nm")
dio = Diode("MY-DIODE")


x1 = []
y1 = []
for pos in scan_iter(mot1, 0, 10, 1):
    x1.append(pos)
    y1.append(dio.get())

x2 = []
y2 = []
for pos in scan_iter(mot2, 0, 10, 1):
    x2.append(pos)
    y2.append(dio.get())


plt.plot(x1, y1)
plt.plot(x2, y2)
plt.show()



