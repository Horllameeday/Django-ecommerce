# Generated by Django 2.2.4 on 2019-09-02 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.CharField(max_length=400, null=True),
        ),
    ]
