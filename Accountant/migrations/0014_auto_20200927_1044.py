# Generated by Django 3.0.8 on 2020-09-27 04:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('People', '0020_auto_20200921_1451'),
        ('Accountant', '0013_auto_20200924_1228'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='createaccount',
            name='credit',
        ),
        migrations.RemoveField(
            model_name='createaccount',
            name='debit',
        ),
        migrations.AddField(
            model_name='createaccount',
            name='total_credit',
            field=models.DecimalField(decimal_places=2, default='0.00', max_digits=12),
        ),
        migrations.AddField(
            model_name='createaccount',
            name='total_debit',
            field=models.DecimalField(decimal_places=2, default='0.00', max_digits=12),
        ),
        migrations.AlterField(
            model_name='manualjournal',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journal_account', to='Accountant.CreateAccount'),
        ),
        migrations.AlterField(
            model_name='manualjournal',
            name='credit',
            field=models.DecimalField(blank=True, decimal_places=2, default='0.00', max_digits=12),
        ),
        migrations.AlterField(
            model_name='manualjournal',
            name='debit',
            field=models.DecimalField(blank=True, decimal_places=2, default='0.00', max_digits=12),
        ),
        migrations.AlterField(
            model_name='manualjournal',
            name='people_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journal_people_by', to='People.People'),
        ),
        migrations.AlterField(
            model_name='manualjournal',
            name='people_for_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journal_people_for', to='People.People'),
        ),
    ]
