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

    words = []
    for word in open(dictionary):
        word = word.strip().upper()
        if word and word.isalpha() and len(word) <= 12:
            if not Dictionary.objects.filter(word=word):
                words.append(Dictionary(word=word))
    Dictionary.objects.bulk_create(words)

    for word in open(targets):
        word = word.strip().upper()
        if word and word.isalpha() and len(word) <= 12:
            if not Challenge.objects.filter(word=word):
                challenge = Challenge.objects.create(word=word)
                challenge.save()  

    # players to populate database with
    players = {
        'Tom':{'score': 100, 'games_played': 100, 'win_streak': 25, 'games_won': 50, 'games_lost':50},
        'Jerry':{'score': 50, 'games_played': 25, 'win_streak': 6, 'games_won': 10, 'games_lost':15},
        'Mario':{'score': 200, 'games_played': 200, 'win_streak': 50, 'games_won': 100, 'games_lost':100},
        'Bowser':{'score': 300, 'games_played': 100, 'win_streak': 25, 'games_won': 50, 'games_lost':50}}

    for player, player_data in players.items():
        add_statistics(player, player_data.get('score'), player_data.get('games_played'), player_data.get('win_streak'), player_data.get('games_won'), player_data.get('games_lost'))
    
 
def add_statistics(user, score, games_played, win_streak, games_won, games_lost):

    # create user
    new_user = User.objects.get_or_create(username=user,
                                 email='example.com',
                                 password='passw0rd')[0]
    new_user.save()

    # create their user profile
    profile = UserProfile.objects.get_or_create(user=new_user)[0]
    profile.save()

    # create statistics for user
    new_statistics = Statistics.objects.get_or_create(user=new_user, next_challenge = Challenge.objects.all()[0])[0]
    new_statistics.score=score
    new_statistics.games_played=games_played
    new_statistics.games_player = games_played
    new_statistics.win_streak=win_streak
    new_statistics.games_lost = games_lost
    new_statistics.games_won = games_won
    new_statistics.save()
    return new_statistics

# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()