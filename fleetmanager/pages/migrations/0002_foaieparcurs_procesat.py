# Generated by Django 3.2.12 on 2022-04-26 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='foaieparcurs',
            name='procesat',
            field=models.BooleanField(default=False),
        ),
    ]
