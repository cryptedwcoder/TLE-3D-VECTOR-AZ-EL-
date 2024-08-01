# File path: satellite_vector_plotter.py

from skyfield.api import Topos, load, EarthSatellite
import numpy as np
from datetime import datetime, timezone
import plotly.graph_objects as go
import matplotlib.pyplot as plt

def get_satellite_vector_and_angles(lat, lon, alt, date_time, tle_lines):
    ts = load.timescale()
    t = ts.utc(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second)
    satellite = EarthSatellite(tle_lines[0], tle_lines[1], 'NOAA 17', ts)
    observer_location = Topos(latitude_degrees=lat, longitude_degrees=lon, elevation_m=alt)
    difference = satellite - observer_location
    topocentric = difference.at(t)
    alt, az, distance = topocentric.altaz()
    
    alt_rad = np.radians(alt.degrees)
    az_rad = np.radians(az.degrees)
    x = distance.km * np.cos(alt_rad) * np.cos(az_rad)
    y = distance.km * np.cos(alt_rad) * np.sin(az_rad)
    z = distance.km * np.sin(alt_rad)
    vector = np.array([x, y, z])
    
    return vector, alt.degrees, az.degrees, distance.km

def plot_vectors(vectors, elevations, azimuths, distances, observer_location):
    fig = go.Figure()

    # Add vectors to the plot
    for i, (vector, elevation, azimuth, distance) in enumerate(zip(vectors, elevations, azimuths, distances)):
        fig.add_trace(go.Scatter3d(
            x=[0, vector[0]],
            y=[0, vector[1]],
            z=[0, vector[2]],
            mode='lines+markers',
            marker=dict(size=5, color=f'rgba({i*100}, 0, 0, 0.8)'),
            line=dict(color=f'rgba({i*100}, 0, 0, 0.8)', width=5),
            name=f'Time {i+1}'
        ))

        # Add annotations for elevation, azimuth, and distance
        fig.add_annotation(
            text=f"Time {i+1}:<br>Elevation: {elevation:.2f}°<br>Azimuth: {azimuth:.2f}°<br>Distance: {distance:.2f} km",
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.5,
            y=1 - i * 0.1,
            xanchor="center",
            yanchor="bottom",
            font=dict(size=14)
        )

    # Add observer marker
    fig.add_trace(go.Scatter3d(
        x=[0],
        y=[0],
        z=[0],
        mode='markers',
        marker=dict(size=8, color='green'),
        name='Observer'
    ))

    # Add observer location information
    fig.add_annotation(
        text=f"Observer Location:<br>Lat: {observer_location[0]}°<br>Lon: {observer_location[1]}°<br>Alt: {observer_location[2]} m",
        showarrow=False,
        xref="paper",
        yref="paper",
        x=1,
        y=0.5,
        xanchor="left",
        yanchor="middle",
        font=dict(size=14),
        align="left",
        bordercolor="black",
        borderwidth=1
    )

    # Set plot title and labels
    fig.update_layout(
        title='Vectors to NOAA 17 Satellite at Different Times',
        scene=dict(
            xaxis_title='X (km)',
            yaxis_title='Y (km)',
            zaxis_title='Z (km)'
        )
    )

    fig.show()

def plot_vector_2d(azimuths):
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)

    ax.set_title('Top-down View of Vectors to NOAA 17', va='bottom')
    
    for i, azimuth in enumerate(azimuths):
        ax.annotate(f'Time {i+1}: Azimuth: {azimuth:.2f}°', xy=(0.5, 1.05 - i*0.05), xycoords='axes fraction', ha='center', fontsize=12)
        ax.plot(np.radians(azimuth), 1, marker='o', markersize=10, label=f'Time {i+1}')
        ax.annotate(f'Time {i+1}', xy=(np.radians(azimuth), 1), xytext=(np.radians(azimuth), 1.1),
                    arrowprops=dict(facecolor='black', shrink=0.05), ha='center')

    ax.legend()
    plt.show()

# Example usage
latitude = 41.0082  # Latitude of the observer
longitude = 28.9784  # Longitude of the observer
altitude = 10  # Altitude of the observer in meters
date_time1 = datetime(2024, 8, 1, 0, 18, 0, tzinfo=timezone.utc)  # First date and time in UTC
date_time2 = datetime(2024, 8, 1, 0, 20, 0, tzinfo=timezone.utc)  # Second date and time in UTC

# Provided TLE data for NOAA 17
tle_lines = [
    "1 27453U 02032A   24213.56602493  .00000311  00000-0  15014-3 0  9994",
    "2 27453  98.7648 164.1391 0011700 174.1883 185.9434 14.25628626149270"
]

vector1, elevation1, azimuth1, distance1 = get_satellite_vector_and_angles(latitude, longitude, altitude, date_time1, tle_lines)
vector2, elevation2, azimuth2, distance2 = get_satellite_vector_and_angles(latitude, longitude, altitude, date_time2, tle_lines)

print(f"3D Vector to NOAA 17 at Time 1: {vector1}")
print(f"Elevation at Time 1: {elevation1} degrees")
print(f"Azimuth at Time 1: {azimuth1} degrees")
print(f"Distance at Time 1: {distance1} km")

print(f"3D Vector to NOAA 17 at Time 2: {vector2}")
print(f"Elevation at Time 2: {elevation2} degrees")
print(f"Azimuth at Time 2: {azimuth2} degrees")
print(f"Distance at Time 2: {distance2} km")

# Plot the vectors with annotations
plot_vectors([vector1, vector2], [elevation1, elevation2], [azimuth1, azimuth2], [distance1, distance2], (latitude, longitude, altitude))

# Plot the 2D top-down view on a 360-degree compass
plot_vector_2d([azimuth1, azimuth2])
