import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ITECH_Word_Game.settings')

import django
django.setup()

from django.contrib.auth.models import User
from django import views

import django
django.setup()
from wordgame.models import Statistics, UserProfile, Challenge

def populate():

    # players to populate database with
    players = {
        'Tom':{'score': 100, 'games_played': 100, 'win_streak': 25, 'games_won': 50, 'games_lost':50},
        'Jerry':{'score': 50, 'games_played': 25, 'win_streak': 6, 'games_won': 10, 'games_lost':15},
        'Mario':{'score': 200, 'games_played': 200, 'win_streak': 50, 'games_won': 100, 'games_lost':100},
        'Bowser':{'score': 300, 'games_played': 100, 'win_streak': 25, 'games_won': 50, 'games_lost':50}}

    challenges = [
        {'word':'WORD','word_length':4},
        {'word':'PROGRAM','word_length':7},
        {'word':'BOOK','word_length':4},
        {'word':'WORM','word_length':4},
        {'word':'FOOD','word_length':4},
    ]

    for challenge in challenges:
        add_challenge(challenge.get('word'), challenge.get('word_length'))

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

def add_challenge(word, word_length):
    challenge = Challenge.objects.get_or_create(word=word, word_length=word_length)[0]
    challenge.save()
    return challenge

# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()