from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from . import layout
import plotly.graph_objs as go
import pandas as pd
import sqlite3
from datetime import datetime


def plot_grafico_previsao(data):
    print(pd.to_datetime(data).strftime("%Y%m%d"))
    lt_conn = sqlite3.connect('precip.db')
    db_query = pd.read_sql_query('''select * from previsoes limit 5;''', lt_conn)
    df = pd.DataFrame(db_query)
    lt_conn.close()
    print(df)  

    fig = go.Figure()
    return fig

def card_generico(titulo, texto, especifico):
    card = dbc.Card([
        dbc.CardHeader(titulo),
        dbc.CardBody([
            html.P(texto),
            especifico
        ])
    ])

    return card

forecast_plot = html.Div([
    dbc.Row(dcc.DatePickerSingle(id='data-inicio-previsao',max_date_allowed=datetime.today().strftime('%Y-%m-%d'), date=datetime.today().strftime('%Y-%m-%d')),),
    dbc.Row(dcc.Graph(id='previsao-10dias',figure=plot_grafico_previsao('19910212'), style={'padding':'10px'}))
])

card_registro_medidas = html.Div([
    dbc.Row(html.Div(['Data: ',dcc.DatePickerSingle(id='data-registro',date=datetime.today().strftime('%Y-%m-%d'))], className='pb-1')),
    dbc.Row(html.Div(['Precipitação (mm):   ',dcc.Input(id='precipitacao-mm', type="number",style={'width':'10em'})])),
    dbc.Row(dbc.Button('Salvar',color='primary',className='me-1', style={'width':'10em'}), className = 'pt-3')
]

)


layout_home = html.Div([
    html.H3('Precipitação'),
    dbc.Row([
       dbc.Col(card_generico("Gráfico 1",'esse é o primeiro texto',forecast_plot),width=7),
       dbc.Col(card_generico("Gráfico 2",'',''),width=5),
   ], className='mb-4'),
    dbc.Row([
       dbc.Col(card_generico("Gráfico 3",'',''),width=6),
       dbc.Col(card_generico("Registro de medidas",'',card_registro_medidas),width=6),
   ], className='mb-4'),
])


layout = layout.main_layout(layout_home)

@callback(
    Output('previsao-10dias','figure'),
    Input('data-inicio-previsao','date')
)
def update_previsao10dias(data):
    return plot_grafico_previsao(data)