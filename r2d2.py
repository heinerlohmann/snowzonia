from gpiozero import Button
from gpiozero import Motor
from gpiozero import LED
from time import sleep

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

POSTURES = [[1,1,1,0], [1,0,0,0], [1,0,1,0], [1,0,1,1], [0,0,1,0], [0,1,1,0], [0,1,0,0], [1,1,0,0]]

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

    def is_posture(self, posture):
        if posture[0]==self.pos_b0.value and posture[1]==self.pos_b1.value and posture[2]==self.pos_b2.value and posture[3]==self.pos_b3.value:
            return True
        else:
            return False

    def core_turn_to(self, goal_index, speed):
        start_index = self.get_posture()
        goal_posture = POSTURES[goal_index]
        print "turning from index ", start_index, " to index ", goal_index
        if start_index < goal_index:
            print "direction: forward"
            self.motor_core.forward(speed)
            while not self.is_posture(goal_posture):
                sleep(0.01)
            self.motor_core.stop()
        elif start_index > goal_index:
            print "direction: backward"
            self.motor_core.backward(speed)
            while not self.is_posture(goal_posture):
                sleep(0.01)
            self.motor_core.stop()
        else:
            print "direction: none"

    def default_posture(self):
        self.core_turn_to(5, 1.0)

    def turn_head(self, speed):
        current_index = self.get_posture()
        print "current index: ", current_index
        if current_index == 4 or current_index == 5 or current_index == 3:
            self.core_turn_to(6, speed)
        elif current_index == 6 or current_index == 7:
            self.core_turn_to(4, speed)
        elif current_index == 0 or current_index == 1:
            self.core_turn_to(2, speed)
        elif current_index == 2:
            self.core_turn_to(0, speed)

    def core_turn_right(self):
        b0 = self.pos_b0.value
        b1 = self.pos_b1.value
        b2 = self.pos_b2.value
        b3 = self.pos_b3.value
        print "start:", b0, b1, b2, b3
        if not(b0==1 and b1==1 and b2==0):
            print "moving one to right"
            self.motor_core.forward(0.5)
            while (b0==self.pos_b0.value and b1==self.pos_b1.value and b2==self.pos_b2.value and b3==self.pos_b3.value):
                sleep(0.05)
            self.motor_core.stop()
            print "end:", self.pos_b0.value, self.pos_b1.value, self.pos_b2.value, self.pos_b3.value
            return True
        else:
            print "cannot move further right"
            return False

    def core_turn_left(self):
        b0 = self.pos_b0.value
        b1 = self.pos_b1.value
        b2 = self.pos_b2.value
        b3 = self.pos_b3.value
        print "start:", b0, b1, b2, b3
        if not(b0==1 and b1==1 and b2==1):
            print "moving one to left"
            self.motor_core.backward(0.5)
            while (b0==self.pos_b0.value and b1==self.pos_b1.value and b2==self.pos_b2.value and b3==self.pos_b3.value):
                sleep(0.05)
            self.motor_core.stop()
            print "end:", self.pos_b0.value, self.pos_b1.value, self.pos_b2.value, self.pos_b3.value
            return True
        else:
            print "cannot move further left"
            return False

    

    


