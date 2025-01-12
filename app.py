from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from pages import home, sobre

app = Dash(__name__, suppress_callback_exceptions=True)


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/home", active="exact"),
                dbc.NavLink("Sobre", href="/sobre", active="exact"),
           ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

layout = html.Div(id="page-content", style=CONTENT_STYLE)


app.layout = html.Div([
     dcc.Location(id='url', refresh=False),
   layout])


@callback(Output('page-content', 'children'),
          Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/home':
        return home.layout
    elif pathname == '/sobre':
        return sobre.layout
    else:
        return '404'


if __name__ == '__main__':
    app.run(debug=True)