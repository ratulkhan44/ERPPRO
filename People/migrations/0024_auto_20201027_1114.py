# Generated by Django 3.0.8 on 2020-10-27 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('People', '0023_auto_20201025_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='people',
            name='name',
            field=models.CharField(max_length=254),
        ),
        migrations.AlterField(
            model_name='people',
            name='nid',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='people',
            name='passport',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='people',
            name='tracking',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]
