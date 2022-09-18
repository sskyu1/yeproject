#import libraries
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connections
from django.contrib import messages
from django.urls import reverse
import pandas as pd
import pymysql.cursors
from plotly.offline import plot
import plotly.graph_objs as go
from datetime import datetime
from .utils import *
from .forms import *
from .models import FeedBack
import time
from .Dash_Apps import sqlalchemy_test

def chart(request):

    daily_gender_table = pd.read_csv(r"test_data\train.csv")
    total_cases = 10
    total_vaccination = 20
 
    #Return options for different counties
    county_options = [ 'a','b', 'c']

    #Plotly visualizations
    daily_gender_plot = daily_gender_plotly()
    total_age_plot = daily_gender_plotly()
    exam_stats_plot = daily_gender_plotly()
    daily_vacc_plot = daily_gender_plotly()
    total_vacc_plot = daily_gender_plotly()

    #Create form for web page
    form = FeedBackForm()

    #Return context to home page view
    context = {'total_case': total_cases,
               'total_vaccination': total_vaccination,
               'daily_gender_plot': daily_gender_plot,
               'total_age_plot': total_age_plot,
               'exam_stats_plot': exam_stats_plot,
               'daily_vacc_plot': daily_vacc_plot,
               'total_vacc_plot': total_vacc_plot,
               'form': form}
        

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'test_app/index.html',
        context= context)

def db_test(request):
    sqlalchemy_test.sqlalchemy_db_test()
    return render(request, 'test_app/sqlacchemy.html')