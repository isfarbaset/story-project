import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
from sklearn.linear_model import LinearRegression

# Load the cleaned datasets
historic_data = pd.read_csv('./data/clean-data/historic_data_cleaned.csv')
nearterm_data = pd.read_csv('./data/clean-data/nearterm_data_cleaned.csv')

# Combine datasets for some visualizations
combined_data = pd.concat([historic_data, nearterm_data])

# Group by year and calculate the average values for Tmax_Summer and VWC_Summer_whole
average_data = combined_data.groupby('year').agg({'Tmax_Summer': 'mean', 'VWC_Summer_whole': 'mean'}).reset_index()

# Create the scatter plot to show the relationship between Tmax_Summer and VWC_Summer_whole
fig = px.scatter(average_data, x='Tmax_Summer', y='VWC_Summer_whole',
                 trendline='ols',  # Add a trendline
                 title='Relationship Between Summer Maximum Temperature and Soil Moisture',
                 labels={'Tmax_Summer': 'Maximum Summer Temperature (°C)', 'VWC_Summer_whole': 'Average Soil Moisture (%)'})

# Update layout for better aesthetics
fig.update_layout(
    title_font=dict(size=18, family='Arial, sans-serif'),
    xaxis_title='Maximum Summer Temperature (°C)',
    yaxis_title='Average Soil Moisture (%)',
    width=800,
    height=600
)

# Extracting the relevant column for VWC_Summer_whole analysis
historic_soil_data_vwc = historic_data[['year', 'VWC_Summer_whole']]
nearterm_soil_data_vwc = nearterm_data[['year', 'VWC_Summer_whole']]
combined_soil_data_vwc = pd.concat([historic_soil_data_vwc, nearterm_soil_data_vwc])
combined_soil_data_vwc_aggregated = combined_soil_data_vwc.groupby('year').mean().reset_index()

# Extracting the relevant column for DrySoilDays_Summer_whole analysis
historic_soil_data_dry = historic_data[['year', 'DrySoilDays_Summer_whole']]
nearterm_soil_data_dry = nearterm_data[['year', 'DrySoilDays_Summer_whole']]
combined_soil_data_dry = pd.concat([historic_soil_data_dry, nearterm_soil_data_dry])
combined_soil_data_dry_aggregated = combined_soil_data_dry.groupby('year').mean().reset_index()

# Function to calculate trendline
def calculate_trendline(x, y):
    model = LinearRegression()
    x_reshaped = np.array(x).reshape(-1, 1)
    model.fit(x_reshaped, y)
    trend = model.predict(x_reshaped)
    return trend

# Calculate trendline for VWC_Summer_whole
vwc_trend = calculate_trendline(combined_soil_data_vwc_aggregated['year'], combined_soil_data_vwc_aggregated['VWC_Summer_whole'])

# Determine the y-axis range to better show changes in moisture levels
y_min = combined_soil_data_vwc_aggregated['VWC_Summer_whole'].min() - 0.005
y_max = combined_soil_data_vwc_aggregated['VWC_Summer_whole'].max() + 0.005

# Create the first area chart for VWC_Summer_whole with trendline
fig1 = go.Figure(
    data=[
        go.Scatter(
            x=combined_soil_data_vwc_aggregated['year'],
            y=combined_soil_data_vwc_aggregated['VWC_Summer_whole'],
            fill='tozeroy',
            name='Soil Moisture in Summer',
            mode='none',
            fillcolor='#003c54'
        ),
        go.Scatter(
            x=combined_soil_data_vwc_aggregated['year'],
            y=vwc_trend,
            mode='lines',
            name='Trendline',
            line=dict(color='red', dash='dash')
        )
    ],
    layout=dict(
        title='Soil Moisture in Summer Trend',
        xaxis_title='Year',
        yaxis_title='Soil Moisture (%)',
        yaxis=dict(range=[y_min, y_max], tickfont=dict(size=14)),  # Set the y-axis range
        title_font=dict(size=18, family='Arial, sans-serif'),
        xaxis=dict(tickfont=dict(size=14)),
        width=800,
        height=600,
        plot_bgcolor='#f7f7f7',
        hoverlabel=dict(font_size=16),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='top',
            y=-0.2,
            xanchor='center',
            x=0.5
        )
    )
)

# Display the first plot
fig1.show()

# Calculate trendline for DrySoilDays_Summer_whole
dry_soil_trend = calculate_trendline(combined_soil_data_dry_aggregated['year'], combined_soil_data_dry_aggregated['DrySoilDays_Summer_whole'])

# Create the second area chart for DrySoilDays_Summer_whole with trendline
fig2 = go.Figure(
    data=[
        go.Scatter(
            x=combined_soil_data_dry_aggregated['year'],
            y=combined_soil_data_dry_aggregated['DrySoilDays_Summer_whole'],
            fill='tozeroy',
            name='Dry Soil Days in Summer',
            mode='none',
            fillcolor='rgba(165,42,42,0.5)'
        ),
        go.Scatter(
            x=combined_soil_data_dry_aggregated['year'],
            y=dry_soil_trend,
            mode='lines',
            name='Trendline',
            line=dict(color='blue', dash='dash')
        )
    ],
    layout=dict(
        title='Dry Soil Days in Summer Trend',
        xaxis_title='Year',
        yaxis_title='Dry Soil Days',
        title_font=dict(size=18, family='Arial, sans-serif'),
        xaxis=dict(tickfont=dict(size=14)),
        yaxis=dict(tickfont=dict(size=14)),
        width=800,
        height=600,
        plot_bgcolor='#f7f7f7',
        hoverlabel=dict(font_size=16),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='top',
            y=-0.2,
            xanchor='center',
            x=0.5
        )
    )
)

# Display the second plot
fig2.show()