# Generated by Django 2.0.3 on 2018-04-16 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lens', '0010_auto_20180416_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='axe',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]