# Generated by Django 3.0.8 on 2021-04-14 05:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('People', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='BaseAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_account', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CreateAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_name', models.CharField(max_length=100, unique=True)),
                ('account_code', models.IntegerField(unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('total_debit', models.DecimalField(decimal_places=2, default='0.00', max_digits=12)),
                ('total_credit', models.DecimalField(decimal_places=2, default='0.00', max_digits=12)),
                ('account_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='createaccount_account_type', to='Accountant.AccountType')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('trnsaction_type', models.CharField(blank=True, max_length=100)),
                ('status', models.BooleanField(default=False)),
                ('total_debit', models.DecimalField(decimal_places=2, default='0.00', max_digits=12)),
                ('total_credit', models.DecimalField(decimal_places=2, default='0.00', max_digits=12)),
                ('balance', models.DecimalField(decimal_places=2, default='0.00', max_digits=12)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction_account', to='Accountant.CreateAccount')),
            ],
        ),
        migrations.CreateModel(
            name='ManualJournal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voucher_no', models.CharField(max_length=100)),
                ('voucher_date', models.DateField()),
                ('reference', models.CharField(blank=True, max_length=100)),
                ('notes', models.TextField(blank=True)),
                ('particular', models.TextField(blank=True)),
                ('debit', models.DecimalField(blank=True, decimal_places=2, default='0.00', max_digits=12)),
                ('credit', models.DecimalField(blank=True, decimal_places=2, default='0.00', max_digits=12)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journal_account', to='Accountant.CreateAccount')),
                ('people_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journal_people_by', to='People.People')),
                ('people_for_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journal_people_for', to='People.People')),
            ],
        ),
        migrations.AddField(
            model_name='accounttype',
            name='base_account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounttype_baseaccount', to='Accountant.BaseAccount'),
        ),
    ]
