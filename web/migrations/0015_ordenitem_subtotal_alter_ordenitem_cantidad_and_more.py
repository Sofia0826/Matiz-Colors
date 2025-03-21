# Generated by Django 5.1.6 on 2025-03-03 15:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0014_remove_ordenitem_precio_alter_ordenitem_cantidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordenitem',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='ordenitem',
            name='cantidad',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='ordenitem',
            name='orden',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.orden'),
        ),
    ]
