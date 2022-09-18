from django.urls import path, include
from . import views
from .Dash_Apps import county_plot

from yeproject.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
)

app_name = "test_app"
urlpatterns = [
    path('', views.chart, name = 'chart'),  
    path('db_test', views.db_test, name = 'db_test'),  
    ]
    

