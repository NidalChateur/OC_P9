# Generated by Django 4.2.3 on 2023-07-10 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0006_listing_band'),
    ]

    operations = [
        migrations.AddField(
            model_name='band',
            name='like_new',
            field=models.BooleanField(default=False),
        ),
    ]
