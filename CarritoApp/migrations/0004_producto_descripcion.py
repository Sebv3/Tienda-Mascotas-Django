# Generated by Django 5.0.6 on 2024-09-11 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CarritoApp', '0003_producto_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='descripcion',
            field=models.TextField(blank=True, null=True),
        ),
    ]
