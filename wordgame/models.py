from unicodedata import decimal
from django.db import models

from django.contrib.auth.models import User
from django.db.models import Avg


# Create your models here.


class UserProfile(models.Model):
    SEX_CHOICES = (
        (0, 'male'),
        (1, 'female')
    )
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The additional attributes we wish to include.
    photo = models.ImageField(upload_to='photos', null=True, blank=True)
    sex = models.IntegerField(choices=SEX_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.user.username

class Challenge(models.Model):

    id = models.AutoField(unique=True, primary_key=True)
    word = models.CharField(max_length=12)
    timesPlayed = models.IntegerField(default=0)
    successes = models.IntegerField(default=0)
    failures = models.IntegerField(default=0)
    word_length = models.IntegerField()

    def save(self, *args, **kwargs):
        self.word_length = len(self.word)
        self.timesPlayed = self.successes + self.failures
        super().save(*args, **kwargs) 


class Statistics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    score = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)
    games_won = models.IntegerField(default=0)
    games_lost = models.IntegerField(default=0)
    win_streak = models.IntegerField(default=0)
    visible = models.BooleanField(default=True)
    next_challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    average_guesses = models.DecimalField(decimal_places=2, max_digits=5, default=0)

    @property
    def ranking(self):
        return Statistics.objects.filter(score__gt=self.score).count() + 1

    def __str__(self):
        return f'{self.user.username} ({self.score})({self.games_played})({self.games_won})'
        # return self.user

    class Meta:
        verbose_name_plural = 'Statistics'

    def save(self, *args, **kwargs):
        self.games_played = self.games_lost + self.games_won
        
        calculated_score = self.games_won + self.games_won * self.win_streak
        self.score = round(calculated_score)

        if self.games_played > 0:
            self.average_guesses = calculate_average_guesses(self.user)


        super().save(*args, **kwargs) 


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    guesses = models.IntegerField(default=0)
    successful = models.BooleanField(default=False)

    # user and challengeID make up the composite primary key (neither are unique alone)

    def __str__(self):
        return f'Game #{self.challenge.id} played by {self.user.username}'
        

class Dictionary(models.Model):
    word = models.CharField(max_length=10, unique=True, primary_key=True)


def calculate_average_guesses(user):
    average_guesses = Game.objects.filter(user=user, successful=True).aggregate(Avg('guesses'))
    if average_guesses['guesses__avg']:
        print(average_guesses['guesses__avg'])
        return average_guesses['guesses__avg']
    else:
        return 0
