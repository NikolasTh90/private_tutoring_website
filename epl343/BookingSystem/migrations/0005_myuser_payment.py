# Generated by Django 3.2.14 on 2022-09-20 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookingSystem', '0004_auto_20220920_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='payment',
            field=models.CharField(choices=[('c', 'Cash'), ('paypal', 'Paypal'), ('card', 'Card'), ('rev', 'Revolut')], default='c', max_length=255, verbose_name='pref_payment_method'),
        ),
    ]
