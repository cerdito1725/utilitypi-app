import datetime
import logging
from utility import update_svg, configure_logging
from sockets import socketclient, socketclient2
from solar import solarapi

configure_logging()

def main():

    output_svg_filename = '/home/neal/scripts/waveshare/screen-hotwater.svg'

    hotWater = str(socketclient.socketTemp())

    logging.info("Updating SVG")
    output_dict = {
        'HOT_WATER' : hotWater,
        'HOUSE_TEMP' : houseTemp,
        'TIME_NOW': (datetime.datetime.now()+datetime.timedelta(minutes=2)).strftime("%-I:%M%p"),
        'DAY_ONE': datetime.datetime.now().strftime("%b %-d"),
        'DAY_NAME': datetime.datetime.now().strftime("%a")
    }
    update_svg('/home/neal/scripts/waveshare/screen-hotwater.svg', '/home/neal/scripts/waveshare/screen-output-hotwater-temp.svg', output_dict)

if __name__ == "__main__":
    main()
