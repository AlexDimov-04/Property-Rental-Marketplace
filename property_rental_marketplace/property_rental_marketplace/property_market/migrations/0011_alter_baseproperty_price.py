# Generated by Django 4.2.2 on 2023-07-30 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property_market', '0010_alter_baseproperty_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseproperty',
            name='price',
            field=models.PositiveIntegerField(),
        ),
    ]
