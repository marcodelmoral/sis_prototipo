# Generated by Django 3.2.5 on 2021-10-30 06:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('geo', '0004_auto_20211029_0249'),
        ]

    operations = [
        migrations.RemoveField(
            model_name='ageb',
            name='id',
            ),
        migrations.RemoveField(
            model_name='entidad',
            name='id',
            ),
        migrations.RemoveField(
            model_name='localidad',
            name='id',
            ),
        migrations.RemoveField(
            model_name='manzana',
            name='id',
            ),
        migrations.RemoveField(
            model_name='municipio',
            name='id',
            ),
        migrations.AlterField(
            model_name='ageb',
            name='cvegeo',
            field=models.CharField(max_length=13, primary_key=True, serialize=False),
            ),
        migrations.AlterField(
            model_name='entidad',
            name='cvegeo',
            field=models.CharField(max_length=2, primary_key=True, serialize=False),
            ),
        migrations.AlterField(
            model_name='localidad',
            name='cvegeo',
            field=models.CharField(max_length=17, primary_key=True, serialize=False),
            ),
        migrations.AlterField(
            model_name='manzana',
            name='cvegeo',
            field=models.CharField(max_length=16, primary_key=True, serialize=False),
            ),
        migrations.AlterField(
            model_name='municipio',
            name='cvegeo',
            field=models.CharField(max_length=5, primary_key=True, serialize=False),
            ),
        ]
