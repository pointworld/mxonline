# Generated by Django 2.1.4 on 2018-12-17 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_course_course_org'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.CharField(default='backend', max_length=20, verbose_name='course category'),
        ),
    ]
