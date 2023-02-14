from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from django.contrib.gis.db import models


class DivisionGeografica(models.Model):
    geom = models.MultiPolygonField(srid=settings.CRS)
    cve_ent = models.CharField(max_length=2)
    pobtot = models.PositiveIntegerField(
        "Población total",
        null=True,
        blank=True,
    )
    pobmas = models.PositiveIntegerField(
        "Población masculina",
        null=True,
        blank=True,
    )
    pobfem = models.PositiveIntegerField(
        "Población femenina",
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

class Entidad(DivisionGeografica):
    cvegeo = models.CharField(max_length=2, primary_key=True)
    nomgeo = models.CharField(max_length=80)

    def __str__(self):
        return self.nomgeo

    class Meta:
        ordering = ["nomgeo"]


class Municipio(DivisionGeografica):
    geom = models.MultiPolygonField(srid=settings.CRS)
    cvegeo = models.CharField(max_length=5, primary_key=True)
    nomgeo = models.CharField(max_length=80)
    cve_ent = models.CharField(max_length=2)
    cve_mun = models.CharField(max_length=3)
    entidad = models.ForeignKey(Entidad, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nomgeo

    class Meta:
        ordering = ["nomgeo"]


class Localidad(DivisionGeografica):
    PLANO_TIPO = ((0, "No"), (1, "Si"), (2, "Croquis"))
    AMBITO_TIPO = ((0, "No Aplica"), (1, "Urbana"), (2, "Rural"))
    cvegeo = models.CharField(max_length=9, primary_key=True)
    nomgeo = models.CharField(max_length=120)
    cve_ent = models.CharField(max_length=2)
    cve_mun = models.CharField(max_length=3)
    cve_loc = models.CharField(max_length=4)
    ambito = models.PositiveSmallIntegerField(choices=AMBITO_TIPO, null=True)
    plano = models.PositiveSmallIntegerField(choices=PLANO_TIPO, null=True)
    puntual = models.BooleanField(default=False)
    municipio = models.ForeignKey(
        Municipio, on_delete=models.SET_NULL, null=True
    )
    def __str__(self):
        return self.nomgeo

    class Meta:
        ordering = ["nomgeo"]


class Manzana(DivisionGeografica):
    # Definicion de elementos para campo de eleccion
    AMBITO_TIPO = ((0, "No Aplica"), (1, "Urbana"), (2, "Rural"))
    MANZANA_TIPO = (
        (0, "No Aplica"),
        (1, "Típica"),
        (2, "Atípica"),
        (3, "Contenedora"),
        (4, "Contenida"),
        (5, "Económica"),
        (6, "Edificio-Manzana"),
        (7, "Glorieta"),
        (8, "Parque o Jardín"),
        (9, "Camellón"),
        (10, "Bajo Puente"),
    )

    cvegeo = models.CharField(max_length=16, primary_key=True)
    cve_ent = models.CharField(max_length=2)
    cve_mun = models.CharField(max_length=3)
    cve_loc = models.CharField(max_length=4)
    cve_ageb = models.CharField(max_length=4)
    cve_mza = models.CharField(max_length=3)
    ambito = models.PositiveSmallIntegerField(choices=AMBITO_TIPO)
    tipomza = models.PositiveSmallIntegerField(choices=MANZANA_TIPO)
    localidad = models.ForeignKey(
        Localidad, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.cvegeo
