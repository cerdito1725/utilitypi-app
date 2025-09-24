import time
import logging
import RPi.GPIO as GPIO
from datetime import datetime,timedelta
from sockets import socketclient

Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(filename = "boostwater.log",
                    filemode = "a",
                    format = Log_Format, 
                    level = logging.INFO)

logger = logging.getLogger()

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
GPIO.setwarnings(False)

RELAIS_1_GPIO = 4

GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode

try:
   if socketclient.socketTemp() < 23:
      GPIO.output(RELAIS_1_GPIO, GPIO.HIGH)
      logging.info("Time is "+str(datetime.now())+" - Boosting at "+str(socketclient.socketTemp())+" degrees for 50 minutes")
      time.sleep(3000)
   elif socketclient.socketTemp() < 28:
      logging.info("Time is "+str(datetime.now())+" - Waiting for 20 minutes at "+str(socketclient.socketTemp())+" degrees")      
      time.sleep(1200)
      GPIO.output(RELAIS_1_GPIO, GPIO.HIGH)	  
      logging.info("Time is "+str(datetime.now())+" - Boosting at "+str(socketclient.socketTemp())+" degrees for 40 minutes")
      time.sleep(2400)
   elif socketclient.socketTemp() < 33:
      logging.info("Time is "+str(datetime.now())+" - Waiting for 30 minutes at "+str(socketclient.socketTemp())+" degrees")      
      time.sleep(1800)
      GPIO.output(RELAIS_1_GPIO, GPIO.HIGH)	  
      logging.info("Time is "+str(datetime.now())+" - Boosting at "+str(socketclient.socketTemp())+" degrees for 30 minutes")
      time.sleep(1800)
   elif socketclient.socketTemp() < 38:
      logging.info("Time is "+str(datetime.now())+" - Waiting for 40 minutes at "+str(socketclient.socketTemp())+" degrees")
      time.sleep(2400)
      GPIO.output(RELAIS_1_GPIO, GPIO.HIGH)	  
      logging.info("Time is "+str(datetime.now())+" - Boosting at "+str(socketclient.socketTemp())+" degrees for 20 minutes")
      time.sleep(1200)
except:
   GPIO.output(RELAIS_1_GPIO, GPIO.LOW)
   logging.info("Error at "+str(datetime.now())+" - Ending boost at "+str(socketclient.socketTemp())+" degrees")
	  
GPIO.output(RELAIS_1_GPIO, GPIO.LOW)
logging.info("Time is "+str(datetime.now())+" - Ending boost at "+str(socketclient.socketTemp())+" degrees")
