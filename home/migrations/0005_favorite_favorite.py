# Generated by Django 4.2.6 on 2023-10-19 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='favorite',
            name='favorite',
            field=models.BooleanField(default=False),
        ),
    ]
