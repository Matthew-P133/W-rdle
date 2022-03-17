import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ITECH_Word_Game.settings')

import django
django.setup()

from django.contrib.auth.models import User
from django import views

from wordgame.models import Statistics, UserProfile, Challenge, Dictionary

import re
from django.conf import settings

def populate():

    dictionary = os.path.join(settings.STATIC_DIR, 'wordlists/dictionary')
    targets = os.path.join(settings.STATIC_DIR, 'wordlists/targets')

    print('Adding dictionary words...')

    words = []
    for word in open(dictionary):
        word = word.strip().upper()
        if word and word.isalpha() and len(word) <= 12:
            print(word, end='\r')
            if not Dictionary.objects.filter(word=word):
                words.append(Dictionary(word=word))
    Dictionary.objects.bulk_create(words)

    print('Adding target words...')

    for word in open(targets):
        word = word.strip().upper()
        if word and word.isalpha() and len(word) <= 12:
            if not Challenge.objects.filter(word=word):
                challenge = Challenge.objects.create(word=word)
                challenge.save()  

    print('Creating made-up users...')

    # players to populate database with
    players = {
        'Tom':{'win_streak': 2, 'games_won': 5, 'games_lost':1},
        'Jerry':{'win_streak': 3, 'games_won': 10, 'games_lost':8},
        'Mario':{'win_streak': 1, 'games_won': 10, 'games_lost':10},
        'Bowser':{'win_streak': 0, 'games_won': 5, 'games_lost':5}}

    for player, player_data in players.items():
        add_player(player, player_data.get('win_streak'), player_data.get('games_won'), player_data.get('games_lost'))
    
 
def add_player(user, win_streak, games_won, games_lost):

    # create user
    new_user = User.objects.get_or_create(username=user,
                                 email='example.com')[0]
    new_user.set_password("passw0rd")
    new_user.save()

    # create their user profile
    profile = UserProfile.objects.get_or_create(user=new_user)[0]
    profile.save()

    # create statistics for user
    new_statistics = Statistics.objects.get_or_create(user=new_user, next_challenge = Challenge.objects.all()[0])[0]
    new_statistics.win_streak=win_streak
    new_statistics.games_lost = games_lost
    new_statistics.games_won = games_won
    new_statistics.save()
    return new_statistics

# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
    print('Database successfully populated.')