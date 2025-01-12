from dash import dcc, html, Input, Output, callback
from . import layout 

l = html.Div([
    html.H3('Page 1'),
    dcc.Dropdown(
        {f'Page 1 - {i}': f'{i}' for i in ['New York City', 'Montreal', 'Los Angeles']},
        id='page-1-dropdown'
    ),
    html.Div(id='page-1-display-value'),
    dcc.Link('Go to Page 2', href='/page2')
])

layout = layout.main_layout(l)


@callback(
    Output('page-1-display-value', 'children'),
    Input('page-1-dropdown', 'value'))
def display_value(value):
    return f'You have selected {value}'