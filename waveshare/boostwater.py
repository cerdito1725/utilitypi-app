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

boostRate = 0.50  # degrees C per minute
targetTemp = 70.0

# Default finish time
finish_hour = 6
finish_minute = 0

if len(sys.argv) > 1:
    try:
        parts = sys.argv[1].split(":")
        finish_hour = int(parts[0])
        finish_minute = int(parts[1]) if len(parts) > 1 else 0
    except ValueError:
        finish_hour = 6
        finish_minute = 0

GPIO.setup(RELAIS_1_GPIO, GPIO.OUT)

def seconds_until_finish(finish_hour: int, finish_minute: int) -> int:
    now = datetime.now()
    finish = now.replace(
        hour=finish_hour,
        minute=finish_minute,
        second=0,
        microsecond=0
    )
    if now >= finish:
        finish = finish + timedelta(days=1)
    return int((finish - now).total_seconds())

try:
    # Read current temp once
    tempNow = float(socketclient.socketTemp())
    tempRaise = targetTemp - tempNow

    if tempRaise > 0:
        boostTime = int((tempRaise / boostRate) * 60)  # seconds
        windowSeconds = seconds_until_finish(finish_hour, finish_minute)

        # Wait so we finish at finishHour, but never wait negative
        boostWait = max(0, windowSeconds - boostTime)

        logging.info(
            "Temp: %s C. Finish: %02d:%02d. Wait/Boost (mins): %s/%s",
            tempNow, finish_hour, finish_minute, round(boostWait / 60), round(boostTime / 60)
        )
        print(
            "Temp:", tempNow, "C. Finish:", f"{finish_hour:02d}:{finish_minute:02d}. "
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
            windowSeconds2 = seconds_until_finish(finish_hour, finish_minute)
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
        tempEnd = float(socketclient.socketTemp())
    except Exception:
        tempEnd = "?"
    logging.info("Ending boost at %s degrees", tempEnd)
    print("Ending boost at", tempEnd, "degrees")
