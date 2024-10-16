# Generated by Django 5.1.2 on 2024-10-17 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StayfinderApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='hotel_banner',
            field=models.FileField(blank=True, default='no_image/noimage.png', null=True, upload_to='hotel_iamge'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='interior_image',
            field=models.FileField(blank=True, default='no_image/noimage.png', null=True, upload_to='hotel_iamge'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='latitude',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='longitude',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
