import time
import logging
import sys
from datetime import datetime, timedelta

import RPi.GPIO as GPIO
from sockets import socketclient

Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(
    filename="boostwater.log",
    filemode="a",
    format=Log_Format,
    level=logging.INFO
)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

RELAIS_1_GPIO = 14

boostRate = 0.55
targetTemp = 70.0

# Finish hour passed as first arg, default to 6 (06:00)
# Use 16 for 4pm run.
finishHour = 6
if len(sys.argv) > 1:
    try:
        finishHour = int(sys.argv[1])
    except ValueError:
        finishHour = 6

GPIO.setup(RELAIS_1_GPIO, GPIO.OUT)

def seconds_until_finish(finish_hour: int) -> int:
    now = datetime.now()
    finish = now.replace(hour=finish_hour, minute=0, second=0, microsecond=0)
    if now >= finish:
        finish = finish + timedelta(days=1)
    return int((finish - now).total_seconds())

try:
    # Read current temp once
    tempNow = float(socketclient.socketTemp())
    tempRaise = targetTemp - tempNow

    if tempRaise > 0:
        boostTime = int((tempRaise / boostRate) * 60)  # seconds
        windowSeconds = seconds_until_finish(finishHour)

        # Wait so we finish at finishHour, but never wait negative
        boostWait = max(0, windowSeconds - boostTime)

        logging.info(
            "Temp: %s C. Finish: %02d:00. Wait/Boost (mins): %s/%s",
            tempNow, finishHour, round(boostWait / 60), round(boostTime / 60)
        )
        print(
            "Temp:", tempNow, "C. Finish:", f"{finishHour:02d}:00. "
            "Wait/Boost (mins):", round(boostWait / 60), "/", round(boostTime / 60)
        )

        time.sleep(boostWait)

        # Optional accuracy tweak with minimal code: re-read temp before heating
        tempNow2 = float(socketclient.socketTemp())
        tempRaise2 = targetTemp - tempNow2
        if tempRaise2 <= 0:
            logging.info("No boost needed at start time. Temp: %s C", tempNow2)
            print("No boost needed at start time. Temp:", tempNow2, "C")
        else:
            boostTime2 = int((tempRaise2 / boostRate) * 60)

            # Clamp boost to remaining time until finish so we do not run past finish time
            windowSeconds2 = seconds_until_finish(finishHour)
            boostTime2 = min(boostTime2, windowSeconds2)

            GPIO.output(RELAIS_1_GPIO, GPIO.HIGH)
            logging.info("Boosting at %s C for %s minutes", tempNow2, round(boostTime2 / 60))
            print("Boosting at", tempNow2, "C for", round(boostTime2 / 60), "minutes")
            time.sleep(boostTime2)

except Exception as e:
    logging.exception("Error in boostwater: %s", e)
    print("Error in boostwater:", e)

finally:
    GPIO.output(RELAIS_1_GPIO, GPIO.LOW)
    try:
        tempEnd = socketclient.socketTemp()
    except Exception:
        tempEnd = "?"
    logging.info("Ending boost at %s degrees", tempEnd)
    print("Ending boost at", tempEnd, "degrees")
