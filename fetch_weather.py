import requests
import json

def fetch_weather_data(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data


