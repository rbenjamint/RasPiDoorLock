import RPi.GPIO as GPIO
import time

opentime = 3

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)


while True:
    input_state = GPIO.input(18)
    if input_state == False:
        print 'Open'
        GPIO.setup(17, GPIO.OUT)
        time.sleep(3)
        GPIO.setup(17, GPIO.IN)
        print 'closed'
