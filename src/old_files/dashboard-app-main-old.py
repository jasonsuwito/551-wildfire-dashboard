import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
fire_df = pd.read_csv("fire.csv", low_memory=False)
wildfires = pd.read_csv("final.csv")  # For map

# Ensure latitude longitude are numeric
wildfires['LATITUDE'] = pd.to_numeric(wildfires['LATITUDE'], errors='coerce')
wildfires['LONGITUDE'] = pd.to_numeric(wildfires['LONGITUDE'], errors='coerce')
wildfires['SIZE_HA'] = pd.to_numeric(wildfires['SIZE_HA'], errors='coerce')

# Remove NaN values
wildfires = wildfires.dropna(subset=["LATITUDE", "LONGITUDE"])

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Define color scheme
BACKGROUND_COLOR = "#292929"
CARD_COLOR = "#333333"
TEXT_COLOR = "#FBB03B"
GRAPH_BG_COLOR = CARD_COLOR

# BC Pie Chart (Fire Causes)
bc_fire = fire_df[fire_df['SRC_AGENCY'] == 'BC']
df_cause_count = bc_fire['CAUSE'].value_counts().reset_index()
df_cause_count.columns = ['CAUSE', 'COUNT']
bc_fire_2013_2023 = bc_fire[(fire_df['YEAR'] >= 2013) & (bc_fire['YEAR'] <= 2023)]

complementary_colours = ['#FF8C00', '#D84B16', '#E0E0E0']
bc_pie_plot = go.Figure(go.Pie(
    labels=df_cause_count['CAUSE'],
    values=df_cause_count['COUNT'],
    hoverinfo='label+value',
    textinfo='label+percent',
    marker=dict(colors=complementary_colours),
    hole=0.5
))

bc_pie_plot.update_layout(
    paper_bgcolor=GRAPH_BG_COLOR,
    font=dict(color=TEXT_COLOR),
    title="Fire Cause Distribution",
    margin=dict(t=60, b=35, l=35, r=35),
)

# Provincial Fire Count Bar Chart
df_filtered = fire_df[(fire_df['YEAR'] >= 2013) & (fire_df['YEAR'] <= 2023)]
fire_count_by_province = df_filtered.groupby(['YEAR', 'SRC_AGENCY']).size().reset_index(name='count')

highlight_prov = 'BC'

prov_fire_plot = go.Figure()
for year in range(2013, 2024):  
    df_year = fire_count_by_province[fire_count_by_province['YEAR'] == year]
    prov_fire_plot.add_trace(go.Bar(
        x=df_year['SRC_AGENCY'],
        y=df_year['count'],
        name=str(year),
        marker_color=df_year['SRC_AGENCY'].apply(lambda prov: '#FF8C00' if prov == highlight_prov else '#E14D2A'),
        hoverinfo='x+y+text',
        text=df_year['count']
    ))
    
prov_fire_plot.update_layout(
    plot_bgcolor=GRAPH_BG_COLOR,
    paper_bgcolor=GRAPH_BG_COLOR,
    font=dict(color=TEXT_COLOR),
    title="Fire Count by Province",
    xaxis=dict(title=None, tickangle=0, showgrid=False, tickfont=dict(size=8, color=TEXT_COLOR)),
    yaxis=dict(title="Count", tickfont=dict(size=8, color=TEXT_COLOR), showgrid=False),
    margin=dict(t=60, b=35, l=35, r=35)
)

# Provincial Fire Size Line Chart
df_grouped = df_filtered.groupby(['YEAR', 'SRC_AGENCY'])['SIZE_HA'].mean().reset_index()

prov_line = go.Figure()
for prov in sorted(df_grouped['SRC_AGENCY'].unique()):
    prov_df = df_grouped[df_grouped['SRC_AGENCY'] == prov]
    prov_line.add_trace(go.Scatter(x=prov_df['YEAR'],
                                   y=prov_df['SIZE_HA'],
                                   mode='lines',
                                   name=prov,
                                   line=dict(color='#FF8C00')))

prov_line.update_layout(
    plot_bgcolor=GRAPH_BG_COLOR,
    paper_bgcolor=GRAPH_BG_COLOR,
    font=dict(color=TEXT_COLOR),
    title="Average Fire Size by Province",
    xaxis=dict(title=None, tickangle=0, showgrid=False, tickfont=dict(size=8, color=TEXT_COLOR)),
    yaxis=dict(title="Average Fire Size", showgrid=False, tickfont=dict(size=8, color=TEXT_COLOR)),
    margin=dict(t=60, b=35, l=35, r=35)
)

# Dashboard Layout
app.layout = dbc.Container(
    [
        # Header
        dbc.Row([
            dbc.Col(html.H3("British Columbia Wildfire Dashboard",
                    style={"color": "#333333", "textAlign": "left", "padding": "15px", "fontWeight": "bold"}),
                    width=12,
                    className="mx-auto",
                    style={"background": "linear-gradient(to right, #ffde59, #ff914d)", "padding": "10px", "margin": "10px"})
        ]),

        # Main Content Row
        dbc.Row([
            # Left Column (Statistics Cards)
            dbc.Col([
                dbc.Card([
                    html.Div([
                        html.H4("Total Fires in BC", className="card-title", style={"color": TEXT_COLOR, "marginBottom": "5px"}),
                        html.H2(f"{bc_fire.shape[0]}", className="card-text", style={"color": TEXT_COLOR})],
                    style={"display": "flex", "flexDirection": "column", "justifyContent": "center", "alignItems": "center", "height": "100%"})
                ], body=True, style={"backgroundColor": CARD_COLOR, "height": "160px", "margin": "10px", "borderRadius": "0px", "display": "flex", "alignItems": "center", "justifyContent": "center"}),

                dbc.Card([
                    html.Div([
                        html.H4("Total Area Burned (HA) in BC", className="card-title", style={"color": TEXT_COLOR}),
                        html.H2(f"{int(bc_fire['SIZE_HA'].sum()):,}", className="card-text", style={"color": TEXT_COLOR})],
                    style={"display": "flex", "flexDirection": "column", "justifyContent": "center", "alignItems": "center", "height": "100%"})
                ], body=True, style={"backgroundColor": CARD_COLOR, "height": "160px", "margin": "10px", "borderRadius": "0px", "display": "flex", "alignItems": "center", "justifyContent": "center"}),
                
                dbc.Card([
                    html.Div([
                        html.H4("Most Common Cause in BC", className="card-title", style={"color": TEXT_COLOR}),
                        html.H2(f"{df_cause_count.iloc[0, 0]}", className="card-text", style={"color": TEXT_COLOR})],
                    style={"display": "flex", "flexDirection": "column", "justifyContent": "center", "alignItems": "center", "height": "100%"})
                ], body=True, style={"backgroundColor": CARD_COLOR, "height": "160px", "margin": "10px", "borderRadius": "0px", "display": "flex", "alignItems": "center", "justifyContent": "center"}),
                
                dbc.Card([
                    html.Div([
                       html.H4("Year with Most Fires in BC", className="card-title", style={"color": TEXT_COLOR}),
                    html.H2(f"{bc_fire_2013_2023['YEAR'].value_counts().idxmax()}", className="card-text", style={"color": TEXT_COLOR})],
                    style={"display": "flex", "flexDirection": "column", "justifyContent": "center", "alignItems": "center", "height": "100%"})
                ], body=True, style={"backgroundColor": CARD_COLOR, "height": "160px", "margin": "10px", "borderRadius": "0px", "display": "flex", "alignItems": "center", "justifyContent": "center"})

            ], width=3, className="px-0"),

            # Right Column (Filter Bar, Graphs and Map)
            dbc.Col([
                
                #Filter bar
                dbc.Row([
                    dbc.Col(
                        dbc.Card([
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
                                style={
                                    "backgroundColor": TEXT_COLOR,
                                    "color": BACKGROUND_COLOR,
                                    "width": "100%",
                                    "height": "40px"
                                }
                            )
                        ], style={"backgroundColor": TEXT_COLOR, "borderRadius": "0px", "marginTop": "10px", "marginRight": "10px"}),
                        width=3
                    ), 
                    dbc.Col(
                        dbc.Card([
                            html.Div("Other Filters Coming Soon", style={
                                "color": TEXT_COLOR,
                                "fontSize": "18px",
                                "fontWeight": "bold",
                                "height": "40px",
                                "padding": "5px"
                            })
                        ], style={"backgroundColor": CARD_COLOR, "borderRadius": "0px", "marginTop": "10px"}),
                        width=9
                    )
                ], className="g-0 px-0", style={"marginBottom": "10px"}),
                
                # Map & Pie Chart
                dbc.Row([
                    dbc.Col(dcc.Graph(id="bc-map", style={"height": "300px", "marginLeft": "10px", "marginBottom": "10px"}), width=8, className="g-0 px-0"),
                    dbc.Col(dcc.Graph(figure=bc_pie_plot, style={"height": "300px", "marginLeft": "10px", "marginBottom": "10px", "marginRight": "10px"}), width=4, className="px-0")
                ]),

                # Bar Chart & Line Chart
                dbc.Row([
                    dbc.Col(dcc.Graph(figure=prov_fire_plot, style={"height": "300px", "marginLeft": "10px", "marginBottom": "10px"}), width=6, className="g-0 px-0"),
                    dbc.Col(dcc.Graph(figure=prov_line, style={"height": "300px", "marginLeft": "10px", "marginBottom": "10px", "marginRight": "10px"}), width=6, className="px-0")
                ]),
            ], width=9, className="g-0 px-0"),
        ], className="gx-0"),
    ], fluid=True, style={"padding": "0px", "backgroundColor": BACKGROUND_COLOR}  # No extra padding
)


@app.callback(
    Output("bc-map", "figure"),
    Input("feature-dropdown", "value")
)
def update_map(selected_feature):
    """Generate and update a wildfire map based on the selected feature with dark theme."""
    fig = px.scatter_mapbox(
        wildfires, 
        lat="LATITUDE", 
        lon="LONGITUDE", 
        color=selected_feature, 
        zoom=4, 
        mapbox_style="carto-darkmatter",
    )
    
    fig.update_layout(
        paper_bgcolor=GRAPH_BG_COLOR,
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(
            font=dict(color=TEXT_COLOR),
            x=1
        ),
        coloraxis_colorbar=dict(
            title_font=dict(color=TEXT_COLOR),
            tickfont=dict(color=TEXT_COLOR),
            x=1
        )
    )
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)