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


layout_mais = html.Div([
    html.H3('Qualidade das previsões'),
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


layout = layout.main_layout(layout_mais)


