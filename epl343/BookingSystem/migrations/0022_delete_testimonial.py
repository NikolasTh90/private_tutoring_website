# Generated by Django 4.1.3 on 2022-11-23 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BookingSystem', '0021_learningmaterial_remove_testimonial_author_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Testimonial',
        ),
    ]
