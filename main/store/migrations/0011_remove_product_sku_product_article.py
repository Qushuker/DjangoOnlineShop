# Generated by Django 5.1.4 on 2025-01-03 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_remove_product_article_product_sku'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='sku',
        ),
        migrations.AddField(
            model_name='product',
            name='Article',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
