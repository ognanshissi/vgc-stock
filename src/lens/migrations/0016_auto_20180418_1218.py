# Generated by Django 2.0.3 on 2018-04-18 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lens', '0015_product_in_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='cylindre',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='sphere',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]
