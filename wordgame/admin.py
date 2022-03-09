from django.contrib import admin
from wordgame.models import UserProfile, Challenge, Game, Statistics
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Challenge)
admin.site.register(Statistics)
admin.site.register(Game)
