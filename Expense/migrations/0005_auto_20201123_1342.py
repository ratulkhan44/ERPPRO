# Generated by Django 3.0.8 on 2020-11-23 07:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Expense', '0004_auto_20201123_1317'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='is_supervisior',
            new_name='is_supervisor',
        ),
    ]
