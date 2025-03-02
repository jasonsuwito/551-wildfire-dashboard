import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load data
data_bc = pd.read_csv("final.csv")

# Ensure lat/lon are numeric
data_bc["LATITUDE"] = pd.to_numeric(data_bc["LATITUDE"], errors="coerce")
data_bc["LONGITUDE"] = pd.to_numeric(data_bc["LONGITUDE"], errors="coerce")
data_bc["SIZE_HA"] = pd.to_numeric(data_bc["SIZE_HA"], errors="coerce")

# Remove NaN values
data_bc = data_bc.dropna(subset=["LATITUDE", "LONGITUDE"])

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("BC Wildfire Map - Select Feature", style={'textAlign': 'center'}),

    dcc.Dropdown(
        id="feature-dropdown",
        options=[
            {"label": "Fire Size (SIZE_HA)", "value": "SIZE_HA"},
            {"label": "Cause of Fire (CAUSE)", "value": "CAUSE"},
            {"label": "Response Type (RESPONSE)", "value": "RESPONSE"},
            {"label": "Fire Count (count(FID))", "value": "FID"},
            {"label": "Month (MONTH)", "value": "MONTH"},
        ],
        placeholder="Select a feature...",
        value="SIZE_HA",
        clearable=False,
    ),

    dcc.Graph(id="bc-map")
])

@app.callback(
    Output("bc-map", "figure"),
    Input("feature-dropdown", "value")
)
def update_map(selected_feature):
    """Generate and update a wildfire map based on the selected feature."""
    
    if selected_feature == "SIZE_HA":
        # Aggregate mean SIZE_HA per location
        data_agg = data_bc.groupby(["LATITUDE", "LONGITUDE"], as_index=False).agg({"SIZE_HA": "mean"})
        
        fig = px.scatter_mapbox(
            data_agg,
            lat="LATITUDE",
            lon="LONGITUDE",
            size="SIZE_HA",  # Circle size based on mean fire size
            color="SIZE_HA",  # Use color for continuous scale
            hover_data=["SIZE_HA"],
            zoom=3,
            title="BC Wildfires - Mean Fire Size",
            color_continuous_scale="Reds",  # This now works correctly
            mapbox_style="open-street-map"
        )

    elif selected_feature in ["CAUSE", "RESPONSE", "MONTH"]:
        fig = px.scatter_mapbox(
            data_bc,
            lat="LATITUDE",
            lon="LONGITUDE",
            color=selected_feature,  # Color by categorical feature
            hover_data=["SIZE_HA", "CAUSE", "RESPONSE", "MONTH"],
            zoom=3,
            title=f"BC Wildfires - {selected_feature}",
            mapbox_style="open-street-map"
        )

    elif selected_feature == "FID":
        # Count occurrences per location
        data_agg = data_bc.groupby(["LATITUDE", "LONGITUDE"], as_index=False).agg({"FID": "count"})
        fig = px.scatter_mapbox(
            data_agg,
            lat="LATITUDE",
            lon="LONGITUDE",
            #size="FID",
            color="FID",  # Apply color mapping for fire count
            hover_data=["FID"],
            zoom=3,
            title="BC Wildfires - Fire Count",
            #color_continuous_scale="Blues",
            mapbox_style="open-street-map"
        )

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
