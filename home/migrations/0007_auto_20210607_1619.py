# Generated by Django 3.2.4 on 2021-06-07 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_rename_discountedprice_item_discounted_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image2',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='image3',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='image4',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='image5',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='image6',
            field=models.TextField(blank=True),
        ),
    ]
