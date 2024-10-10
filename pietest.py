try:
    import RPi.GPIO as GPIO
except ImportError:
    print("This code must be run on a Raspberry Pi!")
import SMHI
import time
from datetime import datetime, timedelta
import sys
sys.stdout.flush()
ledpin = 26

sleeptime = 30

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledpin, GPIO.OUT)
GPIO.setwarnings(False)

previous_status = None

def get_seconds_until_next_hour():
    now = datetime.now()
    next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    return (next_hour - now).total_seconds()

try:
    while(True):

        temp = SMHI.fetch_latest_hour_temp_stockholm()
        print(f"Temperature: {temp} degrees Celsius")
        
        if temp is not None:
            if temp < 13.0:
                GPIO.output(ledpin, GPIO.HIGH)
            elif temp > 13.0:
                GPIO.output(ledpin, GPIO.LOW)
            else:
                continue  # Skip the rest of the loop if temp is exactly 12.0

            current_status = GPIO.input(ledpin)
            if current_status != previous_status:
                if current_status == GPIO.HIGH:
                    print("LED on")
                else:
                    print("LED off")
                previous_status = current_status
        else:
            print(f"temp is {temp}")
            GPIO.output(ledpin, GPIO.LOW)  # Ensure LED is off if no data is found
        time_to_sleep = get_seconds_until_next_hour()+30
        seconds_to_minutes = time_to_sleep / 60
        print(f"Sleeping for {seconds_to_minutes} minutes") 
        time.sleep(time_to_sleep)

except KeyboardInterrupt:
    print("Exiting program")
    GPIO.cleanup()
    exit()
finally:
    GPIO.cleanup()
        

#scp C:\Users\AUPX\Patrax\SMHI\pietest.py aupx@192.168.10.136:/home/aupx/scripts

