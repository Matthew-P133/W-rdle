# Generated by Django 2.1.5 on 2022-03-09 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wordgame', '0006_auto_20220307_2331'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='photots'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='sex',
            field=models.IntegerField(blank=True, choices=[(0, 'man'), (1, 'woman')], null=True),
        ),
    ]