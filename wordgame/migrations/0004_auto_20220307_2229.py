# Generated by Django 2.1.5 on 2022-03-07 22:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wordgame', '0003_challenge_game'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('correct_rate', models.IntegerField(default=0)),
                ('time_cost', models.IntegerField(default=0)),
                ('visible', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Statistics',
            },
        ),
        migrations.RemoveField(
            model_name='score',
            name='user',
        ),
        migrations.DeleteModel(
            name='Score',
        ),
    ]
