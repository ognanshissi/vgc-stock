# Generated by Django 2.0.3 on 2018-04-16 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lens', '0007_auto_20180415_2344'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Axe',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='product',
            name='cylindre',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='product',
            name='type',
            field=models.CharField(choices=[('SF + PH + AR', 'Simple Foyer Photogray Anti-Reflet'), ('DFB', 'Double Foyer Blanc'), ('DF', 'Double Foyer'), ('DF + PH + AR', 'Double Foyer Photogray Anti-Reflet'), ('PB', 'Progressif Blanc'), ('P + PH + AR', 'Progressif Photogray Anti-Reflet')], max_length=25),
        ),
    ]
