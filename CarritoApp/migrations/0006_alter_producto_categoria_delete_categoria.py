# Generated by Django 5.0.6 on 2024-09-13 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CarritoApp', '0005_categoria_alter_producto_categoria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='categoria',
            field=models.CharField(max_length=50),
        ),
        migrations.DeleteModel(
            name='Categoria',
        ),
    ]