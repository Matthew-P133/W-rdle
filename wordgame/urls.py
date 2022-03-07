from django.urls import path
from wordgame import views

app_name = 'wordgame'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
    path('learderboard/', views.learderboard, name='leaderboard'),
]