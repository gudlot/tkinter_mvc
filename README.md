# A Toy DAQ🦆

This package contains a toy data acquisition consisting of a few classes simulating motors, sensors (diodes and cameras) and scanning.

```python
from toydaq import Motor, Diode

mot = Motor("MY-MOTOR", units="mm")
dio = Diode("MY-DIODE")
```

There are three options for performing a scan:

1. Callback

```python
def cb_print():
    print(mot, dio)

scan(mot, 0, 10, 1, cb=cb_print)
```

2. Thread

```python
from time import sleep

st = scan_thread(mot, 0, 10, 1)
while st.is_alive():
    print(mot, dio)
    sleep(0.1)
```

3. Iterator

```python
for pos in scan_iter(mot, 0, 10, 1):
    print(pos, mot, dio)
```

## Setup

Dependencies:
- `numpy`
- `tqdm`

The examples also use `matplotlib`.
