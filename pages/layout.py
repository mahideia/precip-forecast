from dash.dependencies import Input, Output
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import sqlite3

def seleciona_cidade():
    lt_conn = sqlite3.connect('precip.db')
    db_query = pd.read_sql_query('''select DISTINCT cidade from previsoes ''', lt_conn)
    df = pd.DataFrame(db_query)
    lt_conn.close()
    return df['cidade'].to_list()

# the style arguments for the sidebar. We use position:fixed and a fixed width
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
        html.H2("Precipitação", className="display-6"),
        html.Hr(),
        html.P(
            "Previsões e medidas reais", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/home", active="exact"),
                dbc.NavLink("Mais", href="/mais", active="exact"),
                dbc.NavLink("Sobre", href="/sobre", active="exact"),
           ],
            vertical=True,
            pills=True,
        ),
        html.Hr(), html.P("Selecionar cidade:"),
        dcc.Dropdown(seleciona_cidade(),'Katueté',id='dropdown-cidade')
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="pg-content", style=CONTENT_STYLE)


def main_layout(especifico):
    pag = html.Div([sidebar, html.Div(especifico, id="pg-content", style=CONTENT_STYLE)])
    return pag


