""" 
TITLE: A python program for checking a location's weather

NOTE: Before running this demo, install the necessary dependencies: geopy and requests
"""

from geopy.geocoders import Nominatim
import requests

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",

    45: "Fog",
    48: "Depositing rime fog",

    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",

    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",

    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",

    66: "Light freezing rain",
    67: "Heavy freezing rain",

    71: "Slight snowfall",
    73: "Moderate snowfall",
    75: "Heavy snowfall",

    77: "Snow grains",

    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",

    85: "Slight snow showers",
    86: "Heavy snow showers",

    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}

print("\t\t\t\t\t WEATHER APP")
city = input("Enter a City/location: ")

# Geocode the location
geolocator = Nominatim(user_agent="space_club_demo")
location = geolocator.geocode(city)

if location is None:
    print("Location not found.")
    exit()

lat = location.latitude
lon = location.longitude

print(f"Latitude: {lat}")
print(f"Longitude: {lon}")

# Fetch weather
url = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={lat}&longitude={lon}"
    "&current=temperature_2m,relative_humidity_2m,"
    "apparent_temperature,wind_speed_10m,weather_code"
)

weather = requests.get(url).json()["current"]

print(f"\nWeather for {city}")
print(f"Temperature: {weather['temperature_2m']} °C")
print(f"Feels like: {weather['apparent_temperature']} °C")
print(f"Humidity: {weather['relative_humidity_2m']} %")
print(f"Wind speed: {weather['wind_speed_10m']} km/h")
print(f"Weather code: {weather['weather_code']} ({WEATHER_CODES.get(weather['weather_code'],'Unknown code')})")