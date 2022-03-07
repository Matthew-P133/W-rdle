import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ITECH_Word_Game.settings')

import django
django.setup()

from django.contrib.auth.models import User
from django import views

import django
django.setup()
from wordgame.models import Statistics, UserProfile

def populate():

    # players to populate database with
    players = {
        'Tom':{'score': 100, 'correct_rate': 100, 'time_cost': 100},
        'Jerry':{'score': 99, 'correct_rate': 99, 'time_cost': 99},
        'Mario':{'score': 98, 'correct_rate': 98, 'time_cost': 98},
        'Bowser':{'score': 97, 'correct_rate': 97, 'time_cost': 97}}

    for player, player_data in players.items():
        add_statistics(player, player_data.get('score'), player_data.get('correct_rate'), player_data.get('time_cost'))
    

def add_statistics(user, score, correct_rate, time_cost):

    # create user
    new_user = User.objects.get_or_create(username=user,
                                 email='example.com',
                                 password='passw0rd')[0]
    new_user.save()

    # create their user profile
    profile = UserProfile.objects.get_or_create(user=new_user)[0]
    profile.save()

    # create statistics for user
    new_statistics = Statistics.objects.get_or_create(user=new_user)[0]
    new_statistics.score=score
    new_statistics.correct_rate=correct_rate
    new_statistics.time_cost=time_cost
    new_statistics.save()
    return new_statistics

# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()