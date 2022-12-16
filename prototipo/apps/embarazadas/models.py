from datetime import date

from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.measure import Distance
from django.core.serializers import serialize
from django.urls import reverse
from simple_history.models import HistoricalRecords

from prototipo.apps.embarazadas.managers import EmbarazadaManager
from prototipo.apps.embarazadas.validators import validador_nss
from prototipo.apps.geo.models import Entidad, Municipio, Localidad
from prototipo.apps.vectores.models import Vector


class Embarazada(models.Model):
    # todo checar las caracteristicas de los campos de embarazada
    # para saber que tipo son etc
    ESCOLARIDAD = (
        ('Ninguna', 'Ninguna'),
        ('Preescolar', 'Preescolar'),
        ('Primaria', 'Primaria'),
        ('Secundaria', 'Secundaria'),
        ('Bachillerato', 'Bachillerato'),
        ('Licenciatura', 'Licenciatura'),
        ('Posgrado', 'Posgrado')
    )

    TURNO = (
        ('Matutino', 'Matutino'),
        ('Vespertino', 'Verpertino')
    )

    creado = models.DateTimeField(auto_now_add=True)  # fecha de primera atencion?

    # Ficha de identificacion
    precision = models.BooleanField(default=False)
    # UMF = models.ForeignKey(Umf, on_delete=models.SET_NULL, null=True)
    folio = models.PositiveIntegerField(blank=True, null=True)
    consultorio = models.CharField(max_length=255, blank=True, null=True)  # Puede que haya consultorios A, B, C ...
    turno = models.CharField(choices=TURNO, blank=True, null=True, max_length=15)
    nss = models.CharField(max_length=11, validators=[validador_nss])  # Se valida en el form
    # Se le quitó el Unique porque entraba en conflicto con una función de la API
    ide_nom = models.CharField(max_length=255, blank=True, null=True)
    ide_ape_pat = models.CharField(max_length=255, null=True, blank=True)
    ide_ape_mat = models.CharField(max_length=255, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    num_ext = models.CharField(max_length=255, null=True, blank=True)
    num_int = models.CharField(max_length=255, null=True, blank=True)
    ide_cal = models.CharField(max_length=255, null=True, blank=True)
    ide_calle1 = models.CharField(max_length=255, blank=True, null=True)
    ide_calle2 = models.CharField(max_length=255, blank=True, null=True)
    ide_cp = models.CharField(max_length=5, null=True, blank=True)
    ide_col = models.CharField(max_length=255, blank=True, null=True)
    des_edo_res = models.ForeignKey(Entidad, on_delete=models.SET_NULL, null=True, blank=True)
    des_mpo_res = models.ForeignKey(Municipio, on_delete=models.SET_NULL, null=True, blank=True)
    des_loc_res = models.ForeignKey(Localidad, on_delete=models.SET_NULL, null=True, blank=True)
    geom = models.PointField(srid=settings.CRS, null=True, default=None, blank=True)
    peso = models.FloatField(blank=True, null=True, default=0, help_text='En kilogramos')
    estatura = models.FloatField(blank=True, null=True, default=0, help_text='En centímetros')
    # crear una metrica para determinar el numero de gestas vs el numero de paras
    escolaridad = models.CharField(choices=ESCOLARIDAD, null=True, blank=True, max_length=20)
    gestas = models.PositiveSmallIntegerField(blank=True, null=True)
    paras = models.CharField(max_length=255, blank=True, null=True)  # ??
    abortos = models.PositiveSmallIntegerField(blank=True, null=True)
    cesareas = models.PositiveSmallIntegerField(blank=True, null=True)
    # edad, imc y sdg son properties
    fecha_menstruacion = models.DateField(null=True, blank=True)
    fecha_parto = models.DateField(null=True, blank=True)  # +365 dias para salir del sistema / Fecha probable
    probable_parto = models.BooleanField(default=False)
    avisados = models.BooleanField(default=False)

    fecha_primera = models.DateField(null=True, blank=True)
    fecha_trabajo_social = models.DateField(null=True, blank=True)
    fecha_ult_cita = models.DateField(null=True, blank=True)
    fecha_prox_cita = models.DateField(null=True, blank=True)
    fecha_envio_mf = models.DateField(null=True, blank=True)  # materno fetal
    fecha_envio_mi = models.DateField(null=True, blank=True)  # materno infantil
    fecha_envio_cph = models.DateField(null=True, blank=True)  # que es cph?
    fecha_envio_gineco = models.DateField(null=True, blank=True)
    fecha_envio_re = models.DateField(null=True, blank=True)  # resolucion de embarazo
    fecha_envio_pr = models.DateField(null=True, blank=True)  # pulsera rosa

    # Antecedentes ginecologicos y obstetricos
    antecedente_cu = models.CharField(max_length=255, blank=True, null=True)  # cirugia uterina
    antecedente_p = models.CharField(max_length=255, blank=True, null=True)  # perinatales
    periodo_inter = models.CharField(max_length=255, blank=True, null=True)  # intergenesico
    primer_embarazo_masdecuatro = models.CharField(max_length=255, blank=True, null=True)  # es pregunta, dropdown?
    antecedente_a = models.BooleanField(default=False)  # dos o mas abortos espontaneos
    antecedente_c = models.BooleanField(default=False)  # antecedente de cesaria bool?
    preeclampsia = models.BooleanField(default=False)  # quizas es bool
    eclampsia = models.BooleanField(default=False)  # quizas es bool
    obito_fetal = models.BooleanField(default=False)  # quizas es bool
    bajo_peso = models.BooleanField(default=False)  # quizas poner el peso
    prematurez = models.BooleanField(default=False)  # quizas es bool
    macrosomia = models.BooleanField(default=False)  # quizas es bool que es?
    malformacion = models.BooleanField(default=False)  # quizas es bool
    sangrado_tercer_trimestre = models.BooleanField(default=False)  # quizas es bool
    polihidramnios = models.BooleanField(default=False)  # quizas es bool que es?
    ectopico = models.BooleanField(default=False)  # quizas es bool
    enfermedad_tg = models.BooleanField(default=False)  # trofoblastica gestacional
    # vector = models.ManyToManyField(Vector, blank=True)
    peligro = models.BooleanField(default=False)
    # numero_cercanos es property

    # Antecedentes personales patologicos
    zika = models.BooleanField(default=False)
    hipertension = models.BooleanField(default=False)  # a lo mejor añadir valores y brazo
    diabetes = models.BooleanField(default=False)  # quizas es bool
    cardiopatia = models.CharField(max_length=255, blank=True, null=True)  # congenita - adquirida - na?
    tiroidopatias = models.CharField(max_length=255, blank=True, null=True)
    autoinmune = models.CharField(max_length=255, blank=True, null=True)  # o de la colagena
    # lupus eritematoso sistemico, artritis reumatoide dropdown ?
    tromboembolica = models.CharField(max_length=255, blank=True, null=True)  # quizas es bool
    accidente_vascular_cerebral = models.CharField(max_length=255, blank=True, null=True)  # quizas es bool
    neumopatias = models.CharField(max_length=255, blank=True, null=True)  # quizas es bool asma bronquial
    tuberculosis = models.CharField(max_length=255, blank=True, null=True)  # quizas es bool
    hepatopatias = models.CharField(max_length=255, blank=True, null=True)  # tumores benignos, malignos, hepatitis
    # cirrosis
    cancer_mama = models.BooleanField(default=False)  # quizas es bool
    cancer_cervico = models.BooleanField(default=False)  # quizas es bool
    cancer_otros = models.CharField(max_length=255, blank=True, null=True)  # quizas es bool
    nefropatias = models.CharField(max_length=255, blank=True, null=True)  # quizas es bool
    epilepsia = models.BooleanField(default=False)  # quizas es bool
    neuropatia = models.CharField(max_length=255, blank=True, null=True)  # quizas es bool
    hematologicas = models.CharField(max_length=255, blank=True, null=True)  # anemia de celula calciformes
    # linfoma, leucemia, purpura trombocitopénica
    enfermedad_isquemica = models.CharField(max_length=255, blank=True, null=True)  # quizas es bool
    discapacidad = models.CharField(max_length=255, blank=True, null=True)  # quizas es bool quizas dropdown y descrip
    # mental - fisica - na
    seropositivo = models.BooleanField(default=False)  # quizas es bool
    alcoholismo = models.BooleanField(default=False)  # quizas es bool
    tabaquismo = models.BooleanField(default=False)  # quizas es bool
    drogadiccion = models.BooleanField(default=False)  # quizas es bool
    adicciones = models.CharField(max_length=255, blank=True, null=True)  # quizas es bool quizas poner cuales o drop

    # PREVENIMSS
    fecha_envio_vi = models.DateField(null=True, blank=True)  # vacula de influenza
    fecha_envio_tpda = models.DateField(null=True, blank=True)  # vacula de TPDA
    fecha_envio_pvih = models.DateField(null=True, blank=True)  # primera
    fecha_envio_svih = models.DateField(null=True, blank=True)  # segunda
    vih_reactivo = models.BooleanField(default=False)  # fue reactiva a una prueba de vih creo que es redundante?
    ivu = models.CharField(max_length=255, blank=True, null=True)  # que sera esto?
    ir = models.CharField(max_length=255, blank=True, null=True)  # chale

    activo = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True, null=True)
    objects = EmbarazadaManager.as_manager()
    history = HistoricalRecords()

    # content = models.TextField(blank=True, null=True)

    @property
    def contenido(self):
        return f'<p><strong>NSS: </strong><a href= {self.get_absolute_url()} target="_blank"> {self.nss} </a></p><p><strong>Nombre: </strong> {self.nombre_completo} </p><p><strong>Dirección: </strong> {self.obtener_direccion} </p><p><strong>Fecha de última menstruación:</strong> {self.FECHA_MENSTRUACION} </p><p><strong>Fecha probable de parto:</strong> {self.FECHA_PARTO} </p><p><strong>Semanas de gestación:</strong> {self.sdg} </p><p><strong>En peligro:</strong> {self.peligra} </p>'

    # @property
    # def dependencia(self):
    #     try:
    #         if self.UMF.delegacion.nombre and self.UMF.nombre:
    #             return f'Delegación: {self.UMF.delegacion.nombre} - UMF: {self.UMF.nombre}'
    #     except:
    #         return None

    @property
    def peligra(self):
        return self.peligro

    @property
    def edad(self):
        try:
            today = date.today()
            edad = today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month,
                                                                                          self.fecha_nacimiento.day))
            return edad
        except:
            return None

    @property
    def imc(self):
        try:
            return self.peso // (self.estatura / 100) ** 2
        except ZeroDivisionError:
            return 0

    @property
    def coords(self):
        try:
            x, y = self.geometry.x, self.geometry.y
            return x, y
        except:
            return None

    @property
    def obtener_direccion(self):
        return f'{self.num_ext} {self.ide_cal}, {self.des_mpo_res} {self.des_edo_res}, {self.ide_cp}'

    def __str__(self):
        return f'{self.nss} - {self.ide_nom} - En peligro: {self.peligro}'

    @property
    def sdg(self):
        try:
            fecha = self.fecha_menstruacion
            delta = date.today()
            return (delta - fecha).days // 7
        except:
            return None

    @property
    def numero_cercanos(self):
        return self.vector.activos().count()

    @property
    def coordenadas_vectores(self):
        vec = []
        for ele in self.vector.all():
            vec.append(ele.coords)
        return vec

    @property
    def geojson_embarazada(self):
        return serialize('geojson', [self], geometry_field='geo')

    @property
    def geojson_cercanos(self):
        return serialize('geojson', self.vector.all(), geometry_field='geo')

    @property
    def nombre_completo(self):
        return f'{self.ide_nom} {self.ide_ape_pat} {self.ide_ape_mat}'

    # def geocodifica(self):
    #     comps = f'country:MX|locality:{self.des_mpo_res.nomgeo}|postal_code{self.ide_cp}'
    #     g = geo(location=self.obtener_direccion,
    #             key=settings.APIKEY_GEO,
    #             components=comps,
    #             language='es')
    #     if g.ok:
    #         self.geo = Point(float(g.lng),
    #                          float(g.lat),
    #                          srid=4326)
    #         self.precision = True
    #         self.save()
    #
    # def retrocodifica(self):
    #
    #     direccion = geo([self.geo.y, self.geo.x],
    #                     method='reverse',
    #                     key=settings.APIKEY_GEO)
    #     if direccion.ok:
    #         self.NUM_EXT = direccion.housenumber
    #         self.IDE_CAL = direccion.street
    #         self.DES_EDO_RES = Entidad.objects.get(nomgeo__icontains=direccion.province_long)
    #         self.DES_MPO_RES = self.DES_EDO_RES.municipio_set.get(nomgeo__icontains=direccion.city_long)
    #         self.IDE_CP = direccion.postal
    #         self.PRECISION = True
    #         self.save()

    def vector_cercano(self):
        if self.PRECISION:
            qs = Vector.objects.activos().precisos().filter(
                geo__distance_lt=(self.geometry, Distance(km=settings.DISTANCIA)))

            if qs.exists():
                qs.update(peligro=True)
                self.vector.add(*qs)
                self.peligro = True
                # numeros = self.UMF.user_set(tipo_usuario=4).values('numero')
                # for numero in numeros:
                #     send_sms(to='+52{}'.format(numero), message='Existe riesgo de vectores')
                self.save()

    # def correo(self):
    #     # tipo 4 = jefe de ginecologia
    #     correos = self.UMF.user_set(tipo=4).values('email')
    #     asunto = 'Embarazada parto'
    #     cuerpo = 'Embarazada proxima a parto'
    #     emailfrom = settings.EMAIL_HOST
    #     send_mail(asunto, cuerpo, emailfrom, correos)
    #     self.AVISADOS = True
    #     self.save()

    # def save(self, *args, **kwargs):
    #     created = self.pk is None
    #     super(Embarazada, self).save(*args, **kwargs)
    #     if created:
    #         if self.geo:
    #             self.retrocodifica()
    #         else:
    #             self.geocodifica()
    #         self.vector_cercano()

    def get_absolute_url(self):
        return reverse('geo:embarazadas', kwargs={'NSS': self.nss})
