#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import time

# Card Register

cameroncard = '173177460'
lockcard = '6714182236'
lisacard = '2222'
colincard = '1111'

#GPIO setup

continue_reading = True

def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

while continue_reading:

# Scan for cards
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"

    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        UIDcode = str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
        print UIDcode

        # Control door lock
        statusFile = open('/home/pi/status.txt', 'r')
        locked = statusFile.readline()
        statusFile.close()
        statusFile2 = open('/home/pi/status2.txt', 'r')
        openTrigSwitch = statusFile2.readline()
        statusFile2.close()

        if UIDcode == cameroncard:
            adminpriv = 1
        else:
            adminpriv = 0

        if UIDcode == cameroncard or UIDcode == lisacard or UIDcode == colincard:
            if locked == '0' or adminpriv == 1:
                GPIO.setup(11, GPIO.OUT)
                print "Door open"
                time.sleep(3)
                GPIO.setup(11, GPIO.IN)
                print "Finished"
            else:
                print "Door locked"
        elif UIDcode == lockcard:
            counter = 0
            if locked == '0':
                while counter <> 5:
                    GPIO.setup(11, GPIO.OUT)
                    time.sleep(0.05)
                    GPIO.setup(11, GPIO.IN)
                    time.sleep(0.05)
                    counter = counter + 1
                locked = 1
                time.sleep(3)
            else:
                while counter <> 2:
                    GPIO.setup(11, GPIO.OUT)
                    time.sleep(0.5)
                    GPIO.setup(11, GPIO.IN)
                    time.sleep(0.05)
                    counter = counter + 1
                locked = 0
                time.sleep(3)

            fh = open('status.txt', 'w')
            fh.write(str(locked))
            fh.close()

        else:
            print "Unrecognised Card"
