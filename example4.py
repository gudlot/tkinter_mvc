#!/usr/bin/env python3

from matplotlib import pyplot as plt
from toydaq import Motor, Camera, scan_iter


mot = Motor("MY-MOTOR", units="mm")
cam = Camera("MY-CAMERA")

fig = plt.figure()
canvas = fig.canvas

img = cam.get()
pims = plt.imshow(img, interpolation="none")

for _ in scan_iter(mot, 0, 10, 1):
    img = cam.get()
    pims.set_array(img)

    plt.show(block=False)
    canvas.draw()



