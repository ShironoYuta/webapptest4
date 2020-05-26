#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

from app import app

import quadratic_function

simulator_app = dash.Dash(name='simulation', server=app,
                          url_base_pathname='/simulation/')

simulator_app.layout = html.Div(
    children=[
        'a: ',
        dcc.Input(id='a', type='text'),
        'b: ',
        dcc.Input(id='b', type='text'),
        'c: ',
        dcc.Input(id='c', type='text'),
        html.Button(children='Start', id='start'),
        dcc.Graph(
            id="output-graph",
            figure={}
        ),
    ]
)


@simulator_app.callback(Output('output-graph', 'figure'),
                        [Input('start', 'n_clicks')],
                        [State('a', 'value'), 
                         State('b', 'value'), 
                         State('c', 'value')])
def update_output(n_clicks, a, b, c):
    data = quadratic_function.calculate(a, b, c)
    graph_data = [go.Scatter(
        x=data[0],
        y=data[1],
        mode='lines')]
    figure = {'data': graph_data,
              'layout': {
                  'title': 'Quadratic Function %sx^2+%sx+%s' % (a, b, c)}
              }
    return figure
