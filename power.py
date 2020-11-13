#!/usr/bin/python

import RPi.GPIO as GPIO
from subprocess import call
from datetime import datetime
import time

def power_btn():
    print("실행됬습니다")
    btnPin = 26
    shutdownSeconds = 2

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(btnPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    prevInput = -1
    pressTime = None

    def getPressTime():
        elapsed = 0
        if pressTime is not None:
            elapsed = (datetime.now() - pressTime).total_seconds()
        return elapsed

    while True:
        input = GPIO.input(btnPin)
        if input == 0:
            if prevInput == -1 or prevInput == 1:
                pressTime = datetime.now()
            elif prevInput == 0:
                if getPressTime() >= shutdownSeconds:
                    call(['shutdown', '-h', 'now'], shell=False)
                    break
        prevInput = input
        time.sleep(1)