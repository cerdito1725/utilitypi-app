
import logging
import datetime
from datetime import timedelta
from weather_providers.base_provider import BaseWeatherProvider

class MetEireann(BaseWeatherProvider):
    '''
    Provide weather data using Met Eireann, http://www.met.ie/
    '''
    def __init__(self, location_lat, location_long, units):
        self.location_lat = location_lat
        self.location_long = location_long
        self.units = units

    # Map Met Eireann icons to local icons
    # Reference: https://www.met.ie/Open_Data/Notes-on-API-XML-file_V6.odt
    def get_icon_from_met_eireann_weathercode(self, weathercode):

        icon_dict = {
                        1: "clear_sky_day",  # Sunny day
                        101: "clearnight",  # Clear night
                        2: "scattered_clouds",  # Light cloud (day)
                        102: "partlycloudynight",  # Partly cloudy (night)
                        3: "scattered_clouds",  # Partly cloudy (day)
                        103: "partlycloudynight",  # Partly cloudy (night)
                        4: "scattered_clouds",  # Cloudy (day)
                        5: "climacell_rain_light",  # Light rain sun (day)
                        105: "rain_night_light",  # Light rain sun (night)
                        6: "climacell_rain_light",  # Light rain thunder sun (day)
                        106: "rain_night_light",  # Light rain thunder sun (night)
                        7: "sleet",  # Sleet sun (day)
                        107: "sleet",  # Sleet sun (night)
                        8: "climacell_snow_light",  # Snow sun (day)
                        108: "climacell_snow_light",  # Snow sun (night)
                        9: "climacell_rain_light",  # Light rain shower (day)
                        10: "climacell_rain",  # DayNight - Rain
                        11: "thundershower_rain",  # Thunder shower (day)
                        12: "sleet",  # Sleet shower (day)
                        13: "snow",  # Heavy snow shower (day)
                        14: "snow",  # snow/thunder (day)
                        15: "climacell_fog",  # fog (day)
                        20: "sleet",  # Sleet shower (day)
                        120: "sleet",  # Sleet shower (night)
                        21: "snow",  # Heavy snow shower (day)
                        121: "snow",  # Heavy snow shower (night)
                        22: "climacell_rain_light",  # Light rain thunder (day)
                        23: "sleet",  # Sleet thunder (day)
                        24: "climacell_drizzle",  # Drizzle Thunder Sun
                        124: "climacell_drizzle",  # Drizzle Thunder Sun
                        25: "thundershower_rain",  # Thunder shower sun (day)
                        125: "thundershower_rain",  # Thunder shower sun (night)
                        26: "sleet",  # Light Sleet thunder sun (day)
                        126: "sleet",  # Light Sleet thunder sun (night)
                        27: "sleet",  # Heavy Sleet thunder sun (day)
                        127: "sleet",  # Heavy Sleet thunder sun (night)
                        28: "snow",  # Light snow thunder sun (day)
                        128: "snow",  # Light snow thunder sun (night)
                        29: "snow",  # Heavy snow thunder sun (day)
                        129: "snow",  # Heavy snow thunder sun (night)
                        30: "climacell_drizzle",  # Drizzle Thunder
                        31: "sleet",  # Light Sleet thunder (day)
                        131: "sleet",  # Light Sleet thunder (night)
                        32: "sleet",  # Heavy Sleet thunder (day)
                        132: "sleet",  # Heavy Sleet thunder (night)
                        33: "snow",  # Light snow thunder (day)
                        133: "snow",  # Light snow thunder (night)
                        34: "snow",  # Heavy snow thunder (day)
                        134: "snow",  # Heavy snow thunder (night)
                        40: "climacell_drizzle",  # Drizzle
                        140: "climacell_drizzle",  # Drizzle (night)
                        41: "climacell_rain_light",  # rain sun (day)
                        141: "climacell_rain_light",  # rain sun (night)
                        42: "sleet",  # Light Sleet sun (day)
                        142: "sleet",  # Light Sleet sun (night)
                        43: "sleet",  # Heavy Sleet sun (day)
                        143: "sleet",  # Heavy Sleet sun (night)
                        44: "snow",  # Light snow sun (day)
                        144: "snow",  # Light snow sun (night)
                        45: "snow",  # Heavy snow sun (day)
                        145: "snow",  # Heavy snow sun (night)
                        46: "climacell_drizzle",  # Drizzle
                        47: "sleet",  # Light Sleet
                        48: "climacell_ice_pellets",  # Heavy Sleet
                        49: "climacell_snow_light",  # Light snow
                        50: "snow",  # Heavy snow
                    }

        icon = icon_dict[weathercode]
        logging.debug(
            "get_icon_by_weathercode({}) - {}"
            .format(weathercode, icon))

        return icon

    def get_description_from_met_eireann_weathercode(self, weathercode):
        if (weathercode > 100):
            weathercode = weathercode - 100     # transform night to day

        # use official names from https://www.met.ie/about-us/faq
        description_dict = {
                                0: "", # "error" in the docs
                                1: "Sunny",
                                2: "Fair",
                                3: "Partly cloudy",
                                4: "Cloudy",
                                5: "Light rain showers",
                                6: "Rain showers with thunder",
                                7: "Sleet with sun",
                                8: "Snow showers",
                                9: "Light rain/drizzle",
                                10: "Rain",
                                11: "Heavy rain and thunder",
                                12: "Sleet",
                                13: "Snow",
                                14: "Snow and thunder",
                                15: "Fog",
                                20: "Sleet showers and thunder",
                                21: "Snow showers and thunder",
                                22: "Rain and thunder",
                                23: "Sleet and thunder",
                                24: "Light rain showers and thunder",
                                25: "Heavy rain showers and thunder",
                                26: "Light sleet showers and thunder",
                                27: "Heavy sleet showers and thunder",
                                28: "Light snow showers and thunder",
                                29: "Heavy snow showers and thunder",
                                30: "Light rain and thunder",
                                31: "Light sleet and thunder",
                                32: "Heavy sleet and thunder",
                                33: "Light snow and thunder",
                                34: "Heavy snow and thunder",
                                40: "Drizzle",
                                41: "Light rain showers",
                                42: "Light sleet showers",
                                43: "Heavy sleet showers",
                                44: "Light snow showers",
                                45: "Heavy snow showers",
                                46: "Drizzle",
                                47: "Light sleet",
                                48: "Heavy sleet",
                                49: "Light snow",
                                50: "Heavy snow"

                            }
        description = description_dict[weathercode]

        logging.debug(
            "get_description_by_weathercode({}) - {}"
            .format(weathercode, description))

        return description.title()


    def hour_offset_from_now(self, h):
        selected_hour = datetime.datetime.utcnow() + timedelta(hours=h)
        return selected_hour.strftime("%Y-%m-%dT%H:00:00Z")

    # Get weather from Met Eireann's open data API:
    # https://data.gov.ie/dataset/met-eireann-weather-forecast-api
    def get_weather(self):
        url = ("http://openaccess.pf.api.met.ie/metno-wdb2ts/locationforecast?lat={};long={}"
               .format(self.location_lat, self.location_long))

        root = self.get_response_xml(url)

        # the document contains the next day's forecast, in 24 hour-offset datapoints (as
        # well as longer term forecasts, but we only want the next day).
	    # scan across the next 24 hours looking for high and low temperatures
        temps = []
        codes = []
        rain = []
        rainMill = []
        for h in range(11):
            hour_string = self.hour_offset_from_now(h-1)
            for t in root.findall("./product/time[@from='%s']/location/temperature" % (hour_string)):
                temps.append(float(t.get("value")))
            for sym in root.findall("./product/time[@from='%s']/location/symbol" % (hour_string)):
                codes.append(int(sym.get("number")))
            for r in root.findall("./product/time[@from='%s']/location/precipitation" % (hour_string)):
                rain.append(float(r.get("probability")))
            for m in root.findall("./product/time[@from='%s']/location/precipitation" % (hour_string)):
                rainMill.append(float(m.get("value")))

        temperatureNow = temps[0]
        temperaturePlus1 = temps[1]
        temperaturePlus2 = temps[2]
        temperaturePlus3 = temps[3]
        temperaturePlus4 = temps[4]
        temperaturePlus5 = temps[5]
        temperaturePlus6 = temps[6]
        temperaturePlus7 = temps[7]
        temperaturePlus8 = temps[8]

        rainNow = rain[0]
        rainPlus1 = rain[1]
        rainPlus2 = rain[2]
        rainPlus3 = rain[3]
        rainPlus4 = rain[4]
        rainPlus5 = rain[5]
        rainPlus6 = rain[6]
        rainPlus7 = rain[7]
        rainPlus8 = rain[8]

        rainMillNow = rainMill[0]
        rainMillPlus1 = rainMill[1]
        rainMillPlus2 = rainMill[2]
        rainMillPlus3 = rainMill[3]
        rainMillPlus4 = rainMill[4]
        rainMillPlus5 = rainMill[5]
        rainMillPlus6 = rainMill[6]
        rainMillPlus7 = rainMill[7]
        rainMillPlus8 = rainMill[8]

        temps.sort()
        temperatureMin = temps[0]
        temperatureMax = temps[-1]

        # unfortunately, there's no daily summary field in the document; instead,
	    # get the symbol for just under 1 hour from now (so it's a very near-term
        # forecast!).  TODO: maybe more than 1 hour would be better?
        hour_string = self.hour_offset_from_now(1)
        for sym in root.findall("./product/time[@from='%s']/location/symbol" % (hour_string)):
            weather_code = int(sym.get("number"))

#        daytime = self.is_daytime(self.location_lat, self.location_long)
#        daytime = True
        weather = {}
        weather["temperatureMin"] = temperatureMin if self.units == "metric" else self.c_to_f(temperatureMin)
        weather["temperatureMax"] = temperatureMax if self.units == "metric" else self.c_to_f(temperatureMax)
        weather["temperatureNow"] = temperatureNow if self.units == "metric" else self.c_to_f(temperatureNow)
        weather["temperaturePlus1"] = temperaturePlus1 if self.units == "metric" else self.c_to_f(temperaturePlus1)
        weather["temperaturePlus2"] = temperaturePlus2 if self.units == "metric" else self.c_to_f(temperaturePlus2)
        weather["temperaturePlus3"] = temperaturePlus3 if self.units == "metric" else self.c_to_f(temperaturePlus3)
        weather["temperaturePlus4"] = temperaturePlus4 if self.units == "metric" else self.c_to_f(temperaturePlus4)
        weather["temperaturePlus5"] = temperaturePlus5 if self.units == "metric" else self.c_to_f(temperaturePlus5)
        weather["temperaturePlus6"] = temperaturePlus6 if self.units == "metric" else self.c_to_f(temperaturePlus6)
        weather["temperaturePlus7"] = temperaturePlus7 if self.units == "metric" else self.c_to_f(temperaturePlus7)
        weather["temperaturePlus8"] = temperaturePlus8 if self.units == "metric" else self.c_to_f(temperaturePlus8)
        weather["icon"] = self.get_icon_from_met_eireann_weathercode(codes[0])
        weather["iconPlus1"] = self.get_icon_from_met_eireann_weathercode(codes[1])
        weather["iconPlus2"] = self.get_icon_from_met_eireann_weathercode(codes[2])
        weather["iconPlus3"] = self.get_icon_from_met_eireann_weathercode(codes[3])
        weather["iconPlus4"] = self.get_icon_from_met_eireann_weathercode(codes[4])
        weather["iconPlus5"] = self.get_icon_from_met_eireann_weathercode(codes[5])
        weather["iconPlus6"] = self.get_icon_from_met_eireann_weathercode(codes[6])
        weather["iconPlus7"] = self.get_icon_from_met_eireann_weathercode(codes[7])
        weather["iconPlus8"] = self.get_icon_from_met_eireann_weathercode(codes[8])
        weather["rainNow"] = rainNow
        weather["rainPlus1"] = rainPlus1
        weather["rainPlus2"] = rainPlus2
        weather["rainPlus3"] = rainPlus3
        weather["rainPlus4"] = rainPlus4
        weather["rainPlus5"] = rainPlus5
        weather["rainPlus6"] = rainPlus6
        weather["rainPlus7"] = rainPlus7
        weather["rainPlus8"] = rainPlus8
        weather["rainMillNow"] = rainMillNow
        weather["rainMillPlus1"] = rainMillPlus1
        weather["rainMillPlus2"] = rainMillPlus2
        weather["rainMillPlus3"] = rainMillPlus3
        weather["rainMillPlus4"] = rainMillPlus4
        weather["rainMillPlus5"] = rainMillPlus5
        weather["rainMillPlus6"] = rainMillPlus6
        weather["rainMillPlus7"] = rainMillPlus7
        weather["rainMillPlus8"] = rainMillPlus8
        weather["description"] = self.get_description_from_met_eireann_weathercode(weather_code)
        logging.debug(weather)
        return weather

