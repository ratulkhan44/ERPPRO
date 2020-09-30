# Generated by Django 3.0.8 on 2020-09-27 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accountant', '0014_auto_20200927_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manualjournal',
            name='credit',
            field=models.DecimalField(decimal_places=2, default='0.00', max_digits=12),
        ),
        migrations.AlterField(
            model_name='manualjournal',
            name='debit',
            field=models.DecimalField(decimal_places=2, default='0.00', max_digits=12),
        ),
    ]