#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   app.py

   Descp: Dashboard to visualize data breaches.

   Created on: 16-dic-2018

   Copyright 2018 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""

### imports ###
import dash
import dash_renderer
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

### create dash intance ###

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] # default styles for Dash apps

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.scripts.config.serve_locally = True
server = app.server

### Define app layout ###
app.layout = html.Div(
    [
        html.Div(
            [
                html.H1(
                    'Data breaches overview',
                    className='twelve columns',
                    id='title'
                ),
            ],
            className='row'
        ),
        html.Div(
            [
                html.P('Select methods used for the data breach:'),
                dcc.Dropdown(
                    id='methods_selector',
                    options=[],
                    multi=True,
                    value=[]
                ),
            ],
            className='container'
        ),

        html.Div(
            [
                html.H5(
                    '',
                    id='breaches_text',
                    className='two columns'
                ),
                html.H5(
                    '',
                    id='companies_text',
                    className='eight columns',
                    style={'text-align': 'center'}
                ),
                html.H5(
                    '',
                    id='years_text',
                    className='two columns',
                    style={'text-align': 'right'}
                ),
            ],
            className='row'
        ),
        html.Div(
            [
                html.P('Filters:'),
                html.Div(
                    [
                        html.Div(
                            [
                                html.P('Filter by data sensitivity:'),
                                dcc.RadioItems(
                                    id='data-sensitivity-selector',
                                    options=[
                                        {'label': 'All ', 'value': 'all'},
                                        {'label': 'Active only ', 'value': 'active'},
                                        {'label': 'Customize ', 'value': 'custom'}
                                    ],
                                    value='all',
                                    labelStyle={'display': 'inline-block'}
                                ),
                                dcc.Dropdown(
                                    id='well_types_2',
                                    options=[],
                                    multi=True,
                                    value=[],
                                ),
                            ],
                            className='six columns'
                        ),
                        html.Div(
                            [
                                html.P('Filter by sector:'),
                                dcc.RadioItems(
                                    id='sector-selector',
                                    options=[
                                        {'label': 'All ', 'value': 'all'},
                                        {'label': 'Productive only ', 'value': 'productive'},
                                        {'label': 'Customize ', 'value': 'custom'}
                                    ],
                                    value='all',
                                    labelStyle={'display': 'inline-block'}
                                ),
                                dcc.Dropdown(
                                    id='well_types',
                                    options=[],
                                    multi=True,
                                    value=[],
                                ),
                            ],
                            className='six columns'
                        ),
                        html.Div(
                        [
                            html.P('Filter by data breach date:'),
                            dcc.RangeSlider(
                                id='year_slider',
                                min=1960,
                                max=2017,
                                value=[1990, 2010]
                            ),
                        ],
                        style={'margin-top': '20'}
                    ),
                ],
                className='row'
                )
            ],
            className='container'
        ),

        html.Hr(),

        html.Div(
            [
                dcc.Graph(id='main_graph')
            ],
        )
    ]
)



if __name__ == '__main__':

    print('Using version ' + dash.__version__ + ' of Dash.')
    print('Using version ' + dash_renderer.__version__ + ' of Dash renderer.')
    print('Using version ' + dcc.__version__ + ' of Dash Core Components.')
    print('Using version ' + html.__version__ + ' of Dash Html Components.')

    app.server.run(debug=True, threaded=True)

