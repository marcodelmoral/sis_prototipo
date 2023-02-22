# Generated by Django 3.2.16 on 2023-01-21 22:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('geo', '0001_initial'),
        ('embarazadas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalembarazada',
            name='des_edo_res',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='geo.entidad'),
        ),
        migrations.AddField(
            model_name='historicalembarazada',
            name='des_loc_res',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='geo.localidad'),
        ),
        migrations.AddField(
            model_name='historicalembarazada',
            name='des_mpo_res',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='geo.municipio'),
        ),
    ]