import dash
import dash_bootstrap_components as dbc
from dash import html, page_container, dcc, Input, Output

# Initialize the Dash app
app = dash.Dash(
    __name__, 
    title='Canadian Wildfire Analysis',
    external_stylesheets=[dbc.themes.DARKLY],
    use_pages=True
)


# Define main app layout
app.layout = dbc.Container(
    fluid=True,
    style={"backgroundColor": "#181818", "width": "100vw", "height": "100vh", "padding": "0"},
    children=[
        # Navigation bar stuff
        dbc.Navbar(
            children=[
                html.H3(
                    "Canadian Wildfire Analysis",
                    style={"color": "#292929", "fontWeight": "bold", "margin-left": "20px"}
                ),
                dcc.Location(id="url", refresh=False), 
                dbc.Nav(
                    [
                        dbc.NavItem(
                            dbc.Button("Home", id="home-btn", color="dark", outline=True, href="/", size="med",
                                       style={"margin-right": "10px"})
                        ),
                        dbc.NavItem(
                            dbc.Button("Detailed View", id="detailed-btn", color="dark", outline=True, href="/detailed", size="med")
                        ),
                    ],
                    className="ms-auto"
                ),
            ],
            color="warning",
            dark=False,
            style={"background": "linear-gradient(to right, #ffde59, #ff914d)", "padding": "10px", "width": "100vw", "margin": "0"}
        ),

        # Page containers for loading
        page_container  
    ],
)

# Callback to change button highlighting
@app.callback(
    Output("home-btn", "color"),
    Output("home-btn", "outline"),
    Output("detailed-btn", "color"),
    Output("detailed-btn", "outline"),
    Input("url", "pathname")
)

# Function for updating the active button
def update_active_button(pathname):
    if pathname == "/detailed":
        return "secondary", True, "dark", False  # Highlight "Detailed View"
    else:
        return "dark", False, "secondary", True  # Highlight "Home" (default)

# Run app
if __name__ == "__main__":
    app.run_server(debug=True)
