from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The additional attributes we wish to include.
    def __str__(self):
        return self.user.username

class Score(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    score = models.IntegerField(default=0)
    correct_rate = models.IntegerField(default=0)
    time_cost = models.TimeField(default=0)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} ({self.score})({self.correct_rate})({self.time_cost})'
        