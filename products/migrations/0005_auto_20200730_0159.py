# Generated by Django 2.2.10 on 2020-07-29 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='abc'),
        ),
    ]
