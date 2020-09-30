# Generated by Django 3.0.8 on 2020-09-21 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('People', '0019_auto_20200817_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='people',
            name='contact',
            field=models.IntegerField(blank=True, unique=True),
        ),
        migrations.AlterField(
            model_name='people',
            name='nid',
            field=models.BigIntegerField(blank=True, unique=True),
        ),
        migrations.AlterField(
            model_name='people',
            name='tracking',
            field=models.BigIntegerField(blank=True, unique=True),
        ),
    ]
