from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
from . import layout
import plotly.graph_objs as go
import pandas as pd
import sqlite3
from datetime import datetime, timedelta



def plot_grafico_previsao(df):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['data_previsao'],
        y=df['valor_previsao']
    ))
    fig.update_layout(
        yaxis_title='Precipitação (mm)',
        margin=dict(l=20, r=20, t=5, b=5),
        template='plotly_white'
    )
    return fig

def plot_precipitacao_real(df):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['data'],
        y=df['precipitacao']
    ))
    fig.update_layout(
        yaxis_title='Precipitação (mm)',
        margin=dict(l=20, r=20, t=5, b=5),
        template='plotly_white'
    )
    return fig


def card_generico(titulo, texto, especifico, rodape=None):
    card = dbc.Card([
        dbc.CardHeader(titulo),
        dbc.CardBody([
            html.P(texto),
            especifico
        ]),
        dbc.CardFooter(rodape)
    ])

    return card

forecast_plot = html.Div([
    dbc.Row(html.Div(['Data:  ',dcc.DatePickerSingle(id='data-inicio-previsao',max_date_allowed=datetime.today().strftime('%Y-%m-%d'), date=datetime.today().strftime('%Y-%m-%d'))]),),
    dbc.Row(dcc.Graph(id='previsao-10dias', style={'padding':'10px'}))
])

data_inicio = datetime.today() - timedelta(days=30)
precip_plot = html.Div([
    dbc.Row(html.Div(['Intervalo:  ',
                      dcc.DatePickerRange(id='data-range',max_date_allowed=datetime.today(), start_date= data_inicio, end_date=datetime.today(),display_format='DD/MM/YYYY'),
                    ]),),
    dbc.Row(dcc.Graph(id='precipitacao-real', style={'padding':'10px'}))
])


forecast_day_plot = html.Div([
    dbc.Row(html.Div(['Data:  ',dcc.DatePickerSingle(id='data-previsao-dia',max_date_allowed=datetime.today().strftime('%Y-%m-%d'), date=datetime.today().strftime('%Y-%m-%d'),display_format='DD/MM/YYYY')]),),
    dbc.Row(dcc.Graph(id='previsao-ate-dia', style={'padding':'10px'}))
])

card_registro_medidas = html.Div([
    dbc.Row(html.Div(['Data: ',dcc.DatePickerSingle(id='data-registro',date=datetime.today().strftime('%Y-%m-%d'),max_date_allowed=datetime.today().strftime('%Y-%m-%d'),display_format='DD/MM/YYYY')], className='pb-1')),
    dbc.Row(html.Div(['Precipitação (mm):   ',dcc.Input(id='precipitacao-mm', type="number",style={'width':'10em'})])),
    dbc.Row([dbc.Button('Salvar',id='salvar-medida',color='primary',className='me-1', style={'width':'10em'}),html.Span(id='salvo-ok')], className = 'pt-3')
]

)


layout_home = html.Div([
    html.H3('Precipitação'),
    dbc.Row([
       dbc.Col(card_generico("Precipitação medida",'',precip_plot),width=6),
       dbc.Col(card_generico("Precipitação prevista",'',forecast_plot),width=6),
    ], className='mb-4'),
    dbc.Row([
       dbc.Col(card_generico("Registro de medidas",'',card_registro_medidas),width=6),
    ], className='mb-4'),
])


layout = layout.main_layout(layout_home)

@callback(
    Output('precipitacao-real','figure'),
    Input('dropdown-cidade','value'),
    Input('data-range','start_date'),
    Input('data-range', 'end_date')
)
def update_grafico_precipitacao_real(cidade,dt_inicio, dt_final):
    dt_ini = pd.to_datetime(dt_inicio).strftime("%Y%m%d")
    dt_fim = pd.to_datetime(dt_final).strftime("%Y%m%d")
    lt_conn = sqlite3.connect('precip.db')
    db_query = pd.read_sql_query(f'''select * from medidas where cidade="{cidade}" and data>{dt_ini} and data<{dt_fim}''', lt_conn)
    df = pd.DataFrame(db_query)
    lt_conn.close()

    df['data'] = df['data'].apply(str)
    df['data'] = df['data'].apply(lambda x: f'{x[0:4]}-{x[4:6]}-{x[6:]}')
  
    fig = plot_precipitacao_real(df)
    return fig


@callback(
    Output('previsao-10dias','figure'),
    Input('dropdown-cidade','value'),
    Input('data-inicio-previsao', 'date')
)
def update_grafico_previsao(cidade, data):
    data_real = pd.to_datetime(data).strftime("%Y%m%d")
    lt_conn = sqlite3.connect('precip.db')
    db_query = pd.read_sql_query(f'''select * from previsoes where cidade="{cidade}" and data_real={data_real}''', lt_conn)
    df = pd.DataFrame(db_query)
    lt_conn.close()
 
    df['data_previsao']=df['data_previsao'].apply(str)
    df['data_previsao']=df['data_previsao'].apply(lambda x: f'{x[0:4]}-{x[4:6]}-{x[6:]}')

    df['data_real']=df['data_real'].apply(str)
    df['data_real']=df['data_real'].apply(lambda x: f'{x[0:4]}-{x[4:6]}-{x[6:]}')

    fig = plot_grafico_previsao(df)

    return fig




@callback(
    Output('salvo-ok','children'),
    Input('salvar-medida','n_clicks'),
    State('dropdown-cidade','value'),
    State('data-registro','date'),
    State('precipitacao-mm','value')
)
def update_bd(nclicks, cidade, data, precipitacao):
    print(nclicks)
    if nclicks != None:
        dt = pd.to_datetime(data).strftime("%Y%m%d")
        lt_conn = sqlite3.connect('precip.db')
        db_cursor = lt_conn.cursor()

        insert = f'''Insert into medidas(cidade, data, precipitacao)
                    values ('{cidade}',{dt},{precipitacao});'''
        db_cursor.execute(insert)
        lt_conn.commit()
        db_cursor.close()
        lt_conn.close()
        return f'Salvo: {cidade} - {data}' 
    else:
        return ''