# Generated by Django 3.0.8 on 2020-09-21 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accountant', '0005_auto_20200921_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manualjournal',
            name='credit',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='manualjournal',
            name='debit',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='manualjournal',
            name='voucher_no',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]