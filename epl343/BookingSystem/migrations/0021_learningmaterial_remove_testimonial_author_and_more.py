# Generated by Django 4.1.3 on 2022-11-22 17:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BookingSystem', '0020_alter_appointment_end_datetime'),
    ]

    operations = [
        migrations.CreateModel(
            name='LearningMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=60)),
                ('Description', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='testimonial',
            name='author',
        ),
        migrations.RemoveField(
            model_name='testimonial',
            name='author_profile_link',
        ),
        migrations.RemoveField(
            model_name='testimonial',
            name='author_profile_pic',
        ),
        migrations.RemoveField(
            model_name='testimonial',
            name='author_school_and_year',
        ),
        migrations.AddField(
            model_name='myuser',
            name='author_profile_link',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='profilePic',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='school',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='yearofStudy',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='testimonial',
            name='user',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='testimonial',
            name='show',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='LearningMaterialReference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LearningMaterial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BookingSystem.learningmaterial')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FilesLearningMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload', models.FileField(upload_to='uploads/')),
                ('LearningMaterialFK', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='BookingSystem.learningmaterial')),
            ],
        ),
    ]
