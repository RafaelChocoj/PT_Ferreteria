# Generated by Django 4.1.1 on 2022-09-09 04:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0002_alter_productodniveles_costo_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('numero', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('fecha', models.DateTimeField()),
                ('descripcion', models.CharField(blank=True, max_length=150, null=True)),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario.proveedor')),
            ],
        ),
    ]
