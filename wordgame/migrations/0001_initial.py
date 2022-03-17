# Generated by Django 2.1.5 on 2022-03-17 09:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('word', models.CharField(max_length=10)),
                ('timesPlayed', models.IntegerField(default=0)),
                ('successes', models.IntegerField(default=0)),
                ('failures', models.IntegerField(default=0)),
                ('word_length', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guesses', models.IntegerField(default=0)),
                ('successful', models.BooleanField(default=False)),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wordgame.Challenge')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('games_played', models.IntegerField(default=0)),
                ('games_won', models.IntegerField(default=0)),
                ('games_lost', models.IntegerField(default=0)),
                ('win_streak', models.IntegerField(default=0)),
                ('visible', models.BooleanField(default=True)),
                ('next_challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wordgame.Challenge')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Statistics',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photots')),
                ('sex', models.IntegerField(blank=True, choices=[(0, 'man'), (1, 'woman')], null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
