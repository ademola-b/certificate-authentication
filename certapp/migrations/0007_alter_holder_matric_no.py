# Generated by Django 4.2.6 on 2023-10-21 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certapp', '0006_alter_holder_matric_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holder',
            name='matric_no',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
