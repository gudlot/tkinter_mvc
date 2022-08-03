# Problem

At SLS, users want to measure data in "scans", i.e., the measurement alternates between moving a motor and reading some sensors (diodes or cameras). The step-wise motor movement has a defined start and stop, and a step size. The sensors are recorded one read-out per step. The result would be a plot of each sensor's readings (y axis) as function of the motor position (x axis).

## Use the toy DAQ to write a GUI that performs a 1D scan

- Allow the user to select one motor

- Allow the user to select N diodes

- Show the signals of the N diodes as function of the motor position

  (at least after the scan, but preferably live updating)

You have **free choice of tools** you use. For instance, the resulting GUI could be a web app, a jupyter notebook or written in a desktop GUI toolkit, etc.

During your subsequent interview, we will talk about the resulting app from a user's point of view and about the code from a developer's point of view. We will also talk about your experimentation and design processes. If you choose to version your code, e.g., in git, the commit history could be useful as a means to follow theses processes.

## Setup

The [dependencies](README.md#setup) should be easily available via conda, pip or the package manager in case your OS has one. How you obtain the libraries is also your choice.

## The devices existing at your toy beamline are as follows:

- Three motors:

  ```python
  mot1 = Motor("MY-LARGE-MOTOR",  units="m")
  mot2 = Motor("MY-TINY-MOTOR",   units="nm")
  mot3 = Motor("MY-NORMAL-MOTOR", units="mm")
  ```

- Three diodes:

  ```python
  dio1 = Diode("INTENSITY")
  dio2 = Diode("COUNTER")
  dio3 = Diode("SIGNAL")
  ```

## Advanced challenges:

Please regard these as fully optional.

- Visualize a camera instead of a diode
- Visualize the overall system status
- Visualize progress (e.g., how long until done) during the scan
- Progress updates via other channels (browser/SMS/email/...)

Feel free to just write down some ideas on these points: what/which might be more/less useful? how would you go about implementing them into your solution for the main problem?
