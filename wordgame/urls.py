from django.urls import path
from wordgame import views

app_name = 'wordgame'

urlpatterns = [
    path('', views.game, name='game'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]