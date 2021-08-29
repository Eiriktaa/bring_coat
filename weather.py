import json, datetime, os, requests

# Ping service
from discord import Webhook, RequestsWebhookAdapter

workdir = os.path.dirname(__file__)
datafile = os.path.join(workdir, "weather.data")
dateformat_string = "%Y-%m-%dT%H:%M:%SZ"
now = datetime.datetime.today()
expected_amount_of_rain = 0


def getWeatherData():
    url = "https://api.met.no/weatherapi/locationforecast/2.0/compact"

    headers = {"User-agent": "Should_i_bring_coat_app"}

    query = {"lat": 59.94, "lon": 10.71}

    res = requests.get(url, params=query, headers=headers)
    return res.json()


def load_weather_data():

    # with open(datafile, "w") as data_file:
    #    data_file.write(json.dumps(getWeatherData(), indent=4))

    with open(datafile) as data_file:
        return json.load(data_file)


weather_JSON_Data = load_weather_data()


def notify_on_rain(expected_amount_of_rain):
    hook = Webhook.from_url(os.getenv("PING_WEBHOOK"), adapter=RequestsWebhookAdapter())
    hook.send(
        f"Expecting {expected_amount_of_rain} mm of rain, consider bringing a coat"
    )


# Searches the data set looking for rain.
for data_series in weather_JSON_Data["properties"]["timeseries"]:
    if "next_1_hours" in data_series["data"]:
        print(data_series)
        weather_time = datetime.datetime.strptime(
            data_series["time"], dateformat_string
        )
        delta = weather_time - now
        print(weather_time)
        # Finds the weather data in a time period given below
        tracked_hours = 14
        if delta.seconds / 3600 < tracked_hours and delta.days >= 0 and delta.days < 1:
            # Tracks through json to find the amount expecxted of rain.
            print(data_series["time"])
            rain_amount = data_series["data"]["next_1_hours"]["details"][
                "precipitation_amount"
            ]
            expected_amount_of_rain += rain_amount

if expected_amount_of_rain > 1:
    notify_on_rain(expected_amount_of_rain)
