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
import pandas as pd

### create dash intance ###

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] # default styles for Dash apps

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.scripts.config.serve_locally = True
server = app.server


### Load data ###
data = pd.read_csv('breaches.csv', thousands= ',')


### selector options ###
#~ sector_options = list(df['SECTOR'].unique())
#~ sensitivity_options = list(df['DATA SENSITIVITY'].unique())

sector_options = [

]


sensitivity_options = [
    {'value': 1, 'label': 'Just email address/Online information' }

]


print(sector_options)
print(sensitivity_options)


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
                                    options=sensitivity_options,
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
                                    options=sector_options,
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
                                id='year-slider',
                                min=2004,
                                max=2018,
                                value=[2004, 2018],
                                marks={i: i for i in range(2004, 2018+1)},
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
                dcc.Graph(id='main-graph')
            ],
        )
    ]
)


### Callbacks ###
# Slider -> year text
#~ @app.callback(Output('year_text', 'children'),
              #~ [Input('year_slider', 'value')])
#~ def update_year_text(year_slider):
    #~ return "{} | {}".format(year_slider[0], year_slider[1])


@app.callback(Output('main-graph', 'figure'),
              [Input('year-slider', 'value')]
            )
def make_main_figure(years):

    print (years)
    list_years_set = list(range(years[0], years[1] + 1))
    local_data = data[data['YEAR'].isin(list_years_set)]

    #~ sorted_lost_data = data['records lost'].sort_values(ascending=False)
    sorted_lost_data = local_data['records lost']
    entities = local_data['Entity']

    trace = dict(
        type='bar',
        x=data.index,
        y=sorted_lost_data,
        text=entities,
        name='Records lost',
    );

    layout = {
        'title': 'Records lost',
        'xaxis': {'title': 'Entity',
                    'titlefont': dict(
                        family='Courier New, monospace',
                        size=18,
                        color='#7f7f7f'
                )
        },
        'yaxis': {'title': 'Records lost',
                    'titlefont': dict(
                        family='Courier New, monospace',
                        size=18,
                        color='#7f7f7f'
                )
        }
    }

    figure = dict(data=[trace], layout=layout)

    return figure


# Selectors -> main graph
#~ @app.callback(Output('main_graph', 'figure'),
              #~ [Input('well_statuses', 'value'),
               #~ Input('well_types', 'value'),
               #~ Input('year_slider', 'value')],
              #~ [State('lock_selector', 'values'),
               #~ State('main_graph', 'relayoutData')])
#~ def make_main_figure(well_statuses, well_types, year_slider,
                     #~ selector, main_graph_layout):

    #~ dff = filter_dataframe(df, well_statuses, well_types, year_slider)

    #~ traces = []
    #~ for well_type, dfff in dff.groupby('Well_Type'):
        #~ trace = dict(
            #~ type='scattermapbox',
            #~ lon=dfff['Surface_Longitude'],
            #~ lat=dfff['Surface_latitude'],
            #~ text=dfff['Well_Name'],
            #~ customdata=dfff['API_WellNo'],
            #~ name=WELL_TYPES[well_type],
            #~ marker=dict(
                #~ size=4,
                #~ opacity=0.6,
                #~ color=WELL_COLORS[well_type]
            #~ )
        #~ )
        #~ traces.append(trace)

    #~ if (main_graph_layout is not None and 'locked' in selector):

        #~ lon = float(main_graph_layout['mapbox']['center']['lon'])
        #~ lat = float(main_graph_layout['mapbox']['center']['lat'])
        #~ zoom = float(main_graph_layout['mapbox']['zoom'])
        #~ layout['mapbox']['center']['lon'] = lon
        #~ layout['mapbox']['center']['lat'] = lat
        #~ layout['mapbox']['zoom'] = zoom
    #~ else:
        #~ lon = -78.05
        #~ lat = 42.54
        #~ zoom = 7

    #~ figure = dict(data=traces, layout=layout)
    #~ return figure





if __name__ == '__main__':

    print('Using version ' + dash.__version__ + ' of Dash.')
    print('Using version ' + dash_renderer.__version__ + ' of Dash renderer.')
    print('Using version ' + dcc.__version__ + ' of Dash Core Components.')
    print('Using version ' + html.__version__ + ' of Dash Html Components.')

    app.server.run(debug=True, threaded=True)

