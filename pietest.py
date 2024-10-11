try:
    import RPi.GPIO as GPIO
except ImportError:
    print("This code must be run on a Raspberry Pi!")
    sys.stdout.flush()
import SMHI
import time
from datetime import datetime, timedelta
import sys
import logging  #testa tail -f logfile.txt
#tmux new -s mysession ---------   python -u script.py
#tmux attach -t mysession

logging.basicConfig(filename='smhi.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s',filemode='a')

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
        
        sys.stdout.flush()
        temp = SMHI.fetch_latest_hour_temp_stockholm()
        print(f"Temperature: {temp} degrees Celsius")
        sys.stdout.flush()
        logging.info(f"Temperature: {temp} degrees Celsius")
        
        if temp is not None:
            if temp <= 7.0:
                GPIO.output(ledpin, GPIO.HIGH)
            elif temp > 7:
                GPIO.output(ledpin, GPIO.LOW)
            else:
                continue  # Skip the rest of the loop if temp is exactly 12.0

            current_status = GPIO.input(ledpin)
            if current_status != previous_status:
                if current_status == GPIO.HIGH:
                    print("LED on")
                    logging.info("LED on")
                    sys.stdout.flush()
                    
                else:
                    print("LED off")
                    logging.info("LED off")
                    sys.stdout.flush()
                previous_status = current_status
               
        else:
            print(f"temp is {temp}")
            GPIO.output(ledpin, GPIO.LOW)  # Ensure LED is off if no data is found
        time_to_sleep = get_seconds_until_next_hour()+30
        seconds_to_minutes = time_to_sleep / 60
        print(f"Sleeping for {seconds_to_minutes} minutes") 
        sys.stdout.flush()
        time.sleep(time_to_sleep)

except KeyboardInterrupt:
    print("Exiting program")
    logging.info(f"Exiting program at {datetime.now()}")
    logging.info("---------------------------")
    GPIO.cleanup()
    exit()
finally:
    GPIO.cleanup()
        

#scp C:\Users\AUPX\Patrax\SMHI\pietest.py aupx@192.168.10.136:/home/aupx/scripts

#