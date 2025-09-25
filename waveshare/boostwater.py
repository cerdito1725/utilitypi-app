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

RELAIS_1_GPIO = 14

boostRate = 0.55
tempRaise = 70-socketclient.socketTemp()
boostTime = int((tempRaise/boostRate)*60)
boostWait = 7200-boostTime

GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode

try:
   if tempRaise > 0:
      logging.info("Temp: "+str(socketclient.socketTemp())+" degrees. Wait/Boost (mins): "+str(round(boostWait/60))+"/"+str(round(boostTime/60)))
      print("Temp: "+str(socketclient.socketTemp())+" degrees. Wait/Boost (mins): "+str(round(boostWait/60))+"/"+str(round(boostTime/60)))
      time.sleep(boostWait)
      GPIO.output(RELAIS_1_GPIO, GPIO.HIGH)
      logging.info("Boosting at "+str(socketclient.socketTemp())+" degrees for "+str(round(boostTime/60))+" minutes")
      print("Boosting at "+str(socketclient.socketTemp())+" degrees for "+str(round(boostTime/60))+" minutes")
      time.sleep(boostTime)
except:
   GPIO.output(RELAIS_1_GPIO, GPIO.LOW)
   logging.info("Error - Ending boost at "+str(socketclient.socketTemp())+" degrees")
   print("Ending boost at "+str(socketclient.socketTemp())+" degrees")
	  
GPIO.output(RELAIS_1_GPIO, GPIO.LOW)
print("Ending boost at "+str(socketclient.socketTemp())+" degrees")
logging.info("Ending boost at "+str(socketclient.socketTemp())+" degrees")
