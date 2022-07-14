#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import geopandas
import shapely
import shapefile
import plotly
from plotly.figure_factory._county_choropleth import create_choropleth
import plotly.express as px
import json
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
america_states = json.load(open('gz_2010_us_040_00_500k.json', 'r'))
state_id_map = {}
for feature in america_states['features']:
    feature['id'] = feature['properties']['STATE']
    state_id_map[feature['properties']['NAME']] = feature['id']
df = pd.read_csv("Homeless5.csv")
df['id'] = df['State'].apply(lambda x: state_id_map[x])
df1 = pd.read_csv("County1.csv")
values = df1['Homeless'].tolist()
fips = df1['id_county'].tolist()
colorscale = [
    'rgb(68.0, 1.0, 84.0)',
    'rgb(66.0, 64.0, 134.0)',
    'rgb(38.0, 130.0, 142.0)',
    'rgb(63.0, 188.0, 115.0)',
    'rgb(216.0, 226.0, 25.0)'
]
fig1 = create_choropleth(fips=fips, values=values, scope = ['CA'],
                           binning_endpoints=[1000, 5000, 10000, 30000], colorscale = colorscale,
                           county_outline={'color': 'rgb(255,255,255)', 'width': 1.5},
                           legend_title='Homeless count per County',
                           round_legend_values=True,
                           title = "Homeless Population in Californian Counties in 2016",
                           width=700, height=400)
fig1.layout.template = None
url_bar_and_content_div = html.Div([

    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')

])
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home Page", href="/")),
        dbc.NavItem(dbc.NavLink("Data", href="/page-1")),
        dbc.NavItem(dbc.NavLink("How You Can Help", href="/page-2")),
    ],
    className = "navbar",
    color="black",
    dark=True,
    brand="Homeless in California",
    brand_href="/",
)
layout_index = html.Div([

    dbc.Jumbotron(
    [
        html.H1("Help the Homeless", style = {'text-align': 'center'}),
        html.P(
            "Homelessness is increasing rapidly in the United States and we need your help to slow it down!",
            className="lead", style = {'text-align': 'center'}
        ),
        html.Hr(className="my-2"),
        html.P(dbc.Button("Learn more", color="primary", href = '/page-1'), className="button", style = {'text-align': 'center'})
], className = "jumbotron"),
    html.Div([
        html.Img(
            src = app.get_asset_url ('homeless.jpeg'),
            style={
                'height': '40%',
                'width': '40%'
            })
], style={'textAlign': 'center'})
])
layout_page_1 = html.Div([
    html.H1("Homelessness Statistics", style = {'text-align': 'center'}),

    html.Br(),
    html.Br(),

    html.H3("Homelessness in the United States: ", style = {'text-align': 'left'}),
    html.Br(),

    html.H5("The program below gives you a visual representation of the average amount of homeless people there are per year in the United States. (Takes a couple of seconds to load)" , style = {'text-align': 'center'}),

    html.Br(),
    html.Br(),

    html.H6("Select a Date: "),
    dcc.Dropdown(id = 'select_year',
                options = [
                    {'label' : '1/1/07', 'value' : '1/1/07'},
                    {'label' : '1/1/08', 'value' : '1/1/08'},
                    {'label' : '1/1/09', 'value' : '1/1/09'},
                    {'label' : '1/1/10', 'value' : '1/1/10'},
                    {'label' : '1/1/11', 'value' : '1/1/11'},
                    {'label' : '1/1/12', 'value' : '1/1/12'},
                    {'label' : '1/1/13', 'value' : '1/1/13'},
                    {'label' : '1/1/14', 'value' : '1/1/14'},
                    {'label' : '1/1/15', 'value' : '1/1/15'},
                    {'label' : '1/1/16', 'value' : '1/1/16'}],
                multi = False,
                value = '1/1/07',
                style = {'width' : '40%'},
                ),
    html.Div(id = 'output_container', children = []),
    html.Br(),

    dcc.Graph(id = 'Homeless_map', figure = {}),

    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),

    html.H3("Homelessness in California: ", style = {'text-align': 'left'}),
    html.Br(),
    html.H5("As you can see, California has the most homeless people in the United States by a wide margin! Let's delve deeper and see which areas are affected the most." , style = {'text-align': 'center'}),


    html.Div([
        html.Div([
        dcc.Graph(id='choro-map', figure = fig1),
        ], className="six columns"),
        html.Div([
             html.H5("Top 3 most affect counties:" ),
             html.H5("1) Los Angeles County "),
             html.H5("2) San Diego County " ),
             html.H5("3) San Francisco County "),
        ], className="six columns"),
    ], className="row")

])
layout_page_2 = html.Div([
    html.H1("How You Can Help", style = {'text-align': 'center'}),
    html.Br(),
    html.Br(),
    html.H3("The data page showed that there are many counties in California that have more homeless people that other states! "),
    html.H3("There are many ways you can help your community: "),
    html.Br(),
    html.H3("Firstly, you can contact a local shelter or visit their website to see what items you can donate to the shelter. "),
    html.H3("Some shelters have restrictions for what you can bring, so you should consult your local shelter first before you donate items."),
    html.Br(),
    html.H3("Secondly, you can volunteer at a shelter. Many shelters are looking for volunteers because they are running low."),
    html.H3("Contact your local shelter to see if you can help."),
    html.Br(),
    html.H3("Lastly, you can always help local homeless people on the streets by giving them money, food, or clothes."),

    html.Div([
        html.Img(
            src = app.get_asset_url('homeless3.png'),
            style={
                'height': '10%',
                'width': '10%'
            })
], style={'textAlign': 'center'})

])

app.layout = html.Div(
    [navbar, url_bar_and_content_div]
)

app.validation_layout = html.Div([
    url_bar_and_content_div,
    layout_index,
    layout_page_1,
    layout_page_2,
])

@app.callback(Output(component_id ='page-content', component_property ='children'),
              [Input(component_id ='url', component_property ='pathname')])
def display_page(pathname):
    if pathname == "/page-1":
        return layout_page_1
    elif pathname == "/page-2":
        return layout_page_2
    else:
        return layout_index

@app.callback(
    [Output(component_id = 'output_container', component_property = 'children'),
      Output(component_id = 'Homeless_map', component_property = 'figure')],
    [Input(component_id = 'select_year', component_property = 'value')]

)

def update_graph(option_selected):
    print(option_selected)
    print(type(option_selected))

    container = "The date that you chose was: {}".format(option_selected)

    dff = df.copy()
    dff = dff[dff['Year'] == option_selected]

    fig = px.choropleth(
                   data_frame = dff,
                   locations= 'id',
                   geojson = america_states,
                   color = 'Count',
                   scope = 'usa',
                   hover_name = 'State',
                   hover_data = ['Count'],
                   title = "Homeless People in the United States in {}".format(option_selected)
                   )


    return container, fig

@app.callback(Output('page-2-display-value', 'children'),
              [Input('page-2-dropdown', 'value')])
def display_value(value):
    print('display_value')
    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=False)









