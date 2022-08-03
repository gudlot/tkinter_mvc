#!/usr/bin/env python3

from toydaq import Motor, Diode, scan, scan_iter, scan_thread

mot = Motor("MY-LARGE-MOTOR", units="m")
dio = Diode("MY-DIODE")


# example 1 -- callback
def cb_print():
    print(mot, dio)

scan(mot, 0, 10, 1, cb=cb_print)


# example 2 -- thread
from time import sleep

st = scan_thread(mot, 0, 10, 1)
while st.is_alive():
    print(mot, dio)
    sleep(0.1)


# example 3 -- iterator
for pos in scan_iter(mot, 0, 10, 1):
    print(pos, mot, dio)



