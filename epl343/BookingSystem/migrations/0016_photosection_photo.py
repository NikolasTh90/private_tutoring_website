# Generated by Django 4.0.6 on 2022-10-15 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BookingSystem', '0015_testimonial_featured'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhotoSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SectionName', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('belongs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BookingSystem.photosection')),
            ],
        ),
    ]
