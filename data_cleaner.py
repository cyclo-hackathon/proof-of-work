import json
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
import numpy as np

raw_traffic_data = json.load(open("Traffic_Volume.geojson", "rb"))
raw_road_data = raw_traffic_data["features"]

# Format: latitude, longitude, AADT / number of coordinate points
formatted_road_data = []
for road in raw_road_data:
    average_vehicles_per_year_on_road = road["properties"]["ALLVEHS_AADT"]
    road_coordinates = road["geometry"]["coordinates"]

    # why is the data format inconsistent
    if type(road_coordinates[0][0]) == list:
        fixed_coordinates = []
        for coordinates in road_coordinates:
            fixed_coordinates += coordinates
        road_coordinates = fixed_coordinates

    for coordinate in road_coordinates:
        latitude, longitude = coordinate
        formatted_road_data.append((latitude, longitude, average_vehicles_per_year_on_road / len(road_coordinates)))

formatted_road_data = np.array(formatted_road_data)

# Keep only part of the data before making the plot to minimise lag in debugging
# formatted_road_data = formatted_road_data[::5]

# Plot vehicle usage on roads
latitudes = formatted_road_data[:, 0]
longitudes = formatted_road_data[:, 1]
vehicle_count = formatted_road_data[:, 2]

plt.scatter(latitudes, longitudes, vehicle_count * 0.001)
plt.show()
