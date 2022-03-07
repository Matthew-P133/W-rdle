import os

from django import views
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                    'ITECH_Word_Game.settings')

import django
django.setup()
from wordgame.models import Score

def populate():

    NPCs = [
        {'Tom':{'score': 100, 'correct_rate': 100, 'time_cost': 100, }},
        {'Jerry':{'score': 99, 'correct_rate': 99, 'time_cost': 99, }},
        {'Mario':{'score': 98, 'correct_rate': 98, 'time_cost': 98, }},
        {'Bowser':{'score': 97, 'correct_rate': 97, 'time_cost': 97, }},]

    for u, user_data in NPCs():
        add_user(u, user_data['score'], user_data['correct_rate'], user_data['time_cost'])
        

def add_user(u, score, correct_rate, time_cost):
    p = Score.objects.get_or_create(username=u)[0]
    p.score=score
    p.correct_rate=correct_rate
    p.time_cost=time_cost
    p.save()
    return p

# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()