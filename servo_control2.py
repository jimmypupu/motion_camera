import RPi.GPIO as GPIO
from RPIO import PWM
import time

class Servo:
    def __init__(self):
        PWM.cleanup()
        self.servo = PWM.Servo()
        self.servo.set_servo(17, 1500)
        self.servo_lr_angle = 0
        self.servo.set_servo(22, 1500)
        self.servo_ud_angle = 0

    def servo_control_left_right(self, angle):
        new_angle = self.servo_lr_angle+angle
        self.servo_lr_angle = new_angle
        new_cycle = (float(new_angle)/45)*500 + 1500
        if new_cycle < 1000:
            new_cycle = 1000
            self.servo_lr_angle = -45
        if new_cycle > 2000:
            new_cycle = 2000
            self.servo_lr_angle = 45
        print("left_right: new_angle="+str(self.servo_lr_angle)+" new_cycle="+str(new_cycle)+" d_angle="+str(angle))
        self.servo.set_servo(17, int(new_cycle/10)*10)
        return self.servo_lr_angle
    def servo_control_up_down(self, angle):
        new_angle = self.servo_ud_angle+angle
        self.servo_ud_angle = new_angle
        new_cycle = (float(new_angle)/45)*500 + 1500
        if new_cycle < 1000:
            new_cycle = 1000
            self.servo_ud_angle = -45
        if new_cycle > 2000:
            new_cycle = 2000
            self.servo_ud_angle = 45
        print("up_down: new_angle="+str(self.servo_ud_angle)+" new_cycle="+str(new_cycle))
        self.servo.set_servo(22, int(new_cycle/10)*10)
        return self.servo_ud_angle
    def servo_reset(self):
        self.servo.set_servo(17, 1500)
        self.servo.set_servo(22, 1500)
        self.servo_lr_angle = 0
        self.servo_ud_angle = 0

def main():
    servo = Servo()
    time.sleep(5)
    servo.servo_control_up_down(45)
    servo.servo_control_left_right(-45)
    time.sleep(3)
    servo.servo_reset()
    time.sleep(3)
    PWM.cleanup()
    #GPIO.cleanup()

if __name__ == "__main__":
    main()
