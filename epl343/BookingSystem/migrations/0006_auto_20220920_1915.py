# Generated by Django 3.2.14 on 2022-09-20 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookingSystem', '0005_myuser_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='payment',
        ),
        migrations.AddField(
            model_name='myuser',
            name='pay',
            field=models.CharField(choices=[('one', '1'), ('two', '2'), ('three', '3'), ('four', '4'), ('five', '5'), ('six', '6'), ('six_p', '6+'), ('OT', 'Other')], default='one', max_length=255, verbose_name='pay'),
        ),
    ]
