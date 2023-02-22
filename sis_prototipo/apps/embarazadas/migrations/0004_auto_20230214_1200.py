# Generated by Django 3.2.16 on 2023-02-14 18:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import sis_prototipo.apps.embarazadas.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('embarazadas', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='embarazada',
            name='nss',
            field=models.CharField(max_length=11, validators=[sis_prototipo.apps.embarazadas.validators.validador_nss]),
        ),
        migrations.AlterField(
            model_name='historicalembarazada',
            name='nss',
            field=models.CharField(max_length=11, validators=[sis_prototipo.apps.embarazadas.validators.validador_nss]),
        ),
        migrations.CreateModel(
            name='ArchivoEmbarazada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('hash', models.CharField(max_length=255)),
                ('archivo', models.FileField(help_text='Archivo en formato xlsx', upload_to='MEDIA', validators=[sis_prototipo.apps.embarazadas.validators.validador_archivo_embarazada])),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]