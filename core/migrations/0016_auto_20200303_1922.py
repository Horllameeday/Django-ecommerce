# Generated by Django 2.2.6 on 2020-03-03 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_category_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='cat'),
            preserve_default=False,
        ),
    ]
