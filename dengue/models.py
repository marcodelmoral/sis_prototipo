from django.contrib.gis.db import models

from geo.models import Entidad, Localidad, Manzana, Municipio


class Vector(models.Model):
    SEXO = ((1, "Masculino"), (2, "Femenino"))

    DIAGNOSTICO = (
        (1, "Dengue no grave"),
        # (10, "DENGUE CON SIGNOS DE ALARMA - ENFERMEDAD POR VIRUS ZIKA"),
        (3, "Dengue grave"),
        # (8, "ENFERMEDAD POR VIRUS ZIKA"),
        # (6, "DENGUE CON SIGNOS DE ALARMA - FIEBRE CHIKUNGUNYA"),
        (2, "Dengue con signos de alarma"),
        # (5, "DENGUE NO GRAVE - FIEBRE CHIKUNGUNYA"),
        )
    fol_id = models.CharField(max_length=255, blank=True, null=True)
    # creado = models.DateTimeField(auto_now_add=True)
    ide_nom = models.CharField(max_length=255, blank=True, null=True)
    ide_ape_pat = models.CharField(max_length=255, blank=True, null=True)
    ide_ape_mat = models.CharField(max_length=255, blank=True, null=True)
    ide_sex = models.PositiveSmallIntegerField(choices=SEXO, null=True, blank=True)
    num_ext = models.CharField(max_length=255)
    num_int = models.CharField(max_length=255, blank=True, null=True)
    ide_cal = models.CharField(max_length=255)
    # localidad = models.ForeignKey(Localidad, on_delete=models.SET_NULL, null=True)
    municipio = models.ForeignKey(Municipio, on_delete=models.SET_NULL, null=True)
    ide_fec_nac = models.DateField(null=True, blank=True)
    ide_cp = models.CharField(max_length=5)
    ide_col = models.CharField(max_length=255, blank=True, null=True)
    # cve_diag_final = models.PositiveSmallIntegerField(choices=DIAGNOSTICO, blank=True, null=True)
    # precision = models.BooleanField(default=False)  # si/no
    # des_diag_final = models.CharField(null=True, blank=True, max_length=255)
    cve_diag_final = models.PositiveSmallIntegerField(choices=DIAGNOSTICO, null=True)
    des_ocupacion = models.CharField(null=True, blank=True, max_length=255)
    geometry = models.PointField(srid=4326, null=True, default=None, blank=True)
    fec_sol_aten = models.DateField(null=True, blank=True)

    # ACTIVO = models.BooleanField(default=True)
    # objects = VectorManager.as_manager()
    #  PELIGRO = models.BooleanField(default=False)

    # @property
    # def coords(self):
    #     try:
    #         x, y = self.LOC.x, self.LOC.y
    #         return x, y
    #     except:
    #         return None, None
    #
    # @property
    # def obtener_direccion(self):
    #     return f"{self.NUM_EXT} {self.IDE_CAL}, {self.DES_MPO_RES} {self.DES_EDO_RES}, {self.IDE_CP}"
    #
    # @property
    # def nombre_completo(self):
    #     return f"{self.IDE_NOM} {self.IDE_APE_PAT} {self.IDE_APE_MAT}"
    #
    # def __str__(self):
    #     return f"{self.nombre_completo} {self.obtener_direccion}"
    #
    # def geocodifica(self):
    #     comps = (
    #         f"country:MX|locality:{self.DES_MPO_RES.nomgeo}|postal_code{self.IDE_CP}"
    #     )
    #     g = geo(
    #         location=self.obtener_direccion,
    #         key=settings.APIKEY_GEO,
    #         components=comps,
    #         language="es",
    #     )
    #     if g.ok:
    #         self.LOC = Point(float(g.lng), float(g.lat), srid=4326)
    #         self.PRECISION = True
    #         self.save()
    #
    # def retrocodifica(self):
    #
    #     direccion = geo(
    #         [self.LOC.y, self.LOC.x], method="reverse", key=settings.APIKEY_GEO
    #     )[0]
    #     if direccion.ok:
    #         self.NUM_INT = direccion.housenumber
    #         self.IDE_CAL = direccion.street
    #         self.DES_EDO_RES = Entidad.objects.get(
    #             nomgeo__icontains=direccion.province_long
    #         )
    #         self.DES_MPO_RES = self.DES_EDO_RES.municipio_set.get(
    #             nomgeo__icontains=direccion.city_long
    #         )
    #         self.IDE_CP = direccion.postal
    #         self.save()
    #
    # @property
    # def geojson_vector(self):
    #     return serialize("geojson", [self], geometry_field="LOC")

    def save(self, *args, **kwargs):
        created = self.pk is None
        super(Vector, self).save(*args, **kwargs)
        if created:
            if self.LOC:
                self.retrocodifica()
            else:
                self.geocodifica()
            self.embarazada_cercana()

    # def get_absolute_url(self):
    #     return reverse('geo:vectores', kwargs={'pk': self.pk})


class DatosAgregados(models.Model):
    TIPO_DATO = (
        (1, 'Número de casos'),
        (2, 'Temperatura mínima'),
        (3, 'Temperatura máxima'),
        (4, 'Temperatura promedio'),
        (5, 'Precipitación'),
        )

    entidad = models.ForeignKey(Entidad, on_delete=models.DO_NOTHING)
    fecha = models.DateField()
    tipo = models.PositiveSmallIntegerField(choices=TIPO_DATO)
    valor = models.FloatField()
