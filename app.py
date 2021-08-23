# -*- coding: utf-8 -*-

# Run this app with `python app.py` and visit http://127.0.0.1:8050/ in your web browser.
# documentation at https://dash.plotly.com/
# based on ideas at "Dash App With Multiple Inputs" in https://dash.plotly.com/basic-callbacks
# mouse-over or 'hover' behavior is based on https://dash.plotly.com/interactive-graphing
# plotly express line parameters via https://plotly.com/python-api-reference/generated/plotly.express.line.html#plotly.express.line
# Mapmaking code initially learned from https://plotly.com/python/mapbox-layers/.


from flask import Flask
from os import environ

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json

#load markdown
introduction = open('introduction.md', 'r')
introduction_markdown = introduction.read()

with open('descriptions.json') as f:
    descriptions = json.load(f)

land_ocean_data = pd.read_csv("./land_ocean_filtered.csv")
climate_forcings_data = pd.read_csv("./climate_forcings_filtered.csv")
#averages_data = pd.read_csv("./averages.csv")


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = Flask(__name__)
app = dash.Dash(
    server=server,
    url_base_pathname=environ.get('JUPYTERHUB_SERVICE_PREFIX', '/'),
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True #because of the tabs, not all callbacks are accessible so we suppress callback exceptions
)

app.layout = html.Div([

    html.Div([
        dcc.Markdown(
            children=introduction_markdown
        ),
    ], style={'width': '80%', 'display': 'inline-block', 'padding': '0 20', 'vertical-align': 'middle', 'margin-bottom': 30, 'margin-right': 50, 'margin-left': 20}),

    #Tabs: https://dash.plotly.com/dash-core-components/tabs
    html.Div([
        dcc.Tabs(id='tabs', value='learn', children=[
            dcc.Tab(label='Learn', value='learn'),
            dcc.Tab(label='Explore', value='explore'),
        ]),
        html.Div(id='tabs-content')
    ], style={'width': '80%', 'display': 'inline-block', 'padding': '0 20', 'vertical-align': 'middle', 'margin-bottom': 30, 'margin-right': 50, 'margin-left': 20}),

], style={'width': '1000px'})

@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'learn':
        return html.Div([
            html.Div([
                dcc.Graph(
                    id='learn_graph',
                    figure={
                        'layout': {
                            'yaxis': {
                                'range': [-5, 5],
                                'autorange': False
                            }
                        }
                    },
                    config={
                        'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                    },
                ),
            ], style={'width': '80%', 'display': 'inline-block', 'vertical-align': 'middle'}),


            html.Div([
                dcc.Markdown('''
                        **Natural Factors**
                        '''),
                dcc.RadioItems(
                    id='natural_radiobuttons',
                    options=[
                        {'label': 'Orbital Changes', 'value': 'OC'},
                        {'label': 'Solar', 'value': 'S'},
                        {'label': 'Volcanic', 'value': 'V'}
                    ],
                ),

                dcc.Markdown('''
                        **Human Factors**
                        '''),
                dcc.RadioItems(
                    id='human_radiobuttons',
                    options=[
                        {'label': 'Land Use', 'value': 'LU'},
                        {'label': 'Ozone', 'value': 'O'},
                        {'label': 'Aerosols', 'value': 'A'},
                        {'label': 'Greenhouse Gases', 'value': 'GG'},
                    ],
                ),

                dcc.Markdown('''
                        **All Factors**
                        '''),
                dcc.RadioItems(
                    id='all_radiobuttons',
                    options=[
                        {'label': 'Natural', 'value': 'N'},
                        {'label': 'Human', 'value': 'H'},
                        {'label': 'All Forcings', 'value': 'ALL'}
                    ],
                ),

            ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'middle'}),


            html.Div([
                dcc.Markdown(
                    children='''**Text**''',
                    id='description',
                    style={'font-size': '14px'}, ),
            ])
        ])
    elif tab == 'explore':
        return html.Div([
            html.Div([
                dcc.Graph(
                    id='explore_graph',
                    figure={
                        'layout': {
                            'yaxis': {
                                'range': [-5, 5],
                                'autorange': False
                            }
                        }
                    },
                    config={
                        'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                    },
                ),
            ], style={'width': '80%', 'display': 'inline-block', 'vertical-align': 'middle'}),

            html.Div([
                dcc.Markdown('''
                        **Natural Factors**
                        '''),
                dcc.Checklist(
                    id='natural_checklist',
                    options=[
                        {'label': 'Orbital Changes', 'value': 'OC'},
                        {'label': 'Solar', 'value': 'S'},
                        {'label': 'Volcanic', 'value': 'V'}
                    ],
                    value=[],
                ),
                dcc.Markdown('''
                        **Human Factors**
                        '''),
                dcc.Checklist(
                    id='human_checklist',
                    options=[
                        {'label': 'Land Use', 'value': 'LU'},
                        {'label': 'Ozone', 'value': 'O'},
                        {'label': 'Aerosols', 'value': 'A'},
                        {'label': 'Greenhouse Gases', 'value': 'GG'},
                    ],
                    value=[],
                ),

                dcc.Markdown('''
                        **All Factors**
                        '''),
                dcc.Checklist(
                    id='all_checklist',
                    options=[
                        {'label': 'Natural', 'value': 'N'},
                        {'label': 'Human', 'value': 'H'},
                        {'label': 'All Forcings', 'value': 'ALL'}
                    ],
                    value=[],
                ),

            ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'middle'}),

        ])




@app.callback(
    Output(component_id='description', component_property='children'),
    Input(component_id='natural_radiobuttons', component_property='value'),
    Input(component_id='human_radiobuttons', component_property='value'),
    Input(component_id='all_radiobuttons', component_property='value'),
)
def update_description(natural, human, all):
    output = []

    if natural is not None:
        output += descriptions[natural]
    if human is not None:
        output += descriptions[human]
    if all is not None:
        output += descriptions[all]

    return output

def update_factors(fig, factors):
    #colors: https://www.w3schools.com/cssref/css_colors.asp
    #error bars: https://plotly.com/python/continuous-error-bars/
    colour_name = ['DeepSkyBlue', 'Orange', 'Red', 'Sienna', 'CadetBlue', 'MediumSlateBlue', 'SeaGreen', 'GreenYellow', 'DarkGrey', 'Purple']
    colour_rgb = ['rgba(0, 191, 255, 0.2)', 'rgba(255, 165, 0, 0.2)', 'rgba(255, 0, 0, 0.2)', 'rgba(136, 45, 23, 0.2)', 'rgba(95, 158, 160, 0.2)',
                  'rgba(123, 104, 238, 0.2)', 'rgba(46, 139, 87, 0.2)', 'rgba(173, 255, 47, 0.2)', 'rgba(169, 169, 169, 0.2)', 'rgba(128, 0, 128, 0.2)']
    name = ['OC', 'S', 'V', 'LU', 'O', 'A', 'GG', 'N', 'H', 'ALL']
    df_name = ['Orbital changes', 'Solar', 'Volcanic', 'Land use', 'Ozone', 'Anthropogenic tropospheric aerosol', 'Greenhouse gases',
               'Natural', 'Human', 'All forcings']
    for i in range(10):
        if name[i] in factors:
            new_fig = px.line(climate_forcings_data, x='Year', y=df_name[i], color_discrete_sequence=[colour_name[i]])
            new_fig_error = go.Figure([
                go.Scatter(name='Upper Bound', x=climate_forcings_data['Year'],
                           y=climate_forcings_data[df_name[i]] + climate_forcings_data['Error'],
                           mode='lines', marker=dict(color="#444"), line=dict(width=0), showlegend=False),
                go.Scatter(name='Lower Bound', x=climate_forcings_data['Year'],
                           y=climate_forcings_data[df_name[i]] - climate_forcings_data['Error'],
                           marker=dict(color="#444"), line=dict(width=0), mode='lines', fillcolor=colour_rgb[i],
                           fill='tonexty', showlegend=False)
            ])
            fig.add_traces(new_fig_error.data)
            fig.add_trace(new_fig.data[0])
    return fig


@app.callback(
    Output(component_id='learn_graph', component_property='figure'),
    Input(component_id='natural_radiobuttons', component_property='value'),
    Input(component_id='human_radiobuttons', component_property='value'),
    Input(component_id='all_radiobuttons', component_property='value'),
)
def update_plot(natural_radiobuttons, human_radiobuttons, all_radiobuttons):
    factors = [natural_radiobuttons] + [human_radiobuttons] + [all_radiobuttons]

    fig = px.line()
    fig.update_layout(plot_bgcolor='rgb(255, 255, 255)', yaxis_zeroline=True, yaxis_zerolinecolor='gainsboro', yaxis_showline=True, yaxis_linecolor='gainsboro')
    fig = update_factors(fig, factors)
    figTemp = px.line(land_ocean_data, x='Year', y='Annual_Mean', color_discrete_sequence=['black'])
    fig.add_trace(figTemp.data[0])
    fig.update_yaxes(title='Temperature (C)', range=[-1.2, 1.2])

    #annotation
    fig.add_annotation(x=2005, y=0.938064516129032,
                       text="<b>observed<br>temperature</b>",
                       showarrow=True,
                       arrowhead=1)

    return fig

@app.callback(
    Output(component_id='explore_graph', component_property='figure'),
    Input(component_id='natural_checklist', component_property='value'),
    Input(component_id='human_checklist', component_property='value'),
    Input(component_id='all_checklist', component_property='value'),
)
def update_plot(natural_checklist, human_checklist, all_checklist):
    factors = natural_checklist + human_checklist + all_checklist

    #fig = px.line(land_ocean_data, x='Year', y='Annual_Mean', color_discrete_sequence=['black'])
    fig = px.line()
    fig.update_layout(plot_bgcolor='rgb(255, 255, 255)', yaxis_zeroline=True, yaxis_zerolinecolor='gainsboro', yaxis_showline=True, yaxis_linecolor='gainsboro')
    fig = update_factors(fig, factors)
    figTemp = px.line(land_ocean_data, x='Year', y='Annual_Mean', color_discrete_sequence=['black'])
    fig.add_trace(figTemp.data[0])
    fig.update_yaxes(title='Temperature (C)', range=[-1.2, 1.2])

    #annotation
    fig.add_annotation(x=2005, y=0.938064516129032,
                       text="<b>observed<br>temperature</b>",
                       showarrow=True,
                       arrowhead=1)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)


