#!/usr/bin/env python3.7

import iterm2
import json
import requests
import datetime

API_KEY = "KEY"
LOCATION_NAME = "LOCATION"
API_URL = "https://api.openweathermap.org/data/2.5/weather?units=metric&q={0}&appid={1}"
HUMIDITY = "HUMIDITY"
PRESSURE = "PRESSURE"
MAX_TEMPERTUR = "MAX_TEMPERTUR"
MIN_TEMPERTUR = "MIN_TEMPERTUR"
counter = 0


async def main(connection):
    knobs = [
               iterm2.StringKnob("OpenWeatherMap API key", "API_KEY", "", API_KEY),
               iterm2.StringKnob("Location name", "LOCATION_NAME", "", LOCATION_NAME),
               iterm2.CheckboxKnob("Add Humidity", False, HUMIDITY),
               iterm2.CheckboxKnob("Add Pressure", False, PRESSURE),
               iterm2.CheckboxKnob("Add Max Temperatur", False, MAX_TEMPERTUR),
               iterm2.CheckboxKnob("Add Min Temperatur", False, MIN_TEMPERTUR)
            ]
    component = iterm2.StatusBarComponent(
        short_description="Weather",
        detailed_description="This is weather status bar",
        knobs=knobs,
        exemplar="18℃ 🌙",
        update_cadence=50,
        identifier="take.weather"
    )

    # request api
    def request_api(api_key, location):
        url = API_URL.format(location, api_key)
        response = requests.get(url)
        forecast_data = json.loads(response.text)
        if response.status_code == 401:
            return forecast_data
        elif response.status_code == 404:
            return forecast_data

        return forecast_data

    # get icon
    def get_icon(icon_id):

        if icon_id == "01d":
            return "☀️"
        elif icon_id == "01n":
            return "🌙"
        elif icon_id == "02d" or icon_id == "02n" or icon_id == "03d" or icon_id == "03n" or icon_id == "04d" or icon_id == "04n":
            return "☁️"
        elif icon_id == "09d" or icon_id == "09n":
            return "🌧"
        elif icon_id == "10d" or icon_id == "10n":
            return "☔️"
        elif icon_id == "11d" or icon_id == "11n":
            return "⚡️"
        elif icon_id == "13d" or icon_id == "13n":
            return "❄️"
        elif icon_id == "50d" or icon_id == "50n":
            return "🌫️"

    # status result
    def result_status(forecast_data, config):
        degree = forecast_data["main"]["temp"]
        icon = get_icon(forecast_data["weather"][0]["icon"])
        status = "{0}℃ {1}".format(degree, icon)

        if config["humidity"]:
            humidity = forecast_data["main"]["humidity"]
            status = status + " H:{0}%".format(humidity)
        if config["pressure"]:
            pressure = forecast_data["main"]["pressure"]
            status = status + " P:{0}".format(pressure)
        if config["max_temp"]:
            max_temp = forecast_data["main"]["temp_max"]
            status = status + " HT:{0}".format(max_temp)
        if config["min_temp"]:
            min_temp = forecast_data["main"]["temp_min"]
            status = status + " LT:{0}".format(min_temp)

        return status

    # checkbox info
    def get_checkbox_config(knobs):
        humidity = knobs[HUMIDITY]
        pressure = knobs[PRESSURE]
        max_temp = knobs[MAX_TEMPERTUR]
        min_temp = knobs[MIN_TEMPERTUR]

        config = {"humidity": humidity, "pressure": pressure, "max_temp": max_temp, "min_temp": min_temp}

        return config

    @iterm2.StatusBarRPC
    async def weather_component(knobs):
        # global variable
        global counter
        global status
        global forecast_data
        global time

        api_key = knobs[API_KEY]
        location = knobs[LOCATION_NAME]

        if not api_key:
            return "Please set API key"

        if not location:
            return "Please set location name"

        if counter == 0:
            # first excute
            config = get_checkbox_config(knobs)
            forecast_data = request_api(api_key, location)
            print(type(forecast_data["cod"]))
            print(forecast_data["cod"])

            if forecast_data["cod"] == 401:
                return "Invalid API key"
            elif forecast_data["cod"] == "404":
                return forecast_data["message"]

            status = result_status(forecast_data, config)
            time = datetime.datetime.now()
            counter += 1

        else:
            now_time = datetime.datetime.now()
            delta = now_time - time
            config = get_checkbox_config(knobs)
            status = result_status(forecast_data, config)

            # api reuest time 10m
            if int(delta.total_seconds()) > 600:
                delta = now_time - time
                config = get_checkbox_config(knobs)
                forecast_data = request_api(api_key, location)

                if forecast_data["cod"] == 401:
                    return "Invalid API key"
                elif forecast_data["cod"] == "404":
                    return forecast_data["message"]

                status = result_status(forecast_data, config)
                time = datetime.datetime.now()

        return status

    await component.async_register(connection, weather_component)

iterm2.run_forever(main)
