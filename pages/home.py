from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
from . import layout
import plotly.graph_objs as go
import pandas as pd
import sqlite3
from datetime import datetime



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

def plot_previsao_vs_real(df): #refazer!!
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['valor_medida'],
        y=df['valor_previsao']
    ))
    fig.update_layout(
        xaxis_title='Precipitação Real (mm)',
        yaxis_title='Precipitação Prevista (mm)',
        margin=dict(l=20, r=20, t=10, b=5),
        template='plotly_white'
    )
    return fig 

def plot_previsao_ate_dia(df,precipitacao):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['data_real'],
        y=df['valor_previsao']
    ))
    
    if precipitacao>0:
        print(precipitacao)
        fig.add_hline(y=precipitacao)


    fig.update_layout(
        yaxis_title='Precipitação (mm)',
        margin=dict(l=20, r=20, t=5, b=5),
        template='plotly_white'
    )
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
    dbc.Row(html.Div(['Data:  ',dcc.DatePickerSingle(id='data-inicio-previsao',max_date_allowed=datetime.today().strftime('%Y-%m-%d'), date=datetime.today().strftime('%Y-%m-%d'))]),),
    dbc.Row(dcc.Graph(id='previsao-10dias', style={'padding':'10px'}))
])

forecast_real_plot = html.Div([
    dbc.Row([dbc.Col(html.Div(['Mês:   ',dcc.Dropdown(['01','02','03','04','05','06','07','08','09','10','11','12'],'01',id='dropdown-mes-forecast-real',style={'width':'5em'})])),
            dbc.Col(html.Div(['Ano:   ',dcc.Dropdown(['2024','2025'],'2025',id='dropdown-ano-forecast-real',style={'width':'6em'})])),
            dbc.Col(html.Div(['Intervalo*: ', dcc.Dropdown(['1','2','3','4','5','6','7','8','9','10'],'5',id='dropdown-dt-forecast-real',style={'width':'5em'})]))]),
    dbc.Row(dcc.Graph(id='forecast-vs-real', style={'padding':'5px'})),
    dbc.Row(html.Div('* (previsto x dias antes)'))
])

forecast_day_plot = html.Div([
    dbc.Row(html.Div(['Data:  ',dcc.DatePickerSingle(id='data-previsao-dia',max_date_allowed=datetime.today().strftime('%Y-%m-%d'), date=datetime.today().strftime('%Y-%m-%d'))]),),
    dbc.Row(dcc.Graph(id='previsao-ate-dia', style={'padding':'10px'}))
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
       dbc.Col(card_generico("Precipitação prevista",'',forecast_plot),width=6),
       dbc.Col(card_generico("Previsões para um dia",'',forecast_day_plot),width=6),
       #dbc.Col(card_generico("Previsto vs. Real",'',forecast_real_plot),width=5),
   ], className='mb-4'),
    dbc.Row([
       #dbc.Col(card_generico("Previsões para um dia",'',''),width=6),
       dbc.Col(card_generico("Registro de medidas",'',card_registro_medidas),width=6),
   ], className='mb-4'),
])


layout = layout.main_layout(layout_home)


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

#@callback(
#    Output('forecast-vs-real','figure'),
#    Input('dropdown-mes-forecast-real','value'),
#    Input('dropdown-ano-forecast-real','value'),
#    Input('dropdown-dt-forecast-real','value'),
#    Input('dropdown-cidade','value')
#)
#def update_plot_previsao_vs_real(mes,ano,deltat,cidade):
#
#    lt_conn = sqlite3.connect('precip.db')
#    db_query = pd.read_sql_query(f'''select * from previsoes where cidade="{cidade}" and data_real={data_real}''', lt_conn)
#    df = pd.DataFrame(db_query)
#    lt_conn.close()
#    print(df)
#    
#    fig = plot_previsao_vs_real(df)
#    return fig

@callback(
    Output('previsao-ate-dia','figure'),
    Input('dropdown-cidade','value'),
    Input('data-previsao-dia','date'),
)
def update_plot_previsao_ate_dia(cidade,data):
    print('Data',data)
    data_previsao = pd.to_datetime(data).strftime("%Y%m%d")
    lt_conn = sqlite3.connect('precip.db')
    db_query = pd.read_sql_query(f'''select * from previsoes where cidade="{cidade}" and data_previsao={data_previsao}''', lt_conn)
    df = pd.DataFrame(db_query)
    lt_conn.close()
    print('dados',df)

    df['data_previsao']=df['data_previsao'].apply(str)
    df['data_previsao']=df['data_previsao'].apply(lambda x: f'{x[0:4]}-{x[4:6]}-{x[6:]}')

    df['data_real']=df['data_real'].apply(str)
    df['data_real']=df['data_real'].apply(lambda x: f'{x[0:4]}-{x[4:6]}-{x[6:]}')

    lt_conn = sqlite3.connect('precip.db')
    db_query = pd.read_sql_query(f'''select * from medidas where cidade="{cidade}" and data={data_previsao}''', lt_conn)
    df2 = pd.DataFrame(db_query)
    lt_conn.close()
    print(df2)
    
    precipitacao = df2['precipitacao']
    fig = plot_previsao_ate_dia(df,precipitacao[0])

    return fig