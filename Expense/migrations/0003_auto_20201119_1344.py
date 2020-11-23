# Generated by Django 3.0.8 on 2020-11-19 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Expense', '0002_expense_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='is_accounts',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='expense',
            name='is_executive',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='expense',
            name='is_supervisior',
            field=models.BooleanField(default=False),
        ),
    ]