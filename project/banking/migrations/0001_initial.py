# Generated by Django 3.2.5 on 2021-07-23 01:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=80)),
                ('number', models.CharField(max_length=80)),
                ('Currency', models.CharField(max_length=5)),
                ('balance', models.FloatField()),
            ],
            options={
                'verbose_name': 'Account',
                'verbose_name_plural': 'Account',
            },
        ),
        migrations.CreateModel(
            name='BankingData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(db_index=True, default='', max_length=50, unique=True)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('DONE', 'DONE'), ('FAIL', 'FAIL')], default='PENDING', max_length=30)),
            ],
            options={
                'verbose_name': 'Search Banking Data',
                'verbose_name_plural': 'Search Banking Data',
            },
        ),
        migrations.CreateModel(
            name='Statement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('date', models.DateField()),
                ('amount', models.FloatField()),
                ('balance', models.FloatField()),
                ('concept', models.TextField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banking.account')),
            ],
            options={
                'verbose_name': 'Statement',
                'verbose_name_plural': 'Statements',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=80)),
                ('participation', models.CharField(max_length=80)),
                ('doc', models.CharField(max_length=20)),
                ('address', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('banking_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banking.bankingdata')),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
            },
        ),
        migrations.AddField(
            model_name='account',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banking.customer'),
        ),
    ]
