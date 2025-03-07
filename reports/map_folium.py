import dash
from dash import dcc, html, Input, Output
import pandas as pd
import folium
import uuid
import os

# Load data
data_bc = pd.read_csv('final.csv')

# Ensure lat/lon are numeric
data_bc['LATITUDE'] = pd.to_numeric(data_bc['LATITUDE'], errors='coerce')
data_bc['LONGITUDE'] = pd.to_numeric(data_bc['LONGITUDE'], errors='coerce')

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("BC Wildfire Map - Select Feature", style={'textAlign': 'center'}),

    dcc.Dropdown(
        id='feature-dropdown',
        options=[
            {'label': 'Fire Size (SIZE_HA)', 'value': 'SIZE_HA'},
            {'label': 'Cause of Fire (CAUSE)', 'value': 'CAUSE'},
            {'label': 'Response Type (RESPONSE)', 'value': 'RESPONSE'},
            {'label': 'Fire Count (count(FID))', 'value': 'FID'},
            {'label': 'Month (MONTH)', 'value': 'MONTH'}
        ],
        placeholder='Select a feature...',
        value='SIZE_HA',
        clearable=False
    ),

    html.Iframe(
        id='bc-map',
        style={'width': '100%', 'height': '600px', 'border': 'none'}
    )
])

@app.callback(
    Output('bc-map', 'srcDoc'),
    Input('feature-dropdown', 'value')
)
def update_map(selected_feature):
    """Generate and update a wildfire map based on the selected feature."""
    map_center = [data_bc['LATITUDE'].mean(), data_bc['LONGITUDE'].mean()]
    m = folium.Map(location=map_center, zoom_start=6, tiles="OpenStreetMap")

    # Add wildfire markers
    for _, row in data_bc.iterrows():
        if pd.notnull(row['LATITUDE']) and pd.notnull(row['LONGITUDE']):
            fire_size = row.get('SIZE_HA', 1)  # Default if missing
            color = "red"

            # Modify color based on feature
            if selected_feature == "SIZE_HA":
                color = "darkred" if fire_size > 1000 else "lightred"
            elif selected_feature == "CAUSE":
                color = "blue" if row.get("CAUSE") == "Lightning" else "orange"
            elif selected_feature == "RESPONSE":
                color = "green" if row.get("RESPONSE") == "Under Control" else "purple"
            elif selected_feature == "MONTH":
                chart = base_chart.encode(color='MONTH:N')

            folium.CircleMarker(
                location=[row['LATITUDE'], row['LONGITUDE']],
                radius=max(3, min(12, fire_size / 500)),  # Scale size
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.6,
                popup=f"Fire Size: {fire_size} ha\nCause: {row.get('CAUSE', 'Unknown')}\nResponse: {row.get('RESPONSE', 'Unknown')}"
            ).add_to(m)

    # Save map as an HTML file and return its content
    map_html = m._repr_html_()
    return map_html  # Directly return HTML content

if __name__ == '__main__':
    app.run_server(debug=True)
