# Generated by Django 3.2.5 on 2021-07-23 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('banking', '0003_alter_statement_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statement',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statements', to='banking.account'),
        ),
    ]