from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from pages import home, sobre

app = Dash(__name__, suppress_callback_exceptions=True,external_stylesheets=[dbc.themes.SANDSTONE] )

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@callback(Output('page-content', 'children'),
          Input('url', 'pathname'))
def display_page(pathname):
    print(pathname)

    if pathname == '/home':
        #return html.Div('este é um teste')
        return home.layout
    elif pathname == '/sobre':
        return sobre.layout
    else:
        return home.layout


if __name__ == '__main__':
    app.run(debug=True)