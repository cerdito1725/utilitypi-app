#!/usr/bin/python

import datetime
import sys
import os
import logging
from weather_providers import climacell, openweathermap, metofficedatahub, metno, meteireann, accuweather, visualcrossing, weathergov
from alert_providers import metofficerssfeed, weathergovalerts
from alert_providers import meteireann as meteireannalertprovider
from utility import update_svg, configure_logging
import textwrap
import html
from sockets import socketclient, socketclient2
from solar import solarapi

configure_logging()


def format_weather_description(weather_description):
    if len(weather_description) < 20:
        return {1: weather_description, 2: ''}

    splits = textwrap.fill(weather_description, 20, break_long_words=False,
                           max_lines=2, placeholder='...').split('\n')
    weather_dict = {1: splits[0]}
    weather_dict[2] = splits[1] if len(splits) > 1 else ''
    return weather_dict

def get_weather(location_lat, location_long, units):

    # gather relevant environment configs
    climacell_apikey = os.getenv("CLIMACELL_APIKEY")
    openweathermap_apikey = os.getenv("OPENWEATHERMAP_APIKEY")
    metoffice_clientid = os.getenv("METOFFICEDATAHUB_CLIENT_ID")
    metoffice_clientsecret = os.getenv("METOFFICEDATAHUB_CLIENT_SECRET")
    accuweather_apikey = os.getenv("ACCUWEATHER_APIKEY")
    accuweather_locationkey = os.getenv("ACCUWEATHER_LOCATIONKEY")
    metno_self_id = os.getenv("METNO_SELF_IDENTIFICATION")
    visualcrossing_apikey = os.getenv("VISUALCROSSING_APIKEY")
    use_met_eireann = os.getenv("WEATHER_MET_EIREANN")
    weathergov_self_id = os.getenv("WEATHERGOV_SELF_IDENTIFICATION")

    if (
        not climacell_apikey
        and not openweathermap_apikey
        and not metoffice_clientid
        and not accuweather_apikey
        and not metno_self_id
        and not visualcrossing_apikey
        and not use_met_eireann
        and not weathergov_self_id
    ):
        logging.error("No weather provider has been configured (Climacell, OpenWeatherMap, Weather.gov, MetOffice, AccuWeather, Met.no, Met Eireann, VisualCrossing...)")
        sys.exit(1)

    if visualcrossing_apikey:
        logging.info("Getting weather from Visual Crossing")
        weather_provider = visualcrossing.VisualCrossing(visualcrossing_apikey, location_lat, location_long, units)

    elif use_met_eireann:
        logging.info("Getting weather from Met Eireann")
        weather_provider = meteireann.MetEireann(location_lat, location_long, units)

    elif weathergov_self_id:
        logging.info("Getting weather from Weather.gov")
        weather_provider = weathergov.WeatherGov(weathergov_self_id, location_lat, location_long, units)

    elif metno_self_id:
        logging.info("Getting weather from Met.no")
        weather_provider = metno.MetNo(metno_self_id, location_lat, location_long, units)

    elif accuweather_apikey:
        logging.info("Getting weather from Accuweather")
        weather_provider = accuweather.AccuWeather(accuweather_apikey, location_lat,
                                                   location_long,
                                                   accuweather_locationkey,
                                                   units)

    elif metoffice_clientid:
        logging.info("Getting weather from Met Office Weather Datahub")
        weather_provider = metofficedatahub.MetOffice(metoffice_clientid,
                                                      metoffice_clientsecret,
                                                      location_lat,
                                                      location_long,
                                                      units)

    elif openweathermap_apikey:
        logging.info("Getting weather from OpenWeatherMap")
        weather_provider = openweathermap.OpenWeatherMap(openweathermap_apikey,
                                                         location_lat,
                                                         location_long,
                                                         units)

    elif climacell_apikey:
        logging.info("Getting weather from Climacell")
        weather_provider = climacell.Climacell(climacell_apikey, location_lat, location_long, units)

    weather = weather_provider.get_weather()
    logging.info("weather - {}".format(weather))
    return weather

def format_alert_description(alert_message):
    return html.escape(alert_message)

def get_alert_message(location_lat, location_long):
    alert_message = ""
    alert_metoffice_feed_url = os.getenv("ALERT_METOFFICE_FEED_URL")
    alert_weathergov_self_id = os.getenv("ALERT_WEATHERGOV_SELF_IDENTIFICATION")
    alert_meteireann_feed_url = os.getenv("ALERT_MET_EIREANN_FEED_URL")

    if alert_weathergov_self_id:
        logging.info("Getting weather alert from Weather.gov API")
        alert_provider = weathergovalerts.WeatherGovAlerts(location_lat, location_long, alert_weathergov_self_id)
        alert_message = alert_provider.get_alert()

    elif alert_metoffice_feed_url:
        logging.info("Getting weather alert from Met Office RSS Feed")
        alert_provider = metofficerssfeed.MetOfficeRssFeed(alert_metoffice_feed_url)
        alert_message = alert_provider.get_alert()

    elif alert_meteireann_feed_url:
        logging.info("Getting weather alert from Met Eireann")
        alert_provider = meteireannalertprovider.MetEireannAlertProvider(alert_meteireann_feed_url)
        alert_message = alert_provider.get_alert()

#    logging.info("alert - {}".format(alert_message))
    return alert_message


def main():

    template_name = os.getenv("SCREEN_LAYOUT", "1")
    location_lat = os.getenv("WEATHER_LATITUDE", "51.5077")
    location_long = os.getenv("WEATHER_LONGITUDE", "-0.1277")
    weather_format = os.getenv("WEATHER_FORMAT", "CELSIUS")
    hotWater = str(socketclient.socketTemp())
    houseTemp = str(socketclient2.socketTemp())
    totalPower,currentUse = solarapi.stationDetail()
    currentPower,gridPower,gridSell,gridBuy,batteryCharge = solarapi.inverterDetail()

    if (weather_format == "CELSIUS"):
        units = "metric"
        degrees = "°C"
    else:
        units = "imperial"
        degrees = "°F"

    weather = get_weather(location_lat, location_long, units)

    if not weather:
        logging.error("Unable to fetch weather payload. SVG will not be updated.")
        return

    weather_desc = format_weather_description(weather["description"])

    alert_message = get_alert_message(location_lat, location_long)
    alert_message = format_alert_description(alert_message)

    output_dict = {
        'LOW_ONE': "{}{}".format(str(round(weather['temperatureMin'])), degrees),
        'HIGH_ONE': "{}{}".format(str(round(weather['temperatureMax'])), degrees),
        'TEMP_NOW': "{}{}".format(str(round(weather['temperatureNow'])), degrees),
        'TEMPPLUS1': "{}{}".format(str(round(weather['temperaturePlus1'])), degrees),
        'TEMPPLUS2': "{}{}".format(str(round(weather['temperaturePlus2'])), degrees),
        'TEMPPLUS3': "{}{}".format(str(round(weather['temperaturePlus3'])), degrees),
        'TEMPPLUS4': "{}{}".format(str(round(weather['temperaturePlus4'])), degrees),
        'TEMPPLUS5': "{}{}".format(str(round(weather['temperaturePlus5'])), degrees),
        'TEMPPLUS6': "{}{}".format(str(round(weather['temperaturePlus6'])), degrees),
        'TEMPPLUS7': "{}{}".format(str(round(weather['temperaturePlus7'])), degrees),
        'TEMPPLUS8': "{}{}".format(str(round(weather['temperaturePlus8'])), degrees),
        'ICON_ONE': weather["icon"],
        'ICON_PLUS1': weather["iconPlus1"],
        'ICON_PLUS2': weather["iconPlus2"],
        'ICON_PLUS3': weather["iconPlus3"],
        'ICON_PLUS4': weather["iconPlus4"],
        'ICON_PLUS5': weather["iconPlus5"],
        'ICON_PLUS6': weather["iconPlus6"],
        'ICON_PLUS7': weather["iconPlus7"],
        'ICON_PLUS8': weather["iconPlus8"],
        'WEATHER_DESC_1': weather_desc[1],
        'WEATHER_DESC_2': weather_desc[2],
        'TIME_NOW': (datetime.datetime.now()+datetime.timedelta(minutes=2)).strftime("%-I:%M%p"),
        'HOUR_NOW': datetime.datetime.now().strftime("%-I%p"),
        'HOUR_1': (datetime.datetime.now()+datetime.timedelta(hours=1)).strftime("%-I%p"),
        'HOUR_2': (datetime.datetime.now()+datetime.timedelta(hours=2)).strftime("%-I%p"),
        'HOUR_3': (datetime.datetime.now()+datetime.timedelta(hours=3)).strftime("%-I%p"),
        'HOUR_4': (datetime.datetime.now()+datetime.timedelta(hours=4)).strftime("%-I%p"),
        'HOUR_5': (datetime.datetime.now()+datetime.timedelta(hours=5)).strftime("%-I%p"),
        'HOUR_6': (datetime.datetime.now()+datetime.timedelta(hours=6)).strftime("%-I%p"),
        'HOUR_7': (datetime.datetime.now()+datetime.timedelta(hours=7)).strftime("%-I%p"),
        'HOUR_8': (datetime.datetime.now()+datetime.timedelta(hours=8)).strftime("%-I%p"),
        'HOUR_9': (datetime.datetime.now()+datetime.timedelta(hours=9)).strftime("%-I%p"),
        'RAIN_NOW': "{}{}".format(str(round(weather['rainNow'])), "%"),
        'RAIN_PLUS1': "{}{}".format(str(round(weather['rainPlus1'])), "%"),
        'RAIN_PLUS2': "{}{}".format(str(round(weather['rainPlus2'])), "%"),
        'RAIN_PLUS3': "{}{}".format(str(round(weather['rainPlus3'])), "%"),
        'RAIN_PLUS4': "{}{}".format(str(round(weather['rainPlus4'])), "%"),
        'RAIN_PLUS5': "{}{}".format(str(round(weather['rainPlus5'])), "%"),
        'RAIN_PLUS6': "{}{}".format(str(round(weather['rainPlus6'])), "%"),
        'RAIN_PLUS7': "{}{}".format(str(round(weather['rainPlus7'])), "%"),
        'RAIN_PLUS8': "{}{}".format(str(round(weather['rainPlus8'])), "%"),
        'RAIN_MILL_NOW': "{}{}".format(str(weather['rainMillNow']), "mm"),
        'RAIN_MILL_PLUS1': "{}{}".format(str(weather['rainMillPlus1']), "mm"),
        'RAIN_MILL_PLUS2': "{}{}".format(str(weather['rainMillPlus2']), "mm"),
        'RAIN_MILL_PLUS3': "{}{}".format(str(weather['rainMillPlus3']), "mm"),
        'RAIN_MILL_PLUS4': "{}{}".format(str(weather['rainMillPlus4']), "mm"),
        'RAIN_MILL_PLUS5': "{}{}".format(str(weather['rainMillPlus5']), "mm"),
        'RAIN_MILL_PLUS6': "{}{}".format(str(weather['rainMillPlus6']), "mm"),
        'RAIN_MILL_PLUS7': "{}{}".format(str(weather['rainMillPlus7']), "mm"),
        'RAIN_MILL_PLUS8': "{}{}".format(str(weather['rainMillPlus8']), "mm"),
        'DAY_ONE': datetime.datetime.now().strftime("%b %-d"),
        'DAY_NAME': datetime.datetime.now().strftime("%a"),
        'ALERT_MESSAGE_VISIBILITY': "visible" if alert_message else "hidden",
        'ALERT_MESSAGE': alert_message,
        'HOT_WATER' : hotWater,
        'HOUSE_TEMP' : houseTemp,
        'TOTAL_POWER' : "{:.0f}".format(totalPower),
        'CURRENT_USE' : "{:.1f}".format(currentUse/1000),
        'CURRENT_POWER' : "{:.1f}".format(currentPower),
        'GRID_POWER' : "{:.1f}".format(gridPower),
        'GRID_SELL' : "{:.0f}".format(gridSell),
        'GRID_BUY' : "{:.0f}".format(gridBuy),
        'BATT_CHARGE' : "{:.0f}".format(batteryCharge),
        'TIME_NOW': (datetime.datetime.now()+datetime.timedelta(minutes=2)).strftime("%-I:%M%p"),
        'DAY_ONE': datetime.datetime.now().strftime("%b %-d"),
        'DAY_NAME': datetime.datetime.now().strftime("%a")
    }

    logging.debug("main() - {}".format(output_dict))

    logging.info("Updating SVG")

    template_svg_filename = f'/home/neal/apps/utility/waveshare/WeatherSolarTemplate.svg'
    output_svg_filename = '/home/neal/apps/utility/waveshare/WeatherSolarOutput.svg'
    update_svg(template_svg_filename, output_svg_filename, output_dict)

if __name__ == "__main__":
    main()
