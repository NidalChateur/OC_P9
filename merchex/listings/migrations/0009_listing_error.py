# Generated by Django 4.2.3 on 2023-07-10 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0008_remove_band_like_new'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='error',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
