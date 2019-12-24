from gpiozero import Button
from gpiozero import Motor
from gpiozero import LED
from time import sleep
from time import time
from random import uniform
from random import randint

# GPIO configuration
# motor left leg
ML1 = 14
ML2 = 15
# motor right leg
MR1 = 23
MR2 = 24
# motor core
MC1 = 16
MC2 = 20
# position sensors
B0 = 25
B1 = 8
B2 = 7
B3 = 12
# buttons
ON_OFF = 4
VOL_UP = 17
VOL_DOWN = 27
NEXT = 22
SHUFFLE = 11
BLUETOOTH = 10
WIFI = 9
# LEDs
RED = 5
BLUE1 = 6
BLUE2 = 13
LEIA = 26

POSTURES = [[1,1,1,0], [1,0,0,0], [1,0,1,0], [1,0,1,1], [1,0,1,0], [0,0,1,0], [0,1,1,0], [0,1,0,0], [1,1,0,0]]

class R2D2():

    def __init__(self):
        self.motor_left = Motor(ML1, ML2)
        self.motor_right = Motor(MR1, MR2)
        self.motor_core = Motor(MC1, MC2)
        self.motor_left.stop()
        self.motor_right.stop()
        self.motor_core.stop()
        self.pos_b0 = Button(B0, False)
        self.pos_b1 = Button(B1, False)
        self.pos_b2 = Button(B2, False)
        self.pos_b3 = Button(B3, False)
        self.but_on_off = Button(ON_OFF, False)
        self.but_vol_up = Button(VOL_UP, False)
        self.but_vol_down = Button(VOL_DOWN, False)
        self.but_next = Button(NEXT, False)
        self.but_shuffle = Button(SHUFFLE, False)
        self.but_bluetooth = Button(BLUETOOTH, False)
        self.but_wifi = Button(WIFI, False)
        self.led_red = LED(RED, False)
        self.led_blue1 = LED(BLUE1, False)
        self.led_blue2 = LED(BLUE2, False)
        self.led_leia = LED(LEIA, False)
        self.led_red.on()
        self.led_blue1.off()
        self.led_blue2.off()
        self.led_leia.off()

    def get_posture(self):
        b0 = self.pos_b0.value
        b1 = self.pos_b1.value
        b2 = self.pos_b2.value
        b3 = self.pos_b3.value
        return POSTURES.index([b0,b1,b2,b3])

    def turn_core_to(self, goal_index, speed):
        start_index = self.get_posture()
        if start_index < goal_index:
            self.motor_core.forward(speed)
            while not self.get_posture() == goal_index:
                sleep(0.01)
            self.motor_core.stop()
        elif start_index > goal_index:
            self.motor_core.backward(speed)
            while not self.get_posture() == goal_index:
                sleep(0.01)
            self.motor_core.stop()

    def default_posture(self, speed):
        if self.get_posture() > 6:
            self.turn_core_to(5, speed)
        elif self.get_posture() < 5:
            self.turn_core_to(6, speed)

    def force_default_posture(self, speed):
        if self.get_posture() > 5:
            self.turn_core_to(5, speed)
        elif self.get_posture() < 6:
            self.turn_core_to(6, speed)

    def turn_head_randomly(self, times, speed):
        self.default_posture(speed)
        duration1 = uniform(0.4, 0.7)
        duration2 = uniform(0.4, 0.7)
        direction = randint(0, 1)
        for i in range(times):
            if direction == 0:
                direction = 1
                self.motor_core.forward(speed)
                timeout = time() + duration1
                while time() < timeout and not self.get_posture() == 7:
                    sleep(0.01)
            else:
                direction = 0
                self.motor_core.backward(speed)
                timeout = time() + duration2
                while time() < timeout and not self.get_posture() == 4:
                    sleep(0.01)
            self.motor_core.stop()
        self.force_default_posture(speed)

    def sad_posture(self, speed):
        self.turn_core_to(0, speed)
        self.turn_core_to(2, speed/2)

    def forward(self, duration, speed):
        self.motor_left.forward(speed)
        self.motor_right.forward(speed)
        sleep(duration)
        self.motor_left.stop()
        self.motor_right.stop()

    def backward(self, duration, speed):
        self.motor_left.backward(speed)
        self.motor_right.backward(speed)
        sleep(duration)
        self.motor_left.stop()
        self.motor_right.stop()

    def turn_left(self, duration, speed):
        self.motor_left.backward(speed)
        self.motor_right.forward(speed)
        sleep(duration)
        self.motor_left.stop()
        self.motor_right.stop()

    def turn_right(self, duration, speed):
        self.motor_left.forward(speed)
        self.motor_right.backward(speed)
        sleep(duration)
        self.motor_left.stop()
        self.motor_right.stop()

    def random_dance(self, duration):
        dance_index = randint(0, 1)
        if dance_index == 0:
            self.dance_upright(duration)
        elif dance_index == 1:
            self.dance_swingbackandforth(duration)

    def dance_upright(self, duration):
        self.turn_core_to(3, 1)
        self.turn_left(0.1, 0.3)
        timeout = time() + duration
        while time() < timeout:
            self.turn_right(0.2, 0.3)
            self.turn_left(0.2, 0.3)
        self.turn_right(0.1, 0.3)

    def dance_swingbackandforth(self, duration):
        timeout = time() + duration
        while time() < timeout:
            self.turn_core_to(2, 0.7)
            self.turn_core_to(4, 0.7)
