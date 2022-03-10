from django.db import models

from django.contrib.auth.models import User
# Create your models here.
from django.core.exceptions import ObjectDoesNotExist

class UserProfile(models.Model):
    SEX_CHOICES = (
        (0, 'man'),
        (1, 'woman')
    )
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The additional attributes we wish to include.
    photo = models.ImageField(upload_to='photots', null=True, blank=True)
    sex = models.IntegerField(choices=SEX_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.user.username

class Statistics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    score = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)
    games_won = models.IntegerField(default=0)
    games_lost = models.IntegerField(default=0)
    win_streak = models.IntegerField(default=0)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} ({self.score})({self.games_played})({self.games_won})'

    class Meta:
        verbose_name_plural = 'Statistics'

class Challenge(models.Model):
    word = models.CharField(max_length=10, unique=True, primary_key=True)
    timesPlayed = models.IntegerField(default=0)
    successes = models.IntegerField(default=0)
    failures = models.IntegerField(default=0)
    word_length = models.IntegerField()


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    guesses = models.IntegerField(default=0)
    successful = models.BooleanField(default=False)

    # user and challengeID make up the composite primary key (neither are unique alone)

    def __str__(self):
        return f'Game #{self.challengeID} played by {self.user.username}'
