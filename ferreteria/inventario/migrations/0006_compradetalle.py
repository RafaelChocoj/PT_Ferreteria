# Generated by Django 4.1.1 on 2022-09-09 07:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0005_alter_productodniveles_unique_together_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompraDetalle',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('unidades', models.DecimalField(decimal_places=2, max_digits=9)),
                ('costo', models.DecimalField(decimal_places=2, max_digits=9, null=True)),
                ('compra', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario.compra')),
                ('productodetalle', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventario.productodniveles')),
            ],
        ),
    ]
