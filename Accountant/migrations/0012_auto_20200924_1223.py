# Generated by Django 3.0.8 on 2020-09-24 06:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Accountant', '0011_auto_20200924_1206'),
    ]

    operations = [
        migrations.RenameField(
            model_name='manualjournal',
            old_name='accounts',
            new_name='account',
        ),
    ]