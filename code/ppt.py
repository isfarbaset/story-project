import pandas as pd
import plotly.express as px
import numpy as np
import plotly.express as px
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load the cleaned datasets
historic_data_1 = pd.read_csv('./data/clean-data/historic_data_cleaned.csv')
nearterm_data_1 = pd.read_csv('./data/clean-data/nearterm_data_cleaned.csv')

# Combine datasets for some visualizations
combined_data_1 = pd.concat([historic_data_1, nearterm_data_1])

# Calculate the center of the map
center_lat_1 = combined_data_1['lat'].mean()
center_long_1 = combined_data_1['long'].mean()

# Function to calculate an appropriate zoom level based on the spread of data points
def calculate_zoom_level_1(latitudes_1, longitudes_1):
    max_lat_1, min_lat_1 = np.max(latitudes_1), np.min(latitudes_1)
    max_long_1, min_long_1 = np.max(longitudes_1), np.min(longitudes_1)
    lat_diff_1 = max_lat_1 - min_lat_1
    long_diff_1 = max_long_1 - min_long_1
    max_diff_1 = max(lat_diff_1, long_diff_1)
    
    if max_diff_1 < 0.01:
        return 15
    elif max_diff_1 < 0.1:
        return 12
    elif max_diff_1 < 1:
        return 10
    elif max_diff_1 < 10:
        return 8
    else:
        return 6

# Calculate zoom level (but we will manually adjust it for more zoom)
zoom_level_1 = calculate_zoom_level_1(combined_data_1['lat'], combined_data_1['long'])

# Manually adjust zoom level for a more zoomed-in view
zoom_level_1 = zoom_level_1 * 0.95  # Increase the zoom factor

# Set Mapbox access token
px.set_mapbox_access_token("pk.eyJ1IjoiaXNmYXJiYXNldCIsImEiOiJjbHdiOWVtY2IwbGxsMmtraHZoYnB1YTMwIn0.10XSE1rNVsmXSnFmYYa0Cw")

# Create the Plotly scatter_mapbox map with enhanced aesthetics and detailed map layers
map_fig_1 = px.scatter_mapbox(combined_data_1, lon='long', lat='lat', color='PPT_Summer',
                              hover_data={'PPT_Summer': ':.2f', 'lat': ':.2f', 'long': ':.2f', 'year': True}, size='PPT_Summer',
                              labels={'PPT_Summer': 'summer precipitation', 'lat': 'latitude', 'long': 'longitude'},
                              animation_frame='year', title='Geospatial Distribution of Summer Precipitation Over Time',
                              color_continuous_scale=px.colors.sequential.Viridis_r, size_max=15, zoom=zoom_level_1,
                              center={"lat": center_lat_1, "lon": center_long_1}
                              )

# Update the layout for better aesthetics and visibility of state lines
map_fig_1.update_layout(
    mapbox_style="carto-positron",  # Change the map style to show more details
    mapbox=dict(
        center=dict(lat=center_lat_1, lon=center_long_1),
        zoom=zoom_level_1,  # Adjusted zoom level
    ),
    title_font=dict(size=18, family='Arial, sans-serif'),  
    title_x=0.5,
    coloraxis_colorbar=dict(
        title="Summer Precipitation (inches)",
        title_side="right",  # Align the title horizontally with the colorbar
        title_font=dict(size=14)  # Adjust the font size as needed
    ),
    autosize=True,
    width=750,  # Increase the width of the map
    height=700   # Increase the height of the map
)

# Load the cleaned datasets
historic_data_1 = pd.read_csv('./data/clean-data/historic_data_cleaned.csv')
nearterm_data_1 = pd.read_csv('./data/clean-data/nearterm_data_cleaned.csv')

# Combine datasets for some visualizations
combined_data_1 = pd.concat([historic_data_1, nearterm_data_1])

# Extracting the relevant column for analysis
historic_ppt_data = historic_data_1[['year', 'PPT_Summer']]
nearterm_ppt_data = nearterm_data_1[['year', 'PPT_Summer']]

# Merging both datasets for a comprehensive analysis
combined_ppt_data = pd.concat([historic_ppt_data, nearterm_ppt_data])

# Aggregating the data by year using the mean
combined_ppt_data_aggregated = combined_ppt_data.groupby('year').mean().reset_index()

# Setting the style of the plot
sns.set_theme(style="whitegrid")

# Plotting the PPT_Summer over the years with enhancements and a trendline
plt.figure(figsize=(16, 9))
sns.lineplot(data=combined_ppt_data_aggregated, x='year', y='PPT_Summer', marker='o', color='navy', linewidth=2.5, label='Summer Precipitation')
sns.regplot(data=combined_ppt_data_aggregated, x='year', y='PPT_Summer', scatter=False, color='#4682B4', ci=None, line_kws={"linewidth":2.5, "linestyle":"--"}, label='Trendline')

# Adding titles and labels with enhanced aesthetics
plt.title('Summer Precipitation Trend\n in Southeastern Utah', fontsize=32)
plt.xlabel('Year', fontsize=25, weight='bold')
plt.ylabel('Summer Precipitation (inches)', fontsize=25, weight='bold')

# Setting the x-axis range from 1980 to 2024
_ = plt.xlim(1980, 2024)

# Adding a grid with customized appearance
_ = plt.grid(True, linestyle='--', linewidth=0.7, alpha=0.7)

# Enhancing the tick labels for better readability
_ = plt.xticks(fontsize=20)
_ = plt.yticks(fontsize=20)

# Adding a light background color to the plot area
plt.gca().set_facecolor('#f7f7f7')

# Removing the top and right spines for a cleaner look
sns.despine()

# Adding legend
_ = plt.legend(fontsize=20)

# Display the plot
plt.show()