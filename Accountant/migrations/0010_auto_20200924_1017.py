# Generated by Django 3.0.8 on 2020-09-24 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accountant', '0009_auto_20200922_1010'),
    ]

    operations = [
        migrations.AddField(
            model_name='createaccount',
            name='credit',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='createaccount',
            name='debit',
            field=models.IntegerField(default=0),
        ),
    ]
