# Generated by Django 2.0.3 on 2018-04-16 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lens', '0009_auto_20180416_1317'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='Axe',
            new_name='axe',
        ),
        migrations.AlterField(
            model_name='product',
            name='addition',
            field=models.PositiveSmallIntegerField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='sphere',
            field=models.FloatField(default=0.0),
        ),
    ]