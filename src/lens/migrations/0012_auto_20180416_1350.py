# Generated by Django 2.0.3 on 2018-04-16 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lens', '0011_auto_20180416_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='axe',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
    ]
