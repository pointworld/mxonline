# Generated by Django 2.1.4 on 2018-12-15 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_auto_20181215_2004'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='course_nums',
            field=models.IntegerField(default=0, verbose_name='number of courses'),
        ),
        migrations.AddField(
            model_name='courseorg',
            name='learners',
            field=models.IntegerField(default=0, verbose_name='number of learners'),
        ),
    ]