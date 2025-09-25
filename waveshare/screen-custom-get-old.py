import datetime
import logging
from utility import update_svg, configure_logging
from sockets import socketclient, socketclient2
from solar import solarapi

configure_logging()

def main():

    output_svg_filename = '/home/neal/scripts/waveshare/screen-custom.svg'

    hotWater = str(socketclient.socketTemp())
    houseTemp = str(socketclient2.socketTemp())
    totalPower,currentUse = solarapi.stationDetail()
    currentPower,gridPower,gridSell,gridBuy,batteryCharge = solarapi.inverterDetail()

    logging.info("Updating SVG")
    output_dict = {
        'HOT_WATER' : hotWater,
        'HOUSE_TEMP' : houseTemp,
        'TOTAL_POWER' : "{:.0f}".format(totalPower),
        'CURRENT_USE' : "{:.1f}".format(currentUse/1000),
        'CURRENT_POWER' : "{:.1f}".format(currentPower),
        'GRID_POWER' : "{:.1f}".format(gridPower),
        'GRID_SELL' : "{:.0f}".format(gridSell*10),
        'GRID_BUY' : "{:.0f}".format(gridBuy),
        'BATT_CHARGE' : "{:.0f}".format(batteryCharge),
        'TIME_NOW': (datetime.datetime.now()+datetime.timedelta(minutes=2)).strftime("%-I:%M%p"),
        'DAY_ONE': datetime.datetime.now().strftime("%b %-d"),
        'DAY_NAME': datetime.datetime.now().strftime("%a")
    }
    update_svg('/home/neal/scripts/waveshare/screen-custom.svg', '/home/neal/scripts/waveshare/screen-output-custom-temp.svg', output_dict)

if __name__ == "__main__":
    main()
