# Generated by Django 4.2.3 on 2023-07-31 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_alter_ticket_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='time_edited',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='time_edited',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
