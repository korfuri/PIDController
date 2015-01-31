import time

class PID:
    """PID controller."""

    def __init__(self, Kp, Ki, Kd, origin_time=time.time()):
        # Gains for each term
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

        # Corrections (outputs)
        self.Cp = 0.0
        self.Ci = 0.0
        self.Cd = 0.0

        self.previous_time = origin_time
        self.previous_error = 0.0

    def Update(self, error, time=time.time()):
        dt = time - self.previous_time
        if dt <= 0.0:
            return 0
        de = error - self.previous_error

        self.Cp = self.Kp * error
        self.Ci += error * dt
        self.Cd = de / dt

        self.previous_time = time
        self.previous_error = error

        return (
            self.Cp                # proportional term
            + (self.Ki * self.Ci)  # integral term
            + (self.Kd * self.Cd)  # derivative term
        )
