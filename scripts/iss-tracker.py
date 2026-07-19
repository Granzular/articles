"""
TITLE: A basic International Space Station (ISS) Tracker

NOTE: Before running this demo, install the necessary dependencies: geopy and requests
"""

import requests
from geopy.geocoders import Nominatim
import time
from zoneinfo import ZoneInfo
from datetime import datetime

# Step 1: Fetch ISS data from Open Notify API
url = "http://api.open-notify.org/iss-now.json"
data = requests.get(url).json()

lat = data['iss_position']['latitude']
lon = data['iss_position']['longitude']
timestamp = data['timestamp']

cnt =  3  # number of times we want to query
print("\t\t\t\t\tISS TRACKER\n")
while(cnt > 0):
    print(f"timestamp: {datetime.fromtimestamp(timestamp,tz=ZoneInfo("Africa/Lagos"))}")
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