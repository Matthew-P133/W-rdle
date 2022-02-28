from django.urls import path
from wordgame import views

app_name = 'wordgame'

urlpatterns = [
    path('', views.index, name='index'),
]