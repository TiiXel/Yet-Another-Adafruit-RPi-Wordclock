# ===========================================================================
#
# WordClock/wordclock_interfaces/gpio_interface.py
# By Remi Berthoz (remi.berthoz@gmail.com)
#
# Last updated: mer. 17 janv. 2018 16:17:45  CET   (RB)
#
#
# ===========================================================================

from __future__ import print_function
import RPi.GPIO as GPIO
import time
import os


class gpiointerface:

    def __init__(self, event_handler):
        print('[    ] Initializing GPIO interface', end='')

        self.event_handler = event_handler

        # 3 buttons are required to run the wordclock
        # Below, for each button, the corresponding GPIO pin is specified
        self.button_left = 18
        self.button_return = 24
        self.button_right = 19

        # Initializations for GPIO inputs
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button_left, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.button_return, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.button_right, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.polarity = GPIO.FALLING

        if self.polarity == GPIO.FALLING:
            self.notpolarity = GPIO.RISING
        elif self.polarity == GPIO.RISING:
            self.notpolarity = GPIO.FALLING

        GPIO.add_event_detect(self.button_left,
                              self.polarity,
                              callback=lambda channel: self._left(),
                              bouncetime=1000)
        GPIO.add_event_detect(self.button_return,
                              self.polarity,
                              callback=lambda channel: self._return(),
                              bouncetime=1000)
        GPIO.add_event_detect(self.button_right,
                              self.polarity,
                              callback=lambda channel: self._right(),
                              bouncetime=1000)

        print('\r[DONE] Initializing GPIO interface')

    def _left(self):
        start = time.time()
        while True:
            state = GPIO.input(self.button_left)
            if state != GPIO.LOW:
                end = time.time()
                break
            time.sleep(0.02)
        # Avoid noise making sure the button was pressed more than 0.04s
        if end-start > 0.04:
            print('[PRESSED] Left')
            self.event_handler.setEvent(self.event_handler.EVENT_BUTTON_LEFT)

    def _return(self):
        start = time.time()
        while True:
            state = GPIO.input(self.button_return)
            if state != GPIO.LOW:
                end = time.time()
                break
            elif time.time()-start > 3.0:
                # Break after 3 seconds, discriminate long press
                end = time.time()
                break
            time.sleep(0.02)
        # Avoid noise making sure the button was pressed more than 0.04s
        if end-start > 0.04 and end-start < 3.0:
                print('[PRESSED] Return')
                self.event_handler.setEvent(
                        self.event_handler.EVENT_BUTTON_RETURN)
        if end-start > 3.0:
            print('[PRESSED] Return, long: shuting down')
            self.shutdown_the_pi()

    def _right(self):
        start = time.time()
        while True:
            state = GPIO.input(self.button_right)
            if state != GPIO.LOW:
                end = time.time()
                break
            time.sleep(0.02)
        # Avoid noise making sure the button was pressed more than 0.04s
        if end-start > 0.04:
            print('[PRESSED] Right')
            self.event_handler.setEvent(self.event_handler.EVENT_BUTTON_RIGHT)

    def __exit__(self, *args):
        print('Cleaning GPIO interface')
        GPIO.cleanup()

    def shutdown_the_pi(self):
        os.system('shutdown -h now')
