#import libraries
from os import name
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd


def daily_county_plotly(county):

    #Get table from SQL result
    daily_gender_table = pd.read_csv(r"test_data\train.csv")
    daily_gender_table['datetime']= daily_gender_table['datetime'].astype('str')
    
    if county=='1':        
        daily_gender_table = daily_gender_table.head(10)
        print(len(daily_gender_table))
    elif county=='2':
        daily_gender_table = daily_gender_table.head(20)  
        print(len(daily_gender_table))
    elif county=='3':
        daily_gender_table = daily_gender_table.head(30) 
        print(len(daily_gender_table))
    elif county=='4':
        daily_gender_table = daily_gender_table.head(40)  
        print(len(daily_gender_table))

    #Create graph object Figure object with data
    fig = go.Figure(data = go.Bar(name = 'Daily Cases: ' + county, x = daily_gender_table['datetime'], y = daily_gender_table['count']))
    
        

    #Update layout for graph object Figure
    fig.update_layout(barmode='stack', 
                      title_text = 'Daily Cases: ' + county,
                      paper_bgcolor = 'rgba(0,0,0,0)', 
                      plot_bgcolor = 'rgba(0,0,0,0)',
                      xaxis_title = 'Date',
                      yaxis_title = 'Total_Daily_Cases')
    
    return fig

county_options = ['1', '2', '3', '4' ]

#Create DjangoDash applicaiton
# app = DjangoDash(name='CountyPlot')
app = DjangoDash(name='CountyPlot', external_stylesheets=[dbc.themes.BOOTSTRAP])

#Configure app layout
app.layout = html.Div([
                html.Div([
                    
                    #Add dropdown for option selection
                    dcc.Dropdown(
                    id = 'county',
                    options = [{'label': i, 'value': i} for i in county_options],
                    value = 'Taipei City')],
                    style={'width': '25%', 'margin':'0px auto'}),

                html.Div([                 
                    dcc.Graph(id = 'county_plot', 
                              animate = True, 
                              style={"backgroundColor": "#FFF0F5"})])
                        ])

#Define app input and output callbacks
@app.callback(
               Output('county_plot', 'figure'),
              [Input('county', 'value')])
              
def display_value(value):
    """
    This function returns figure object according to value input
    Input: Value specified
    Output: Figure object
    """
    #Get daily cases plot with input value
    fig = daily_county_plotly(value)
    
    return fig
