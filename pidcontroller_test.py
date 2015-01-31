import pidcontroller
import unittest

current_time = 0

def time(increment=1):
    global current_time
    current_time += increment
    return current_time

class Model(object):
    """Base class for models that evolve based on a correction input, and
    have a target state."""
    def __init__(self, state=0.0, correction=0.0, target_state=0.0):
        self.state = state
        self.target_state = target_state
        self.correction = correction
        self.history = []
    
    def SetCorrection(self, correction):
        self.correction = correction

    def SetTargetState(self, target_state):
        self.target_state = target_state

    def State(self):
        return self.state

    def Error(self):
        return self.target_state - self.state

    def Update(self):
        correction = self.correction
        self.ApplyUpdate()
        self.history.append({'correction': correction,
                             'state': self.state})

    def DumpHistory(self):
        for h in self.history:
            print 'Correction: %(correction)f, new state: %(state)f' % h

class TestPID(unittest.TestCase):
    def testTargetState(self):
        """A system in the desired state should not have any correction."""
        pid = pidcontroller.PID(1.0, 1.0, 1.0, time())
        error = 0.0
        correction = pid.Update(error, time())
        self.assertAlmostEqual(correction, 0.0)

    def testConvergenceWithImmediateResponse(self):
        """Test convergence with a model who reacts instantly to a correction."""

        class InstantModel(Model):
            def ApplyUpdate(self):
                self.state += self.correction

        pid = pidcontroller.PID(1.0, 0.5, 0.1, time())
        model = InstantModel()

        # We start in target state, verify that no corrections are necessary
        self.assertAlmostEqual(model.Error(), 0.0)
        self.assertAlmostEqual(pid.Update(model.Error(), time()), 0.0)

        # Target a state of 10.0
        model.SetTargetState(10.0)
        self.assertAlmostEqual(model.Error(), 10.0)

        for i in xrange(30):
            correction = pid.Update(model.Error(), time())
            model.SetCorrection(correction)
            model.Update()

        self.assertAlmostEqual(model.Error(), 0.0)
        self.assertAlmostEqual(correction, 0.0)

    def testConvergenceWithADampenedResponse(self):
        """Test convergence with a model that reacts linearly to the correction."""

        class DampenedResponseModel(Model):
            def ApplyUpdate(self):
                self.state += self.correction / 100

        pid = pidcontroller.PID(1.0, 0.5, 0.1, time())
        model = DampenedResponseModel(target_state=10.0)
        self.assertAlmostEqual(model.Error(), 10.0)

        for i in xrange(4000):
            correction = pid.Update(model.Error(), time())
            model.SetCorrection(correction)
            model.Update()

        self.assertAlmostEqual(model.Error(), 0.0)
        self.assertAlmostEqual(correction, 0.0)


    def testConvergenceWithADisminishingResponse(self):
        """Test convergence with a model where the response disminishes
        linearly over time. We ignore the integral component here as
        it is misleading."""

        class DisminishingResponseModel(Model):
            def __init__(self, *args, **kwargs):
                super(DisminishingResponseModel, self).__init__(*args, **kwargs)
                self.age = 0

            def ApplyUpdate(self):
                self.age += 1
                self.state += self.correction / self.age

        pid = pidcontroller.PID(1.0, 0.0, 0.6, time())
        model = DisminishingResponseModel()

        # We start in target state, verify that no corrections are necessary
        self.assertAlmostEqual(model.Error(), 0.0)
        self.assertAlmostEqual(pid.Update(model.Error(), time()), 0.0)

        # Target a state of 10.0
        model.SetTargetState(10.0)
        self.assertAlmostEqual(model.Error(), 10.0)

        for i in xrange(100):
            correction = pid.Update(model.Error(), time())
            model.SetCorrection(correction)
            model.Update()

        self.assertAlmostEqual(model.Error(), 0.0)
        self.assertAlmostEqual(correction, 0.0)

if __name__ == '__main__':
    unittest.main()
