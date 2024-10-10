try:
    import RPi.GPIO as GPIO
except ImportError:
    print("This code must be run on a Raspberry Pi!")
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(25, GPIO.OUT)

GPIO.output(25, GPIO.HIGH)

time.sleep(5)

GPIO.cleanup()