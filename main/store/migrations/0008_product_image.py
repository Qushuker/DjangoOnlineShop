# Generated by Django 5.1.4 on 2024-12-31 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_favoriteitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='products/'),
        ),
    ]
