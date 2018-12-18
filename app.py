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
data = pd.read_csv('breaches_clean.csv', thousands= ',')
data['SECTOR'] = data['SECTOR'].apply(lambda sector: sector.split(', ')) # create list of sectors
# sort data by records lost
#~ data = data['records lost'].sort_values(ascending=False)
data.sort_values(by='records lost', inplace=True, ascending=False)


### selector options ###
#~ sector_options = list(df['SECTOR'].unique())
#~ sensitivity_options = list(df['DATA SENSITIVITY'].unique())

methods_list_names = ['All', 'Hacked', 'oops!', 'Poor security', 'Lost device', 'Inside job']
methods_list_values = ['all', 'hacked', 'oops!', 'poor security', 'lost device ', 'inside job']
methods_dict = { value: name for name, value in zip(methods_list_names, methods_list_values) }
method_options = [ { 'label': label, 'value': value} for label, value in zip(methods_list_names, methods_list_values) ]
method_color = {
    'all': '#0C0F25',
    'hacked' : '#903553',
    'oops!' : '#97BD5B',
    'poor security' : '#562972',
    'lost device ': '#EFAD24',
    'inside job': '#FFBAD2',
}

sector_list = ['web', 'retail', 'transport', 'government', 'telecoms',
        'app', 'healthcare', 'tech', 'financial', 'legal', 'gaming', 'media',
        'academic', 'energy', 'military'] # all options in data
sector_list.sort() #  Sort alphabetically
sector_list.insert(0, 'all') # add 'all' options to the front
sector_options = [ { 'label': sector, 'value': sector} for sector in sector_list ]


sensitivity_options = [
    {'value': 1, 'label': 'Just email address/Online information' },
    {'value': 2, 'label': 'SSN/Personal details' },
    {'value': 3, 'label': 'Credit card information' },
    {'value': 4, 'label': 'Health & other personal records' },
    {'value': 5, 'label': 'Full details' },
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
                    id='methods-selector',
                    options=method_options,
                    multi=True,
                    value=['all'],
                    placeholder='Select method...',
                    clearable=False
                ),
            ],
            className='container'
        ),

        #~ html.Div(
            #~ [
                #~ html.H5(
                    #~ '',
                    #~ id='breaches_text',
                    #~ className='two columns'
                #~ ),
                #~ html.H5(
                    #~ '',
                    #~ id='companies_text',
                    #~ className='eight columns',
                    #~ style={'text-align': 'center'}
                #~ ),
                #~ html.H5(
                    #~ '',
                    #~ id='years-text',
                    #~ className='two columns',
                    #~ style={'text-align': 'right'}
                #~ ),
            #~ ],
            #~ className='row container'
        #~ ),
        html.Div(
            [
                html.P('Filters:'),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.P('Filter by data sensitivity:'),
                                        dcc.Dropdown(
                                            id='data-sensitivity-select',
                                            options=sensitivity_options,
                                            multi=True,
                                            value=[1,2,3,4,5],
                                            placeholder='Select sensitivity options...',
                                        ),
                                    ],
                                    className='six columns'
                                ),
                                html.Div(
                                    [
                                        html.P('Filter by sector:'),
                                        dcc.Dropdown(
                                            id='sector-select',
                                            options=sector_options,
                                            multi=False,
                                            value='all',
                                            placeholder='Select sector...',
                                            clearable=False
                                        ),
                                    ],
                                    className='six columns'
                                ),
                            ],
                            className='row'
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
                            className='row',
                            style={'margin-top': '20'}
                        ),
                    ],
                )
            ],
            className='container',
            style={'margin-top': '20'},
        ),

        html.Hr(),

        html.Div(id='graphs')
    ]
)


### Helpers ###
def get_data_for_method (method: str, local_data: pd.DataFrame):
    if method == 'all':
        return local_data
    else:
        print(method)
        if method in methods_list_values: # Just in case
            return local_data[local_data['METHOD'] == method]
        else:
            raise Exception('method not found')


def method_header(method_name: str, records_lost_no: int, companies_affected_no: int):
    return html.Div(
            [
                html.H5(
                    f'Data for method: "{method_name}"',
                    className='four columns',
                    style={'text-align': 'center'}
                ),
                html.H5(
                    [html.Strong(records_lost_no),' records lost.'],
                    className='four columns',
                    style={'text-align': 'center'}
                ),
                html.H5(
                    [html.Strong(companies_affected_no),' companies affected.'],
                    #~ f'Total companies affected: "{companies_affected_no}"',
                    className='four columns',
                    style={'text-align': 'right'}
                ),
            ],
            className='row container'
        )


### Callbacks ###
# Slider -> year text
#~ @app.callback(Output('years-text', 'children'),
              #~ [Input('year-slider', 'value')]
              #~ )
#~ def update_year_text(year_slider):
    #~ return "{} | {}".format(year_slider[0], year_slider[1])


@app.callback(
            Output('graphs', 'children'),
            [
                Input('methods-selector', 'value'),
                Input('year-slider', 'value'),
                Input('data-sensitivity-select', 'value'),
                Input('sector-select', 'value'),
            ]
    )
def make_main_figure(methods, years, selected_sensitivities, selected_sector):

    # do a local copy of the data to not modify global data var
    local_data = data.copy(deep=True)

    # filter data

    # years slider
    print(f'Years selected: {years}')
    list_years_set = list(range(years[0], years[1] + 1))
    local_data = local_data[local_data['YEAR'].isin(list_years_set)]

    # data sensitivity dropdown
    print(f'Data sensitivity selected: {selected_sensitivities}')
    if selected_sensitivities != sensitivity_options:
        local_data = local_data [ local_data['DATA SENSITIVITY'].apply( lambda sensitivity: sensitivity in selected_sensitivities ) ]

    # sector dropdown selection
    print(f'Sector selected: {selected_sector}')
    if selected_sector != 'all':
        local_data = local_data [ local_data['SECTOR'].apply( lambda sectors: selected_sector in sectors ) ]


    # methods graphs
    # print one figure for each method selected

    graphs = []
    print(f'Methods selected: {methods}')
    for method in methods:
        method_name = methods_dict[method]
        method_data = get_data_for_method(method, local_data)

        lost_data = method_data['records lost']
        entities = method_data['Entity']

        trace = dict(
            type='bar',
            x=len(lost_data),
            y=lost_data,
            text=entities,
            name='Records lost',
            marker=dict(
                color = method_color[method],
            )
        );

        layout = {
            'title': f'Records lost by "{method_name}" method(s)',

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
        dash_graph = dcc.Graph(
                        id=f"graph-{method_name}",
                        figure=figure,
                        config={
                            'displaylogo': False,
                            'showLink': False,
                            'modeBarButtonsToRemove': ['sendDataToCloud']
                        }
                    )

        graphs.append(html.Div(
            [
                method_header(method_name, lost_data.sum(), len(lost_data)),
                dash_graph,
                html.Hr()
            ],
            style={'margin-bottom': '10'}
        ))


    return graphs


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

