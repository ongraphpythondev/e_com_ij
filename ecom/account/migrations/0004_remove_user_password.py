# Generated by Django 3.2.7 on 2022-01-03 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_phoneotp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='password',
        ),
    ]
