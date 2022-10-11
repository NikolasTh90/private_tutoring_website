# Generated by Django 4.1.1 on 2022-10-10 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookingSystem', '0013_teaching_experience_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teaching_experience',
            old_name='date',
            new_name='start_date',
        ),
        migrations.AddField(
            model_name='teaching_experience',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
