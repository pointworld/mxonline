# Generated by Django 2.1.4 on 2018-12-14 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_emailauthcode_slide'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female')], default='female', max_length=10, verbose_name='gender'),
        ),
    ]