# Generated by Django 2.1.4 on 2018-12-15 20:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'verbose_name': 'Course'},
        ),
        migrations.AlterModelOptions(
            name='courseresource',
            options={'verbose_name': 'Course Resource'},
        ),
        migrations.AlterModelOptions(
            name='lesson',
            options={'verbose_name': 'Lesson'},
        ),
        migrations.AlterModelOptions(
            name='video',
            options={'verbose_name': 'Video'},
        ),
    ]