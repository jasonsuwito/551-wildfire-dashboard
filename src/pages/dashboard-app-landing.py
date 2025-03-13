import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/")  # Register as the home page

# Load data
fires = pd.read_csv("../data/NFDB_point_20240613.txt")

# Process data
fire_map_data = fires[['FIRE_ID', 'SRC_AGENCY', 'LATITUDE', 'LONGITUDE', 'YEAR', 'SIZE_HA']]
fire_map_data = fire_map_data[(fire_map_data['YEAR'] >= 2013) & (fire_map_data['YEAR'] <= 2023)].sort_values(by='YEAR', ascending=True)
fire_map_data['SIZE_HA'] = fire_map_data['SIZE_HA']
fire_map_data['color'] = "black"

# Province abbreviation mapping
province_dict = {
    'AB': 'Alberta', 'BC': 'British Columbia', 'MB': 'Manitoba', 'NB': 'New Brunswick',
    'NL': 'Newfoundland and Labrador', 'NS': 'Nova Scotia', 'ON': 'Ontario',
    'PE': 'Prince Edward Island', 'QC': 'Quebec', 'SK': 'Saskatchewan',
    'YT': 'Yukon', 'NT': 'Northwest Territories'
}

fire_map_data['SRC_AGENCY'] = fire_map_data['SRC_AGENCY'].replace(province_dict)

# Add Nunavut to appear on the map
new_row = {
    'FIRE_ID': 'RANDFIRE1', 'SRC_AGENCY': 'Nunavut', 'LATITUDE': 50.990700, 
    'LONGITUDE': -85.060300, 'YEAR': 2023, 'SIZE_HA': 1, 'color': "black"
}
fire_map_data = pd.concat([fire_map_data, pd.DataFrame([new_row])], ignore_index=True)

# Load GeoJSON for provinces
with open("../data/canada_provinces.geojson", "r") as geo:
    geojson_data = json.load(geo)

# Filter data to remove outliers
fire_map_data_filtered = fire_map_data[
    (fire_map_data['LATITUDE'] >= 41) & (fire_map_data['LATITUDE'] <= 83) & 
    (fire_map_data['LONGITUDE'] >= -141) & (fire_map_data['LONGITUDE'] <= -52)
]

# Calculate total hectares burned
total_burned_mil = sum(fire_map_data['SIZE_HA'])/1000000

# Create base choropleth figure
fig = px.choropleth(
    fire_map_data_filtered,
    geojson=geojson_data,
    locations='SRC_AGENCY',
    featureidkey="properties.name",
    scope='north america',
    color='color',
    color_discrete_map={"black": "#101010"},
    hover_data={'color': False, 'SRC_AGENCY': False}
)

# Layout adjustments
fig.update_layout(
    margin={"r":0, "t":0, "l":0, "b":0},
    geo=dict(bgcolor='#181818'),
    plot_bgcolor='#181818',
    paper_bgcolor='#181818',
    showlegend=False,
    dragmode=False,
    autosize=True
)

# Map display settings
fig.update_geos(
    showcountries=False, 
    showcoastlines=False, 
    showland=False, 
    showlakes=False, 
    subunitcolor='white',
    center={"lat": 61, "lon": -91},
    projection_scale=2.7
)

# Province border styling
fig.update_traces(marker=dict(line=dict(color='white', width=0.2)))

# Add fire location points
fig.add_trace(
    go.Scattergeo(
        lat=fire_map_data_filtered['LATITUDE'],
        lon=fire_map_data_filtered['LONGITUDE'],
        mode='markers',
        hoverinfo='skip',
        marker=dict(
            size=1.5, color='#f77b07', symbol='circle', opacity=0.2
        )
    )
)

# Add text into map
fig.add_annotation(
    text=f"<span style='color: #f77b07; font-size: 108px; font-family: Arial Black, Gadget, sans-serif; letter-spacing: -5.5px'>{total_burned_mil:.0f} million</span><br>",
    x=0.9, y=0.75,  
    xref="paper", yref="paper",
    showarrow=False,
    bgcolor="rgba(0, 0, 0, 0)"
)

fig.add_annotation(
    text=f"<span style='color: rgba(255, 255, 255, .6); font-size: 20px; font-family: Arial Narrow, sans-serif;'>Hectares of Land Have Been Burned Over the Last 10 Years</span>",
    x=0.9, y=0.59,  
    xref="paper", yref="paper",
    showarrow=False,
    bgcolor="rgba(0, 0, 0, 0)"
)

# Define home layout
layout = dbc.Container(
    fluid=True,
    style={"backgroundColor": "#181818", "padding": "0px", "margin": "0px", "width": "97vw", "height": "90vh"},
    children=[
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    figure=fig,
                    config={"staticPlot": True},
                    style={"height": "calc(100vh - 70px)", "width": "100vw"},
                ),
                width=12,
                style={"padding": "0px", "margin": "0px"},
            )
        ),
    ],
)
