# Generated by Django 2.2.2 on 2020-01-23 20:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medicines', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bnfpresentation',
            options={'ordering': ['code'], 'verbose_name': 'BNF Presentation'},
        ),
    ]
