import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression

# Load the cleaned datasets
historic_data = pd.read_csv('../../data/clean-data/historic_data_cleaned.csv')
nearterm_data = pd.read_csv('../../data/clean-data/nearterm_data_cleaned.csv')

# Combine datasets for some visualizations
combined_data = pd.concat([historic_data, nearterm_data])

# Prepare data for linear regression
combined_precip = combined_data.dropna(subset=['PPT_Annual'])
X_precip = combined_precip[['year']].values
y_precip = combined_precip['PPT_Annual'].values

# Prepare data for linear regression
combined_temp = combined_data.dropna(subset=['T_Annual'])
X_temp = combined_temp[['year']].values
y_temp = combined_temp['T_Annual'].values

# Aggregate data by year for temperature and precipitation
aggregated_temp = combined_temp.groupby('year').mean().reset_index()
aggregated_precip = combined_precip.groupby('year').mean().reset_index()

# Linear regression analysis for aggregated temperature data
X_temp_agg = aggregated_temp[['year']].values
y_temp_agg = aggregated_temp['T_Annual'].values
model_temp_agg = LinearRegression().fit(X_temp_agg, y_temp_agg)
trend_temp_agg = model_temp_agg.predict(X_temp_agg)
slope_temp_agg = model_temp_agg.coef_[0]
intercept_temp_agg = model_temp_agg.intercept_

# Create the figure for temperature trend
fig_temp = go.Figure(data=[
    go.Scatter(
        x=aggregated_temp['year'], 
        y=aggregated_temp['T_Annual'],
        mode='markers+lines',
        name='Observed',
        hovertemplate='Year: %{x}<br>Avg Temp: %{y:.2f}°C'
    ),
    go.Scatter(
        x=aggregated_temp['year'], 
        y=trend_temp_agg,
        mode='lines',
        name='Trend',
        line=dict(color='red'),
        hovertemplate='Year: %{x}<br>Trend: %{y:.2f}°C'
    )
])

# Update layout for temperature trend
fig_temp.update_layout(
    title='Trend Analysis: Average Annual Temperature in Utah (1980-2024)',
    xaxis_title='Year',
    yaxis_title='Average Temperature (°C)',
    legend_title='',
    template='plotly_white'
)

# Linear regression analysis for aggregated precipitation data with the full range of years
all_years = pd.DataFrame({'year': np.arange(aggregated_precip['year'].min(), aggregated_precip['year'].max() + 1)})
aggregated_precip_full = pd.merge(all_years, aggregated_precip, on='year', how='left')

X_precip_agg_full = aggregated_precip_full[['year']].values
y_precip_agg_full = aggregated_precip_full['PPT_Annual'].values
model_precip_agg_full = LinearRegression().fit(X_precip_agg_full[~np.isnan(y_precip_agg_full)], 
                                               y_precip_agg_full[~np.isnan(y_precip_agg_full)])
trend_precip_agg_full = model_precip_agg_full.predict(X_precip_agg_full)

# Create the figure for precipitation trend with line plot
fig_precip = go.Figure(data=[
    go.Scatter(
        x=aggregated_precip_full['year'], 
        y=aggregated_precip_full['PPT_Annual'],
        mode='markers+lines',
        name='Observed',
        line=dict(color='skyblue'),
        hovertemplate='Year: %{x}<br>Total Precip: %{y:.2f} inches'
    ),
    go.Scatter(
        x=aggregated_precip_full['year'], 
        y=trend_precip_agg_full,
        mode='lines',
        name='Trend',
        line=dict(color='red'),
        hovertemplate='Year: %{x}<br>Trend: %{y:.2f} inches'
    )
])

# Update layout for precipitation trend
fig_precip.update_layout(
    title='Trend Analysis: Total Annual Precipitation in Utah (1980-2024)',
    xaxis_title='Year',
    yaxis_title='Total Precipitation (inches)',
    legend_title='',
    template='plotly_white'
)