from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
from . import layout
import plotly.graph_objs as go
import pandas as pd
import sqlite3
from datetime import datetime

cidade = "Katueté"

def plot_grafico_previsao(data):
    #print(pd.to_datetime(data).strftime("%Y%m%d"))
    lt_conn = sqlite3.connect('precip.db')
    db_query = pd.read_sql_query('''select * from previsoes ''', lt_conn)
    df = pd.DataFrame(db_query)
    lt_conn.close()
    
    df['data_previsao']=df['data_previsao'].apply(str)
    df['data_previsao']=df['data_previsao'].apply(lambda x: f'{x[0:4]}-{x[4:6]}-{x[6:]}')

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['data_previsao'],
        y=df['valor_previsao']
    ))
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
    dbc.Row(html.Div(['Data: ',dcc.DatePickerSingle(id='data-registro',date=datetime.today().strftime('%Y-%m-%d'),max_date_allowed=datetime.today().strftime('%Y-%m-%d'))], className='pb-1')),
    dbc.Row(html.Div(['Precipitação (mm):   ',dcc.Input(id='precipitacao-mm', type="number",style={'width':'10em'})])),
    dbc.Row([dbc.Button('Salvar',id='salvar-medida',color='primary',className='me-1', style={'width':'10em'}),html.Span(id='salvo-ok')], className = 'pt-3')
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

@callback(
    Output('salvo-ok','children'),
    Input('salvar-medida','n_clicks'),
    State('data-registro','date'),
    State('precipitacao-mm','value')
)
def update_bd(nclicks, data, precipitacao):
    print(nclicks)
    if nclicks != None:
        dt = print(pd.to_datetime(data).strftime("%Y%m%d"))
        lt_conn = sqlite3.connect('precip.db')
        db_cursor = lt_conn.cursor()

        insert = f'''Insert into medidas(cidade, data, precipitacao)
                    values ('{cidade}',{data},{precipitacao});'''
        db_cursor.execute(insert)
        lt_conn.commit()
        db_cursor.close()
        lt_conn.close()
        return 'Salvo - ' + data
    else:
        return ''