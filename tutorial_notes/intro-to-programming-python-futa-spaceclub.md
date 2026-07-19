## Table Of Content
 **Module A - INTRO:**
- What is programming?
- How does programming apply to space science? (the different areas of application)
- How Python fits into the picture (including python libraries that make it possible)

**Module B - INTRO TO PYTHON:**
- A very brief history on python
- setting up development environment
- variables and data types and comments
- control statements: conditionals and loops
- modularity: functions and modules

**Module C - Live Demo**
- ISS and satellite tracker
- another demo

**CONCLUSION AND NEXT STEPS:**




# Lecture Notes: Python for Space Exploration

---

# MODULE A: INTRODUCTION TO PROGRAMMING

## 1. What is Programming?
At its core, programming is writing a sequence of precise, logical instructions for a computer to execute. This precise logical instruction is what we call a **computer program**.  
In aerospace, a computer cannot "guess" your intent. If you tell a rocket thruster to fire for `1.0` seconds instead of `0.1` seconds, the mission fails. Programming is how we translate human physics and logic into machine-executable actions.

---

## 2. Python in Space Science (Areas of Application)
Python is the space industry's favorite tool because of its massive library ecosystem. Here is how it is applied:

### A. Data Analysis & Astrophysics
Space telescopes (like James Webb) and planetary rovers send back gigabytes of raw, noisy binary data. Python is used to clean this data, filter out noise, and detect stellar objects.
* **Libraries:** `NumPy` (fast math arrays), `Pandas` (handling telemetry tables), `Astropy` (coordinates, time systems, and astronomical calculations).

### B. Astrodynamics & Orbit Propagation
Calculating trajectories to Mars or managing satellite constellations requires solving complex gravitational differential equations.
* **Libraries:** `SciPy` (calculus & equation solvers), `Poliastro` (astrodynamics and orbital mechanics plotting).

### C. Earth Observation & Computer Vision
Satellite imagery is used to monitor climate change, track forest fires, and map terrain.
* **Libraries:** `OpenCV` (image processing), `Rasterio` (handling geospatial satellite data).

### D. Ground Segment Control & APIs
Retrieving live spacecraft telemetry, sending ground station commands, and parsing communication packets.
* **Libraries:** `requests` (talking to web APIs), `socket` (network programming).

---

# MODULE B: INTRO TO PYTHON (HANDS-ON)


## 1. A Brief History of Python
* **What is it?** Python is a high-level dynamically typed, interpreted language created by Guido van Rossum in 1991.
* **Why space clubs love it:** It reads almost like English, allowing aerospace students to focus on solving physics/engineering problems rather than fighting complex syntax (like C++ memory pointers).

---

## 2. Variables, Data Types, & Comments
Variables are named storage for data.  
There are 8 main categories of data in python. They are:  

**Numeric:**
- `int`
- `float`  
- `complex`  

**Text:**
- `str`  

**Sequence:**
- `list`
- `tuple`
- `range`  

**Mapping:**
- `dict`

**Set:**
- `set`
- `frozenset`

**Boolean**
- `bool`

**Binary**
- `bytes`
- `bytearray`
- `memoryview`

**None**
- `None`



```python
""" 
This is a multi line comment or a doc string.
"""
# This is a comment. Python ignores this. Use it to explain your math!

# NUMERIC
active_satellites = 7500        # int: number of active satellite
orbital_altitude_km = 408.8  # float: ISS altitude in km
phase_shift = 1 + 2j         # complex: signal phase in comms


# TEXT
satellite_name = "ISS"       # str: String

# SEQUENCE
location_list = ["lagos","Akure","Kaduna"]
coordinates = (28.5, -80.6)
orbit_numbers = range(1,11)

# MAPPING
telemetry  = {"temp": -40, "battery_volt": 28.5, "status":"nominal"}    # dict: sensor readings

# SET 
active_sensors = {"accelerometer","gyro","sun_sensor"} # set
locked_constellations = frozenset(["Galileo","Orion","BeiDou"]) # frozenset: immutable

# BOOLEAN
thrusters_active = True
docking_complete = False

# BINARY
packet = b"Hello World" # byte : telemetry data
buffer = bytearray(b"CMD_START") # bytearray: mutable command buffer
frame_view = memoryview(buffer) #  memoryview: zero-copy view for fast byte slicing

# NONE TYPE
last_contact = None # None: placeholder until ground station connects

# Simple math application: Calculate speed (Distance / Time)
distance_km = 42000
time_hours = 1.5
velocity_kmh = distance_km / time_hours
print(velocity_kmh)
```
> **NOTE**: Use type() function to check for the type of a  variable.  
**TIP**: Always use meaningful variable names whereever possible

---

## 3. Control Statements: Conditionals & Loops
In space, code must adapt to changing telemetry in real-time.

### Conditionals (`if`, `elif`, `else`)
How a satellite decides if its battery power is safe or critical:

```python
battery_charge = 15.5  # Percentage of battery remaining

if battery_charge < 10.0:
    print("CRITICAL: Entering safe mode. Power down instruments!")
elif battery_charge < 30.0:
    print("WARNING: Power low. Disable non-essential payloads.")
else:
    print("SAFE: Power levels nominal. Science operations active.")
```

### Loops (`for`, `while`)
Rovers collect hundreds of temperature sensor readings. We use loops to scan through them instantly.

```python
# A list of temperature readings (in Celsius) from a Martian rover wheel
wheel_temps = [22.4, 25.1, 48.9, 120.3, 18.2]

# Print warning if any sensor exceeds 50°C
for temp in wheel_temps:
    if temp > 50.0:
        print(f"Alert: Wheel heating anomaly detected! {temp}°C")
```

---

## 4. Modularity: Functions & Modules
Don't rewrite physics equations. Package them into reusable functions, or import them from modules.

### Writing a Function

```python
# Function to convert orbital height to a rough atmospheric density class
def get_orbit_layer(altitude):
    if altitude < 100:
        return "Troposphere/Mesosphere (Burn up risk)"
    elif altitude <= 2000:
        return "LEO (Low Earth Orbit)"
    else:
        return "MEO/GEO (Medium/Geostationary Orbit)"

# Testing the function
layer = get_orbit_layer(408.8)
print(f"The ISS is in: {layer}")
```

### Importing Modules
Instead of writing the mathematical value of Pi (π) or gravity constants from scratch, we import them:

```python
import math

# Calculate the circumference of a circular orbit (2 * pi * r)
earth_radius_km = 6371.0
orbit_radius = earth_radius_km + 408.8  # Radius from Earth's center

orbit_circumference = 2 * math.pi * orbit_radius
print(f"Orbit Circumference: {orbit_circumference:.2f} km")
```

---

# MODULE C: LIVE DEMOS (THE HOOK)


## Demo 1: Live ISS Tracker & Reverse Geocoder
This demo queries the live position of the ISS, extracts the Latitude/Longitude, and uses a database to name the country it is flying over.  
**dependencies**: `requests`, `geopy`  
**installation**: 
> pip install requests geopy

```python
import requests
from geopy.geocoders import Nominatim
import time

# Step 1: Fetch ISS data from Open Notify API
url = "http://api.open-notify.org/iss-now.json"
data = requests.get(url).json()

lat = data['iss_position']['latitude']
lon = data['iss_position']['longitude']

cnt =  3  # number of times we want to query
print("\t\t\t\t\tISS TRACKER\n")
while(cnt > 0):
    print(f"📡 Current ISS Coordinates: Lat {lat}, Lon {lon}")

    # Step 2: Convert coordinates to a named location
    geolocator = Nominatim(user_agent="space_club_tracker")
    try:
        location = geolocator.reverse(f"{lat}, {lon}", timeout=5)
        if location:
            print(f"🌍 The ISS is flying over: {location.address}")
        else:
            print("🌊 The ISS is currently flying over an ocean.")
    except Exception:
        print("🌍 Location lookup failed (Network timeout/unpopulated area).")
    
    cnt -= 1        # decreament the counter
    print("\n")     # newline
    time.sleep(2)
print("Tracking Done")
```

## Demo 2: Live Weather App
```python
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

```
---

# CONCLUSION & NEXT STEPS

Keep experimenting and learning!
## Learning Material
* **Python Tutorial on GeeksForGeeks:** [click here](https://www.geeksforgeeks.org/python/python-programming-language-tutorial/)
* **Python for aerospace for beginners**: [on Youtube](https://youtu.be/V4jXVrUJsfM?si=UNRjbLbmJe4gx4FD)  

## Further Resources
* **Astropy Tutorials:** [learn.astropy.org](https://learn.astropy.org) — Official astronomy tasks using Python.
* **NASA APIs:** [api.nasa.gov](https://api.nasa.gov) — Access actual rover photos and asteroid tracking data for free.
* **Open-Source Satellite Tracking:** Look up the `skyfield` Python library to learn how to predict orbits mathematically using TLE orbit datasets.