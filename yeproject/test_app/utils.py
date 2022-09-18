#import libraries
import pandas as pd
from plotly.offline import plot
from plotly.subplots import make_subplots
import plotly.graph_objs as go


def daily_gender_plotly():    
    #Get table from SQL result
    daily_gender_table = pd.read_csv(r"test_data\train.csv")
    daily_gender_table['datetime']= daily_gender_table['datetime'].astype('str')
    #Initiate plot data list and append plot object to the list
    plot_data = []
    for gender in daily_gender_table['season'].unique():
        sub_df = daily_gender_table[daily_gender_table['season'] == gender]
        plot_data.append(go.Bar(name = str(gender), x = sub_df['datetime'], y = sub_df['count']))
    
    #Create graph object Figure object with plot data
    fig = go.Figure(data = plot_data)

    #Update layout for graph object Figure
    fig.update_layout(barmode='stack', 
                      title_text = 'Daily Cases By Gender',
                      paper_bgcolor = 'rgba(0,0,0,0)', 
                      plot_bgcolor = 'rgba(0,0,0,0)',
                      xaxis_title = 'Date',
                      yaxis_title = 'Daily_Cases')
    
    #Turn graph object into local plotly graph
    daily_gender_plot = plot({'data': fig}, output_type='div')
    
    # daily_gender_plot = plot({'data': fig}, auto_open=True, image = 'png', image_filename='plot_image',
    #          output_type='file', image_width=800, image_height=600, 
    #          filename='temp-plot.html', validate=False
    #          )    
    return daily_gender_plot
