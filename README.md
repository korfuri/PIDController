# PID Controller

A [proportional-integral-derivative controller (PID
controller)](http://en.wikipedia.org/wiki/PID_controller) is a control
loop feedback mechanism (controller) widely used in industrial control
systems. A PID controller calculates an error value as the difference
between a measured process variable and a desired setpoint. The
controller attempts to minimize the error by adjusting the process
through use of a manipulated variable.

## Python implementation

Several implementations exist, this one is probably not the best.

It is simple, has some unit tests, and it should be easy to use.

Let's say you have a system to control a room's temperature.

```python
def get_room_temperature():
    # use a thermometer
    return t

def set_heater_power(power):
    if power > 10:
       power = 10
    if power < 0:
       power = 0
    # call to the heater's RPC API
```

You can control this system with the following:

```python
import time
import pidcontroller

def keep_room_warm():
    pid = pidcontroller.PID(1.0, 0.5, 0.1)
    target_temperature = 21  # in celsius degrees
    while (True):
      current_temperature = get_room_temperature()
      error = target_temperature - current_temperature
      correction = pid.Update(error)
      print 'Setting the heater to %f' % correction
      set_heater_power(correction)
      time.sleep(60)
```

## A note on the gains (Kp, Ki, Kd)

Each problem requires different gains. The gains in the example above
are arbitrary and probably wrong for most heaters. The [Wikipedia
page](http://en.wikipedia.org/wiki/PID_controller) has information on
how to tune the gains of a PID controller.
