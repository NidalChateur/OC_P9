# Generated by Django 4.2.3 on 2023-08-02 05:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_review_star_review_time_edited_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='second_review',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='review.review'),
        ),
    ]
