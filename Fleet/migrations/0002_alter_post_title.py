# Generated by Django 5.1.7 on 2025-04-26 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Fleet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
