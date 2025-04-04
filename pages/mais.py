from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
from . import layout
import plotly.graph_objs as go
import pandas as pd
import sqlite3
from datetime import datetime, timedelta





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



#forecast_real_plot = html.Div([
#    dbc.Row([dbc.Col(html.Div(['Mês:   ',dcc.Dropdown(['01','02','03','04','05','06','07','08','09','10','11','12'],'01',id='dropdown-mes-forecast-real',style={'width':'5em'})])),
#            dbc.Col(html.Div(['Ano:   ',dcc.Dropdown(['2024','2025'],'2025',id='dropdown-ano-forecast-real',style={'width':'6em'})])),
#            dbc.Col(html.Div(['Intervalo*: ', dcc.Dropdown(['1','2','3','4','5','6','7','8','9','10'],'5',id='dropdown-dt-forecast-real',style={'width':'5em'})]))]),
#    dbc.Row(dcc.Graph(id='forecast-vs-real', style={'padding':'5px'})),
#    dbc.Row(html.Div('* (previsto x dias antes)'))
#])

forecast_day_plot = html.Div([
    dbc.Row(html.Div(['Data:  ',dcc.DatePickerSingle(id='data-previsao-dia',max_date_allowed=datetime.today().strftime('%Y-%m-%d'), date=datetime.today().strftime('%Y-%m-%d'), display_format='DD/MM/YYYY')]),),
    dbc.Row(dcc.Graph(id='previsao-ate-dia', style={'padding':'10px'}))
])

data_inicio = datetime.today() - timedelta(days=30)
forecast_real_plot = html.Div([
    dbc.Row(html.Div(['Período:   ',dcc.DatePickerRange(id='periodo-dispersao',max_date_allowed=datetime.today(),  start_date= data_inicio, end_date=datetime.today(),display_format='DD/MM/YYYY')])),
    dbc.Row(dcc.Graph(id='previsao-real-dispersao', style={'padding':'10px'}))
])

forecast_real_boxplot = html.Div([
    dbc.Row(html.Div(['Período:   ',dcc.DatePickerRange(id='periodo-dispersao',max_date_allowed=datetime.today(),  start_date= data_inicio, end_date=datetime.today(),display_format='DD/MM/YYYY')])),
    dbc.Row(dcc.Graph(id='boxplot-diff',style={'padding':'10px'}))
])



layout_mais = html.Div([
    html.H3('Qualidade das previsões'),
    dbc.Row([
       dbc.Col(card_generico("Todas as previsões até dia",'',forecast_day_plot),width=6),
       dbc.Col(card_generico("Previsões vs Real",'',forecast_real_plot),width=6),
       #dbc.Col(card_generico("Previsto vs. Real",'',forecast_real_plot),width=5),
   ], className='mb-4'),
    dbc.Row([
       dbc.Col(card_generico("Previsões para um dia",'',forecast_real_boxplot),width=12),
       #dbc.Col(card_generico("Registro de medidas",'',card_registro_medidas),width=6),
   ], className='mb-4'),
])


layout = layout.main_layout(layout_mais)


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
    if len(df2)>0:
        precipitacao = df2['precipitacao'][0]
    else:
        precipitacao=0
    fig = plot_previsao_ate_dia(df,precipitacao)

    return fig
