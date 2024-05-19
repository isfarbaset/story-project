import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np

# Load the cleaned datasets
historic_data = pd.read_csv('../../data/clean-data/historic_data_cleaned.csv')
nearterm_data = pd.read_csv('../../data/clean-data/nearterm_data_cleaned.csv')

# Combine datasets for some visualizations
combined_data = pd.concat([historic_data, nearterm_data])

# Calculate the center of the map
center_lat = combined_data['lat'].mean()
center_long = combined_data['long'].mean()

# Function to calculate an appropriate zoom level based on the spread of data points
def calculate_zoom_level(latitudes, longitudes):
    max_lat, min_lat = np.max(latitudes), np.min(latitudes)
    max_long, min_long = np.max(longitudes), np.min(longitudes)
    lat_diff = max_lat - min_lat
    long_diff = max_long - min_long
    max_diff = max(lat_diff, long_diff)
    
    if max_diff < 0.01:
        return 15
    elif max_diff < 0.1:
        return 12
    elif max_diff < 1:
        return 10
    elif max_diff < 10:
        return 8
    else:
        return 6

# Calculate zoom level (but we will manually adjust it for more zoom)
zoom_level = calculate_zoom_level(combined_data['lat'], combined_data['long'])

# Manually adjust zoom level for a more zoomed-in view
zoom_level = zoom_level * 0.95  # Increase the zoom factor

# Create the Plotly scatter_mapbox map with enhanced aesthetics and detailed map layers
map_fig = px.scatter_mapbox(combined_data, lon='long', lat='lat', color='treecanopy',
                            hover_data={'treecanopy': ':.2f', 'lat': ':.2f', 'long': ':.2f', 'year': True}, size='treecanopy',
                            labels={'treecanopy': 'tree canopy', 'lat': 'latitude', 'long': 'longitude'},
                            animation_frame='year', title='Geospatial Distribution of Tree Canopy Over Time',
                            color_continuous_scale=px.colors.sequential.Sunsetdark, size_max=15, zoom=zoom_level,
                            center={"lat": center_lat, "lon": center_long})

# Update the layout for better aesthetics and visibility of state lines
map_fig.update_layout(
    mapbox_style="carto-positron",  # Change the map style to show more details
    mapbox=dict(
        center=dict(lat=center_lat, lon=center_long),
        zoom=zoom_level,  # Adjusted zoom level
    ),
    title_font=dict(size=18, family='Arial, sans-serif'),  
    title_x=0.5,
    coloraxis_colorbar=dict(
        title="Tree Canopy (%)",
        title_side="right",  # Align the title horizontally with the colorbar
        title_font=dict(size=14)  # Adjust the font size as needed
    ),
    autosize=True,
    width=800,  # Increase the width of the map
    height=700   # Increase the height of the map
)