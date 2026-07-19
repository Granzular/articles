"""
TITLE: A weather plot simulation using dummy data

NOTE: Before running this demo, install the necessary dependencies: numpy and matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt

# Step 1: Mock Infrared Brightness Temperature grid (in Kelvin)
# Warmer values (280K+) are land/sea. Freezing values (sub-230K) are high storm clouds.
weather_grid = np.array([
    [285, 284, 280, 278, 281],
    [283, 220, 215, 275, 280],
    [281, 210, 195, 225, 279],
    [284, 230, 218, 270, 282],
    [286, 285, 281, 279, 283]
])

print("🛰️ Weather Grid Received. Analyzing for high-altitude storm clouds...")

# Step 2: Process the grid to find severe weather warnings
rows, cols = weather_grid.shape
for r in range(rows):
    for c in range(cols):
        temp_k = weather_grid[r, c]
        if temp_k < 230:  # Below -43 degrees Celsius (Severe thunderstorm threshold)
            print(f"Warning: Severe Storm cloud detected at Grid Sector [{r}, {c}] ({temp_k} K)")

# Step 3: Visualize the satellite imagery
plt.figure(figsize=(6, 5))
plt.imshow(weather_grid, cmap='winter', origin='upper')
plt.colorbar(label="Temperature (Kelvin)")
plt.title("GOES-R Satellite Infrared Channel")
plt.xlabel("West -> East Grid")
plt.ylabel("North -> South Grid")
plt.show()