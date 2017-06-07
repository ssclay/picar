from nio.block.base import Block
from nio.util.discovery import discoverable
from nio.properties import IntProperty, VersionProperty
from Adafruit_MotorHAT import Adafruit_MotorHAT

@discoverable
class PiCar(Block):

    forward_speed = IntProperty(title="Forward speed, 0-255",
                                default=0)
    left_motor    = IntProperty(title="Rotation of left motor, 0-255",
                                default=0)
    right_motor   = IntProperty(title="Rotation of right motor, 0-255",
                                default=0)
    version = VersionProperty('0.0.1')

    def __init__(self):
        super().__init__()
        self.MotorHAT = Adafruit_MotorHAT(addr=0x60)
        self._motor_left  = self.MotorHAT.getMotor(1)
        self._motor_right = self.MotorHAT.getMotor(2)

    def process_signals(self, signals):
        for signal in signals:
            if (self.forward_speed(signal) >= 0):
                self._motor_right.run(Adafruit_MotorHAT.FORWARD)
                self._motor_left.run(Adafruit_MotorHAT.FORWARD)
                self._motor_right.setSpeed(self.forward_speed(signal))
                self._motor_left.setSpeed(self.forward_speed(signal))

    def stop(self):
        try:
            self.MotorHAT.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
            self.MotorHAT.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        except:
            self.logger.exception('Exception while halting motors')
