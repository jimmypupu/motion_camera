import RPi.GPIO as GPIO
import time

class Servo:
    def __init__(self):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11,GPIO.OUT) #servo_left_right
        self.pwm_servo_lr=GPIO.PWM(11,50)
        self.pwm_servo_lr.start(7.5)
        self.servo_lr_angle = 0
        GPIO.setup(15,GPIO.OUT) #servo_up_down
        self.pwm_servo_ud=GPIO.PWM(15,50)
        self.pwm_servo_ud.start(7.5)
        self.servo_ud_angle = 0

    def servo_control_left_right(self, angle):
        new_angle = self.servo_lr_angle+angle
        self.servo_lr_angle = new_angle
        new_cycle = (float(new_angle)/45)*2.5 + 7.5
        if new_cycle < 5:
            new_cycle = 5
            self.servo_lr_angle = -45
        if new_cycle > 10:
            new_cycle = 10
            self.servo_lr_angle = 45
        print("left_right: new_angle="+str(self.servo_lr_angle)+" new_cycle="+str(new_cycle))
        self.pwm_servo_lr.ChangeDutyCycle(new_cycle)
        return self.servo_lr_angle
    def servo_control_up_down(self, angle):
        new_angle = self.servo_ud_angle+angle
        self.servo_ud_angle = new_angle
        new_cycle = (float(new_angle)/45)*2.5 + 7.5
        if new_cycle < 5:
            new_cycle = 5
            self.servo_ud_angle = -45
        if new_cycle > 10:
            new_cycle = 10
            self.servo_ud_angle = 45
        print("up_down: new_angle="+str(self.servo_ud_angle)+" new_cycle="+str(new_cycle))
        self.pwm_servo_ud.ChangeDutyCycle(new_cycle)
        return self.servo_ud_angle
    def servo_reset(self):
        self.pwm_servo_ud.ChangeDutyCycle(7.5)
        self.pwm_servo_lr.ChangeDutyCycle(7.5)
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
    #GPIO.cleanup()

if __name__ == "__main__":
    main()
