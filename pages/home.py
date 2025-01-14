from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from . import layout

def card_generico(titulo, texto, especifico):
    card = dbc.Card([
        dbc.CardHeader(titulo),
        dbc.CardBody([
            html.P(texto),
            especifico
        ])
    ])

    return card


layout_home = html.Div([
    html.H3('Precipitação'),
    dbc.Row([
       dbc.Col(card_generico("Gráfico 1",'esse é o primeiro texto',''),width=7),
       dbc.Col(card_generico("Gráfico 2",'',''),width=5),
   ], className='mb-4'),
    dbc.Row([
       dbc.Col(card_generico("Gráfico 3",'',''),width=6),
       dbc.Col(card_generico("Registro de medidas",'',''),width=6),
   ]),
])


layout = layout.main_layout(layout_home)

@callback(
    Output('page-1-display-value', 'children'),
    Input('page-1-dropdown', 'value'))
def display_value(value):
    return f'You have selected {value}'