# Generated by Django 2.1.4 on 2018-12-18 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20181215_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailauthcode',
            name='send_type',
            field=models.CharField(choices=[('register', 'register'), ('forget', 'retrieve password'), ('update_email', 'update email')], max_length=20, verbose_name='auth code type'),
        ),
    ]
