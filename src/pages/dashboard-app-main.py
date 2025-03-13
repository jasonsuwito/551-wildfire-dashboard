import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

dash.register_page(__name__, path="/detailed")  # Register as the detailed view page

# Load and Process data
raw_df = pd.read_csv("../data/NFDB_point_20240613.txt", low_memory=False)
cleaned_df = raw_df[(raw_df['YEAR'] >= 2013) & (raw_df['YEAR'] <= 2023)]
cause_mapping = {
    'H': 'Human',
    'U': 'Unknown',
    'N': 'Natural',
    'H-PB': 'Human'
}
cleaned_df['CAUSE'] = cleaned_df['CAUSE'].replace(cause_mapping)
master_fire_df = cleaned_df

#fire_df = pd.read_csv("fire.csv", low_memory=False)
#wildfires = pd.read_csv("final.csv")  # For map
#wildfires = pd.read_csv("final_ca.csv")  # For map

# Ensure latitude longitude are numeric
master_fire_df['LATITUDE'] = pd.to_numeric(master_fire_df['LATITUDE'], errors='coerce')
master_fire_df['LONGITUDE'] = pd.to_numeric(master_fire_df['LONGITUDE'], errors='coerce')
master_fire_df['SIZE_HA'] = pd.to_numeric(master_fire_df['SIZE_HA'], errors='coerce')

# Remove NaN values
master_fire_df = master_fire_df.dropna(subset=["LATITUDE", "LONGITUDE"])

# Define color scheme
BACKGROUND_COLOR = "#181818"
CARD_COLOR = "#242424"
TEXT_COLOR = "#FBB03B"
GRAPH_BG_COLOR = CARD_COLOR

# Cause Count
df_cause_count = master_fire_df['CAUSE'].value_counts().reset_index()
df_cause_count.columns = ['CAUSE', 'COUNT']

# Define all provinces and territories in Canada for Province Filter
province_options = [
    {'label': 'ALL', 'value': 'ALL'},  # "ALL" option for all provinces
    {'label': 'AB', 'value': 'AB'},
    {'label': 'BC', 'value': 'BC'},
    {'label': 'MB', 'value': 'MB'},
    {'label': 'NB', 'value': 'NB'},
    {'label': 'NL', 'value': 'NL'},
    {'label': 'NT', 'value': 'NT'},
    {'label': 'NS', 'value': 'NS'},
    {'label': 'NU', 'value': 'NU'},
    {'label': 'ON', 'value': 'ON'},
    {'label': 'PE', 'value': 'PE'},
    {'label': 'QC', 'value': 'QC'},
    {'label': 'SK', 'value': 'SK'},
    {'label': 'YT', 'value': 'YT'}
]

# Dashboard Layout
layout = dbc.Container(
    [
        # Main Content Row
        dbc.Row([
            # Left Column (Statistics Cards)
            dbc.Col([
                dbc.Card([
                    html.Div([
                        html.H6("Total Fires", className="card-title", style={"color": TEXT_COLOR, "marginBottom": "5px"}),
                        html.H2(id="total-fires-card", className="card-text", style={"color": TEXT_COLOR})],
                    style={"display": "flex", "flexDirection": "column", "justifyContent": "center", "alignItems": "center", "height": "100%"})
                ], body=True, style={"backgroundColor": CARD_COLOR, "height": "160px", "margin": "10px", "borderRadius": "0px", "display": "flex", "alignItems": "center", "justifyContent": "center"}),

                dbc.Card([
                    html.Div([
                        html.H6("Total Area Burned (HA)", className="card-title", style={"color": TEXT_COLOR}),
                        html.H2(id="total-area-burned-card", className="card-text", style={"color": TEXT_COLOR})],
                    style={"display": "flex", "flexDirection": "column", "justifyContent": "center", "alignItems": "center", "height": "100%"})
                ], body=True, style={"backgroundColor": CARD_COLOR, "height": "160px", "margin": "10px", "borderRadius": "0px", "display": "flex", "alignItems": "center", "justifyContent": "center"}),
                
                dbc.Card([
                    html.Div([
                        html.H6("Most Common Cause", className="card-title", style={"color": TEXT_COLOR}),
                        html.H2(id="most-common-cause-card", className="card-text", style={"color": TEXT_COLOR})],
                    style={"display": "flex", "flexDirection": "column", "justifyContent": "center", "alignItems": "center", "height": "100%"})
                ], body=True, style={"backgroundColor": CARD_COLOR, "height": "160px", "margin": "10px", "borderRadius": "0px", "display": "flex", "alignItems": "center", "justifyContent": "center"}),
                
                dbc.Card([
                    html.Div([
                        html.H6("Year with Most Fires", className="card-title", style={"color": TEXT_COLOR}),
                        html.H2(id="most-fires-year-card", className="card-text", style={"color": TEXT_COLOR})],
                    style={"display": "flex", "flexDirection": "column", "justifyContent": "center", "alignItems": "center", "height": "100%"})
                ], body=True, style={"backgroundColor": CARD_COLOR, "height": "160px", "margin": "10px", "borderRadius": "0px", "display": "flex", "alignItems": "center", "justifyContent": "center"})

            ], width=2, className="px-0"),

            # Right Column (Filter Bar, Graphs and Map)
            dbc.Col([
                #Filter bar
                dbc.Row([
                    dbc.Col(
                        dbc.Card([
                            html.Div([
                                html.Div("Province:", 
                                    style={
                                        "color": TEXT_COLOR,
                                        "fontSize": "18px",
                                        "fontWeight": "bold",
                                        "paddingRight": "10px",
                                        "whiteSpace": "nowrap"
                                    }
                                ),
                                html.Div(
                                    dcc.Dropdown(
                                        id="province-dropdown",
                                        options=province_options,  # Predefined province list
                                        placeholder="ALL",
                                        value="ALL",  # Default to "ALL"
                                        clearable=False,
                                        style={
                                            "width": "100%",
                                            "height": "40px",
                                            "backgroundColor": CARD_COLOR,
                                            "color": TEXT_COLOR,
                                        },
                                        className="custom-dropdown"
                                    ), 
                                    style={"flex": "1"}
                                )
                            ], style={"display": "flex", "alignItems": "center", "width": "100%"})  # Flexbox for horizontal alignment
                        ], style={"backgroundColor": CARD_COLOR, "borderRadius": "0px", "marginTop": "10px", "marginRight": "10px", "padding": "5px"}), 
                        width=2
                    ),

                    #=== SELECT VIEW FILTER ===
                    dbc.Col(
                        dbc.Card([
                            html.Div([
                                # Label for the dropdown
                                html.Div("Map View:", 
                                    style={
                                        "color": TEXT_COLOR,
                                        "fontSize": "18px",
                                        "fontWeight": "bold",
                                        "paddingRight": "10px",
                                        "whiteSpace": "nowrap"
                                    }
                                ),
                                # Dropdown component
                                html.Div(
                                    dcc.Dropdown(
                                        id="feature-dropdown",
                                        options=[
                                            {"label": "Fire Size", "value": "SIZE_HA"},
                                            {"label": "Cause of Fire", "value": "CAUSE"},
                                            {"label": "Response Type", "value": "RESPONSE"},
                                            {"label": "Month", "value": "MONTH"},
                                        ],
                                        placeholder="SIZE_HA",
                                        value="SIZE_HA",
                                        clearable=False,
                                        style={
                                            "width": "100%",
                                            "height": "40px",
                                            "backgroundColor": CARD_COLOR,
                                            "color": TEXT_COLOR,
                                        },
                                        className="custom-dropdown"  # Apply external CSS for full control
                                    ), 
                                    style={"flex": "1"}
                                )
                            ], style={"display": "flex", "alignItems": "center", "width": "100%"})  # Flexbox for horizontal alignment
                        ], style={"backgroundColor": CARD_COLOR, "borderRadius": "0px", "marginTop": "10px", "marginRight": "10px", "padding": "5px"}), 
                        width=3
                    ),
                    
                     #=== SELECT YEAR RANGE FILTER ===
                    dbc.Col(
                        dbc.Card([
                            html.Div([
                                html.Div("Year Range:", 
                                    style={
                                        "color": TEXT_COLOR, 
                                        "fontSize": "18px", 
                                        "fontWeight": "bold", 
                                        "paddingRight": "10px",
                                        "whiteSpace": "nowrap"
                                    }
                                ),
                                html.Div(
                                    dcc.RangeSlider(
                                        id="year-slider",
                                        min=master_fire_df['YEAR'].min(),
                                        max=master_fire_df['YEAR'].max(),
                                        step=1,
                                        marks={year: str(year) for year in range(master_fire_df['YEAR'].min(), master_fire_df['YEAR'].max() + 1)},
                                        value=[master_fire_df['YEAR'].min(), master_fire_df['YEAR'].max()],
                                        tooltip={"placement": "bottom", "always_visible": True},
                                    ), 
                                    style={"flex": "1"}  # Make the slider take up remaining space
                                )
                            ], style={"display": "flex", "alignItems": "center", "width": "100%"})  # Flexbox for horizontal alignment
                        ], style={"backgroundColor": CARD_COLOR, "borderRadius": "0px", "marginTop": "10px", "padding": "5px"}), 
                        width=7
                    )
                ], className="g-0 px-0", style={"marginBottom": "10px"}),
                
                # Map & Pie Chart
                dbc.Row([
                    dbc.Col(dcc.Graph(id="fire-map", style={"height": "300px", "marginLeft": "10px", "marginBottom": "10px"}), width=8, className="g-0 px-0"),
                    dbc.Col(dcc.Graph(id="pie-chart", style={"height": "300px", "marginLeft": "10px", "marginBottom": "10px", "marginRight": "10px"}), width=4, className="px-0")
                ]),

                # Bar Chart & Line Chart
                dbc.Row([
                    dbc.Col(dcc.Graph(id="fire-count-bar", style={"height": "300px", "marginLeft": "10px", "marginBottom": "10px"}), width=6, className="g-0 px-0"),
                    dbc.Col(dcc.Graph(id="fire-size-line", style={"height": "300px", "marginLeft": "10px", "marginBottom": "10px", "marginRight": "10px"}), width=6, className="px-0")
                ]),
            ], width=10, className="g-0 px-0"),
        ], className="gx-0"),
    ], fluid=True, style={"padding": "0px", "backgroundColor": BACKGROUND_COLOR}  # No extra padding
)

# Data Filtering Function
def filter_master_fire_df(year_range, province):
    """Filter master_fire_df based on year range and province selection."""
    start_year, end_year = year_range
    filtered_df = master_fire_df[(master_fire_df['YEAR'] >= start_year) & (master_fire_df['YEAR'] <= end_year)]
    
    if province != "ALL":
        filtered_df = filtered_df[filtered_df['SRC_AGENCY'] == province]

    return filtered_df


# === MAP CALLBACK ===
@dash.callback(
    Output("fire-map", "figure"),
    [Input("feature-dropdown", "value"),
     Input("year-slider", "value"),
     Input("province-dropdown", "value")]
)
def update_map(selected_feature, selected_year_range, selected_province):
    """Generate and update a wildfire map based on the selected feature and year range."""
        
    # Filter data based on selected year range
    filtered_df = filter_master_fire_df(selected_year_range, selected_province)

    category_orders = {
        'MONTH': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
        'CAUSE': ["Human", "Natural", "Unknown"]
    }
    
    if selected_feature == "SIZE_HA":
        # Aggregate mean SIZE_HA per location
        data_agg = filtered_df.groupby(["LATITUDE", "LONGITUDE"], as_index=False).agg({"SIZE_HA": "mean"})
        
        fig = px.scatter_mapbox(
            data_agg,
            lat="LATITUDE",
            lon="LONGITUDE",
            size="SIZE_HA",  # Circle size based on mean fire size
            color="SIZE_HA",  # Use color for continuous scale
            hover_data=["SIZE_HA"],
            zoom=2.5,
            color_continuous_scale="Reds",  
            mapbox_style="carto-darkmatter"        
        )

    elif selected_feature in ["CAUSE", "RESPONSE", "MONTH"]:
        # Drop rows where MONTH == 0
        filtered_df = filtered_df[filtered_df["MONTH"] != 0]
        if selected_feature == "MONTH":
            filtered_df['MONTH'] = filtered_df['MONTH'].astype(str)  # Convert to string for categorical

        # Define color mappings
        color_scheme = {
            "MONTH": [
                "#1F78B4", "#6AAED6", "#A6CEE3", "#FEE08B", "#FE9929", "#FD8D3C", 
                "#E41A1C", "#FC4E2A", "#FCAE91", "#FFD92F", "#8DA0CB", "#377EB8"
            ],  # 12 colors from blue to red to blue
            "RESPONSE": [
                "#D73027", "#D84B16", "#FF8C00", "#FED976", "#FEC44F", "#FCAE91"
            ]  # 6 distinct colors for RESPONSE
        }

        # Define specific mapping for CAUSE
        cause_color_map = {
            "Human": "#FF8C00",    # Orange
            "Natural": "#D84B16",  # Deep Red
            "Unknown": "#E0E0E0"   # Grey
        }
    
        fig = px.scatter_mapbox(
            filtered_df,
            lat="LATITUDE",
            lon="LONGITUDE",
            color=selected_feature,  # Color by categorical feature
            hover_data=["SIZE_HA", "CAUSE", "RESPONSE", "MONTH"],
            zoom=2.5,
            size_max=0.5,
            color_discrete_map=cause_color_map if selected_feature == "CAUSE" else None,  # Apply mapping only for CAUSE
            color_discrete_sequence=color_scheme.get(selected_feature) if selected_feature in ["MONTH", "RESPONSE"] else None,  # Assign colors for MONTH and RESPONSE
            mapbox_style="carto-darkmatter",
            category_orders=category_orders  # Ensure correct category order
        )

        fig.update_traces(marker=dict(size=3))

    fig.update_layout(
        paper_bgcolor=GRAPH_BG_COLOR,
        mapbox_center={"lat": 55, "lon": -101},
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(
            font=dict(color=TEXT_COLOR),
            x=1
        ),
        coloraxis_colorbar=dict(
            title_font=dict(color=TEXT_COLOR),
            tickfont=dict(color=TEXT_COLOR),
            x=1
        ),
    )
    
    return fig



# === CAUSE PIE CHART CALLBACK ===
@dash.callback(
    Output("pie-chart", "figure"),
    [Input("year-slider", "value"),
     Input("province-dropdown", "value")]
)
def update_pie_chart(selected_year_range, selected_province):
    """Update the Pie Chart with filtered data."""
    
    filtered_df = filter_master_fire_df(selected_year_range, selected_province)

    cause_counts = filtered_df['CAUSE'].value_counts().reset_index()
    cause_counts.columns = ['CAUSE', 'COUNT']

    fig = px.pie(
        cause_counts,
        names="CAUSE",
        values="COUNT",
        hole=0.5,
        color_discrete_sequence=["#FF8C00", "#D84B16", "#E0E0E0"]
    )

    fig.update_layout(
        paper_bgcolor=GRAPH_BG_COLOR,
        font=dict(color=TEXT_COLOR),
        title=f"Fire Cause Distribution in {selected_province}",
        margin=dict(t=60, b=35, l=35, r=35),
    )

    return fig


# === FIRE COUNT BAR CHART CALLBACK ===
@dash.callback(
    Output("fire-count-bar", "figure"),
    [Input("year-slider", "value"),
     Input("province-dropdown", "value")]
)
def update_fire_count_bar(selected_year_range, selected_province):
    """Update Fire Count Bar Chart based on year range and province selection.
    """

    # If "ALL" is selected, show  fire count by province
    if selected_province == "ALL":
        filtered_df = filter_master_fire_df(selected_year_range, selected_province)

        # Group by Province (Summing Fire Counts)
        fire_count_by_province = filtered_df.groupby(['SRC_AGENCY', 'YEAR']).size().reset_index(name='count')
        fire_count_by_province_aggregated = fire_count_by_province.groupby('SRC_AGENCY')['count'].sum().reset_index()

        highlight_prov = 'BC'  # Highlight BC

        # Create the bar chart for all provinces
        prov_fire_plot = go.Figure()

        prov_fire_plot.add_trace(go.Bar(
            x=fire_count_by_province_aggregated['SRC_AGENCY'],
            y=fire_count_by_province_aggregated['count'],
            marker_color=fire_count_by_province_aggregated['SRC_AGENCY'].apply(lambda prov: '#FF8C00' if prov == highlight_prov else '#E14D2A'),
            hoverinfo='x+y+text',
            text=fire_count_by_province_aggregated.apply(lambda row: f"Prov: {row['SRC_AGENCY']}<br>Count: {row['count']}", axis=1),
            textposition="none"  # Removes text inside bars
        ))

        # Update layout
        prov_fire_plot.update_layout(
            plot_bgcolor=GRAPH_BG_COLOR,
            paper_bgcolor=GRAPH_BG_COLOR,
            font=dict(color=TEXT_COLOR),
            title="Total Fire Count by Province",
            xaxis=dict(
                title=None,
                tickangle=0,
                showgrid=False,
                tickfont=dict(size=8, color=TEXT_COLOR),
                tickcolor=TEXT_COLOR
            ),
            yaxis=dict(
                title="Fire Count",
                title_font=dict(size=9, color=TEXT_COLOR),
                tickfont=dict(size=8, color=TEXT_COLOR),
                tickcolor=TEXT_COLOR,
                showgrid=False,
                showline=True,
                linecolor=TEXT_COLOR,
                linewidth=0.5,
            ),
            margin=dict(t=60, b=35, l=35, r=35),
            showlegend=False  # Removes legend
        )

        return prov_fire_plot

    else:
        # If a specific province is selected, show yearly fire count
        filtered_df = filter_master_fire_df(selected_year_range, selected_province)

        # Group by Year
        fire_count_by_year = filtered_df.groupby(['YEAR']).size().reset_index(name='count')

        # Create the bar chart for a specific province
        prov_fire_plot = go.Figure()

        prov_fire_plot.add_trace(go.Bar(
            x=fire_count_by_year['YEAR'],
            y=fire_count_by_year['count'],
            marker_color=TEXT_COLOR,
            hoverinfo='text',
            text=fire_count_by_year.apply(lambda row: f"Year: {row['YEAR']}<br>Count: {row['count']}", axis=1),
            textposition="none"
        ))

        # Update layout
        prov_fire_plot.update_layout(
            plot_bgcolor=GRAPH_BG_COLOR,
            paper_bgcolor=GRAPH_BG_COLOR,
            font=dict(color=TEXT_COLOR),
            title=f"Fire Count in {selected_province} by Year",
            xaxis=dict(
                title="Year",
                tickangle=0,
                showgrid=False,
                tickfont=dict(size=8, color=TEXT_COLOR)
            ),
            yaxis=dict(
                title="Fire Count",
                tickfont=dict(size=8, color=TEXT_COLOR),
                showgrid=False
            ),
            margin=dict(t=60, b=35, l=35, r=35),
            showlegend=False  # Removes legend
        )

        return prov_fire_plot


# === FIRE SIZE LINE GRAPH CALLBACK ===
@dash.callback(
    Output("fire-size-line", "figure"),
    [Input("year-slider", "value"),
     Input("province-dropdown", "value")]
)
def update_fire_size_line(selected_year_range, selected_province):
    """Update Average Fire Size Line Chart dynamically based on year range and province selection."""

    # Filter data based on selection
    filtered_df = filter_master_fire_df(selected_year_range, selected_province)

    # Group by Year and Province, calculating the mean fire size
    df_grouped = filtered_df.groupby(['YEAR', 'SRC_AGENCY'])['SIZE_HA'].mean().reset_index()

    prov_line = go.Figure()

    # Add a line for each province in the filtered dataset
    for prov in sorted(df_grouped['SRC_AGENCY'].unique()):
        prov_df = df_grouped[df_grouped['SRC_AGENCY'] == prov]
        prov_line.add_trace(go.Scatter(
            x=prov_df['YEAR'],
            y=prov_df['SIZE_HA'],
            mode='lines',
            name=prov,
            line=dict(color='#FF8C00')
        ))

    # Update layout
    prov_line.update_layout(
        plot_bgcolor=GRAPH_BG_COLOR,
        paper_bgcolor=GRAPH_BG_COLOR,
        font=dict(color=TEXT_COLOR),
        title=f"Average Fire Size in {selected_province}",
        xaxis=dict(title=None, tickangle=0, showgrid=False, tickfont=dict(size=8, color=TEXT_COLOR)),
        yaxis=dict(title="Average Fire Size (HA)", showgrid=False, tickfont=dict(size=8, color=TEXT_COLOR)),
        margin=dict(t=60, b=35, l=35, r=35)
    )

    return prov_line


# === STATISTIC CARDS CALLBACK ===
@dash.callback(
    [Output("total-fires-card", "children"),
     Output("total-area-burned-card", "children"),
     Output("most-common-cause-card", "children"),
     Output("most-fires-year-card", "children")],
    [Input("year-slider", "value"),
     Input("province-dropdown", "value")]
)
def update_cards(selected_year_range, selected_province):
    """Update the KPI cards dynamically based on year range and province selection."""

    # Filter the dataset based on the selected criteria
    filtered_df = filter_master_fire_df(selected_year_range, selected_province)

    # Compute the card values
    total_fires = filtered_df.shape[0]  # Total number of fires
    total_area_burned = int(filtered_df['SIZE_HA'].sum())  # Sum of burned area
    most_common_cause = filtered_df['CAUSE'].value_counts().idxmax() if not filtered_df.empty else "N/A"
    most_fires_year = filtered_df['YEAR'].value_counts().idxmax() if not filtered_df.empty else "N/A"
    
    # Format the values for display
    return f"{total_fires:,}", f"{total_area_burned:,}", most_common_cause, most_fires_year