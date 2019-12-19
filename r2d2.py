from gpiozero import Button
from gpiozero import Motor
from gpiozero import LED

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

class R2D2():

    def __init__(self):
        motor_left = Motor(ML1, ML2)
        motor_right = Motor(MR1, MR2)
        motor_core = Motor(MC1, MC2)
        motor_left.stop()
        motor_right.stop()
        motor_core.stop()
        pos_b0 = Button(B0, False)
        pos_b1 = Button(B1, False)
        pos_b2 = Button(B2, False)
        pos_b3 = Button(B3, False)
        but_on_off = Button(ON_OFF, False)
        but_vol_up = Button(VOL_UP, False)
        but_vol_down = Button(VOL_DOWN, False)
        but_next = Button(NEXT, False)
        but_shuffle = Button(SHUFFLE, False)
        but_bluetooth = Button(BLUETOOTH, False)
        but_wifi = Button(WIFI, False)
        led_red = LED(RED, False)
        led_blue1 = LED(BLUE1, False)
        led_blue2 = LED(BLUE2, False)
        led_leia = LED(LEIA, False)
        led_red.on()
        led_blue1.off()
        led_blue2.off()
        led_leia.off()

    def core_turn_right():
        b0 = pos_b0.value
        b1 = pos_b1.value
        b2 = pos_b2.value
        b3 = pos_b3.value
        print "start:", b0, b1, b2, b3
        if not(b0==1 and b1==1 and b2==0):
            print "moving one to right"
            motor_core.forward(0.5)
            while (b0==pos_b0.value and b1==pos_b1.value and b2==pos_b2.value and b3==pos_b3.value):
                sleep(0.05)
            motor_core.stop()
            print "end:", pos_b0.value, pos_b1.value, pos_b2.value, pos_b3.value
            return True
        else:
            print "cannot move further right"
            return False

    def core_turn_left():
        b0 = pos_b0.value
        b1 = pos_b1.value
        b2 = pos_b2.value
        b3 = pos_b3.value
        print "start:", b0, b1, b2, b3
        if not(b0==1 and b1==1 and b2==1):
            print "moving one to left"
            motor_core.backward(0.5)
            while (b0==pos_b0.value and b1==pos_b1.value and b2==pos_b2.value and b3==pos_b3.value):
                sleep(0.05)
            motor_core.stop()
            print "end:", pos_b0.value, pos_b1.value, pos_b2.value, pos_b3.value
            return True
        else:
            print "cannot move further left"
            return False

    


