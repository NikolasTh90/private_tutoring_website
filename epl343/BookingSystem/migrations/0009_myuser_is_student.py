# Generated by Django 3.2.14 on 2022-09-23 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookingSystem', '0008_rename_payment_myuser_pay'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='is_student',
            field=models.BooleanField(default=False, verbose_name='is_student'),
        ),
    ]
