# Generated by Django 3.0.8 on 2020-09-21 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accountant', '0006_auto_20200921_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manualjournal',
            name='credit',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='manualjournal',
            name='debit',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]