# Generated by Django 4.2.2 on 2023-07-30 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property_market', '0009_alter_baseproperty_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseproperty',
            name='price',
            field=models.IntegerField(max_length=50),
        ),
    ]
