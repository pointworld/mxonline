# Generated by Django 2.1.4 on 2018-12-15 20:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userconsulting',
            options={'verbose_name': 'user consulting', 'verbose_name_plural': 'user consulting'},
        ),
        migrations.AlterModelOptions(
            name='userfavorite',
            options={'verbose_name': 'User Favorite', 'verbose_name_plural': 'User Favorite'},
        ),
        migrations.AlterModelOptions(
            name='usermessage',
            options={'verbose_name': 'user message', 'verbose_name_plural': 'user message'},
        ),
    ]
