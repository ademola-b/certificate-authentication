# Generated by Django 4.2.6 on 2023-10-22 21:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certapp', '0010_signature'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='issue_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
