# Generated by Django 5.1.4 on 2025-01-03 22:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_alter_product_article'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='Article',
        ),
    ]
