# Generated by Django 2.2.2 on 2020-03-29 19:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20200304_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tedsearchterm',
            name='keyword',
            field=models.CharField(max_length=200, validators=[django.core.validators.RegexValidator(message='Keyword is not a single word.', regex='^[\\S]*$')]),
        ),
    ]
