# Generated by Django 3.2.5 on 2021-07-25 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banking', '0005_alter_bankingdata_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankingdata',
            name='task_id',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
    ]
