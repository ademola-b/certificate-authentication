# Generated by Django 4.2.6 on 2023-10-21 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('certapp', '0002_remove_holder_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='holder',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='certapp.holder'),
        ),
    ]
