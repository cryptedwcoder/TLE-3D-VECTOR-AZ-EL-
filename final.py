from skyfield.api import Topos, load, EarthSatellite
import numpy as np
from datetime import datetime, timezone
import plotly.graph_objects as go
import matplotlib.pyplot as plt

def get_satellite_vector_and_angles(lat, lon, alt, date_time, tle_lines):
    # Load ephemeris data
    ts = load.timescale()
    #print(ts)
    t = ts.utc(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second)
    #print(t)

    # Define the satellite using the provided TLE data
    satellite = EarthSatellite(tle_lines[0], tle_lines[1], 'NOAA 17', ts)
    #print(satellite)

    # Define the observer's location
    observer_location = Topos(latitude_degrees=lat, longitude_degrees=lon, elevation_m=alt)

    # Calculate the position of the satellite relative to the observer
    difference = satellite - observer_location
    print(difference)
    topocentric = difference.at(t)
    alt, az, distance = topocentric.altaz()

    # Convert alt/az to a 3D vector
    alt_rad = np.radians(alt.degrees)
    az_rad = np.radians(az.degrees)
    x = distance.km * np.cos(alt_rad) * np.cos(az_rad)
    y = distance.km * np.cos(alt_rad) * np.sin(az_rad)
    z = distance.km * np.sin(alt_rad)
    vector = np.array([x, y, z])
    
    return vector, alt.degrees, az.degrees, distance.km

def plot_vector_3d(vector, elevation, azimuth, distance, observer_location):
    fig = go.Figure()

    # Add vector
    fig.add_trace(go.Scatter3d(
        x=[0, vector[0]],
        y=[0, vector[1]],
        z=[0, vector[2]],
        mode='lines+markers',
        marker=dict(size=5, color='red'),
        line=dict(color='blue', width=5),
        name='Vector to NOAA 17'
    ))

    # Add observer marker
    fig.add_trace(go.Scatter3d(
        x=[0],
        y=[0],
        z=[0],
        mode='markers',
        marker=dict(size=8, color='green'),
        name='Observer'
    ))

    # Add satellite marker
    fig.add_trace(go.Scatter3d(
        x=[vector[0]],
        y=[vector[1]],
        z=[vector[2]],
        mode='markers',
        marker=dict(size=8, color='red'),
        name='NOAA 17'
    ))

    # Add annotations for elevation, azimuth, and distance
    fig.add_annotation(
        text=f"Elevation: {elevation:.2f}°<br>Azimuth: {azimuth:.2f}°<br>Distance: {distance:.2f} km",
        showarrow=False,
        xref="paper",
        yref="paper",
        x=0.5,
        y=1,
        xanchor="center",
        yanchor="bottom",
        font=dict(size=14)
    )

    # Add observer and satellite information on the right
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

    fig.add_annotation(
        text="Satellite: NOAA 17",
        showarrow=False,
        xref="paper",
        yref="paper",
        x=1,
        y=2,
        xanchor="left",
        yanchor="middle",
        font=dict(size=14),
        align="left",
        bordercolor="black",
        borderwidth=1
    )

    # Set plot title and labels
    fig.update_layout(
        title='Vector to NOAA 17 Satellite',
        scene=dict(
            xaxis_title='X (km)',
            yaxis_title='Y (km)',
            zaxis_title='Z (km)'
        )
    )

    fig.show()

def plot_vector_2d(azimuth):
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)

    ax.set_title('Top-down View of Vector to NOAA 17', va='bottom')
    ax.annotate(f'Azimuth: {azimuth:.2f}°', xy=(0.5, 1.05), xycoords='axes fraction', ha='center', fontsize=12)

    # Plot the azimuth
    ax.plot(np.radians(azimuth), 1, marker='o', markersize=10, label='NOAA 17')
    ax.annotate('NOAA 17', xy=(np.radians(azimuth), 1), xytext=(np.radians(azimuth), 1.1),
                arrowprops=dict(facecolor='black', shrink=0.05), ha='center')

    ax.legend()
    plt.show()

# Example usage
latitude = 41.0082 # Latitude of the observer
longitude = 28.9784  # Longitude of the observer
altitude = 10  # Altitude of the observer in meters
date_time = datetime(2024, 8, 1, 0, 20, 0, tzinfo=timezone.utc)  # Date and time in UTC

# Provided TLE data for NOAA 17
tle_lines = [
    "1 27453U 02032A   24213.56602493  .00000311  00000-0  15014-3 0  9994",
    "2 27453  98.7648 164.1391 0011700 174.1883 185.9434 14.25628626149270"
]

vector_to_noaa17, elevation, azimuth, distance = get_satellite_vector_and_angles(latitude, longitude, altitude, date_time, tle_lines)
print(f"3D Vector to NOAA 17: {vector_to_noaa17}")
print(f"Elevation: {elevation} degrees")
print(f"Azimuth: {azimuth} degrees")

# Plot the 3D vector with annotations and additional information
plot_vector_3d(vector_to_noaa17, elevation, azimuth, distance, (latitude, longitude, altitude))

# Plot the 2D top-down view on a 360-degree compass
plot_vector_2d(azimuth)
