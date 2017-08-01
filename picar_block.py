from nio.block.base import Block
from nio.util.discovery import discoverable
from nio.properties import IntProperty, VersionProperty
from Adafruit_MotorHAT import Adafruit_MotorHAT

@discoverable
class PiCar(Block):

    forward_speed = IntProperty(title="Forward speed given to both motors, -255 - 255",
                                default=0)
    right_speed   = IntProperty(title="Additional Rotation of right motor, -255 - 255",
                                default=0)
    left_speed    = IntProperty(title="Additional Rotation of left motor, -255 - 255",
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
                right_wheel_speed = self.forward_speed(signal) + self.right_speed(signal)
                left_wheel_speed  = self.forward_speed(signal) + self.left_speed(signal)
                self._motor_right.setSpeed(right_wheel_speed)
                self._motor_left.setSpeed(left_wheel_speed)
            elif (self.forward_speed(signal) < 0):
                self._motor_right.run(Adafruit_MotorHAT.BACKWARD)
                self._motor_left.run(Adafruit_MotorHAT.BACKWARD)
                right_wheel_speed = abs(self.forward_speed(signal) + self.right_speed(signal))
                left_wheel_speed  = abs(self.forward_speed(signal) + self.left_speed(signal))
                self._motor_right.setSpeed(right_wheel_speed)
                self._motor_left.setSpeed(left_wheel_speed)

    def stop(self):
        super().stop()
        self._motor_left.setSpeed(0)
        self._motor_right.setSpeed(0)
        try:
            self.MotorHAT.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
            self.MotorHAT.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        except:
            self.logger.exception('Exception while halting motors')
