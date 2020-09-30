# Generated by Django 3.0.8 on 2020-08-17 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('People', '0017_auto_20200816_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='contact',
            field=models.BigIntegerField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='people',
            name='nid',
            field=models.BigIntegerField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='people',
            name='tracking',
            field=models.BigIntegerField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]