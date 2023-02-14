from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form, CharField, ChoiceField, RadioSelect, \
    ModelChoiceField, IntegerField, HiddenInput, TextInput, ModelMultipleChoiceField, BooleanField, FloatField
from django.contrib.gis.forms.fields import PointField

from sis_prototipo.apps.embarazadas.models import Embarazada, ArchivoEmbarazada
from sis_prototipo.apps.embarazadas.validators import validador_nss
from sis_prototipo.apps.geo.models import Entidad, Municipio, Localidad
from django.contrib.auth.forms import UserCreationForm
from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget
from leaflet.forms.widgets import LeafletWidget
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab, Alert, InlineCheckboxes, Accordion, \
    AccordionGroup
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset


class EmbarazadaForm(ModelForm):

    DES_EDO_RES = ModelChoiceField(
        queryset=Entidad.objects.all(), required=False,
        label="Entidad",
        widget=ModelSelect2Widget(
            model=Entidad,
            search_fields=['nomgeo__icontains'],
        )
    )
    DES_MPO_RES = ModelChoiceField(
        queryset=Municipio.objects.all(), required=False,
        label="Municipio",
        widget=ModelSelect2Widget(
            model=Municipio,
            search_fields=['nomgeo__icontains'],
            dependent_fields={'DES_EDO_RES': 'entidad'},
        )
    )

    DES_LOC_RES = ModelChoiceField(
        queryset=Localidad.objects.all(), required=False,
        label="Localidad",
        widget=ModelSelect2Widget(
            model=Localidad,
            search_fields=['nomloc__icontains'],
            dependent_fields={'DES_MPO_RES': 'municipio'},
        )
    )

    class Meta:
        model = Embarazada

        labels = {
            'IDE_NOM': 'Nombre',
            'IDE_APE_PAT': 'Apellido paterno',
            'IDE_APE_MAT': 'Apellido materno',
            'FECHA_NACIMIENTO': 'Fecha de nacimiento',
            'NUM_EXT': 'Número exterior',
            'NUM_INT': 'Número interior',
            'IDE_CAL': 'Calle',
            'IDE_CALLE1': 'Entre calle',
            'IDE_CALLE2': 'y calle',
            'IDE_COL': 'Colonia',
            'IDE_CP': 'Código postal',
            'LOC': 'Punto geográfico',
            'peso': 'Peso (en Kg)',
            'estatura': 'Estatura (en cm)',
            'escolaridad': 'Escolaridad máxima',
            'gestas': 'Número de gestaciones previas',
            'paras': 'Número de paras',
            'abortos': 'Número de abortos',
            'cesareas': 'Número de cesáreas',
            'FECHA_PARTO': 'Fecha probable de parto',
            'FECHA_MENSTRUACION': 'Fecha de última menstruación',
            'FECHA_PRIMERA': 'Fecha de primera atención',
            'FECHA_TRABAJO_SOCIAL': 'Fecha de cita con Trabajo Social',
            'FECHA_ULT_CITA': 'Fecha de la última cita',
            'FECHA_PROX_CITA': 'Fecha de la próxima cita',
            'FECHA_ENVIO_MF': 'Fecha de envío a Materno Fetal',
            'FECHA_ENVIO_MI': 'Fecha de envío a Materno Infantil',
            'FECHA_ENVIO_CPH': 'Fecha de envío a CPH',
            'FECHA_ENVIO_GINECO': 'Fecha de envío a Ginecología',
            'FECHA_ENVIO_RE': 'Fecha de envío a Resolución de Embarazo',
            'FECHA_ENVIO_PR': 'Fecha de envío de Pulsera Rosa',
            'antecedente_cu': 'Antecedente de Cirugía Uterina',
            'antecedente_p': 'Antecedente de Perinatales',
            'periodo_inter': 'Periodo intergenésico',
            'primer_embarazo_masdecuatro': '¿Primer embarazo o más de cuatro?',
            'antecedente_a': 'Antecedente de dos o más abortos espontáneos',
            'antecedente_c': 'Antecedente de cesárea',
            'preeclampsia': 'Preeclampsia',
            'eclampsia': 'Eclampsia',
            'obito_fetal': 'Óbito fetal',
            'bajo_peso': 'Bajo peso',
            'prematurez': 'Prematurez',
            'macrosomia': 'Macrosomía',
            'malformacion': 'Malformación',
            'sangrado_tercer_trimestre': 'Sangrado en tercer trimestre',
            'polihidramnios': 'Polihidramnios',
            'ectopico': 'Ectópico',
            'enfermedad_tg': 'Enfermedad trofoblástica gestacional',
            'ZIKA': 'Zika',
            'hipertension': 'Hipertensión',
            'diabetes': 'Diabetes',
            'cardiopatia': 'Cardiopatía',
            'tiroidopatias': 'Tiroidopatías',
            'autoinmune': 'Enfermedades autoinmunes',
            'tromboembolica': 'Tromboembólica',
            'accidente_vascular_cerebral': 'Accidente vascular cerebral',
            'neumopatias': 'Neumopatías',
            'tuberculosis': 'Tuberculosis',
            'hepatopatias': 'Hepatopatías',
            'cancer_mama': 'Cáncer de mama',
            'cancer_cervico': 'Cáncer cérvico-uterino',
            'cancer_otros': 'Otros tipos de cáncer',
            'nefropatias': 'Nefropatías',
            'hematologicas': 'Enfermedades hematológicas',
            'enfermedad_isquemica': 'Enfermedad isquémica',
            'discapacidad': 'Discapacidad',
            'seropositivo': 'Seropositivo',
            'alcoholismo': 'Alcoholismo',
            'tabaquismo': 'Tabaquismo',
            'drogadiccion': 'Drogadicción',
            'adicciones': 'Otras adicciones',
            'FECHA_ENVIO_VI': 'Fecha de envío a Vácula de Influenza',
            'FECHA_ENVIO_TPDA': 'Fecha de envío a Vácula de TPDA',
            'FECHA_ENVIO_PVIH': 'Fecha de envío a primera prueba de VIH',
            'FECHA_ENVIO_SVIH': 'Fecha de envío a segunda prueba de VIH',
            'vih_reactivo': 'Reactivo a VIH',
            'IVU': 'Infección en las vías urinarias',
            'IR': 'Infección respiratoria',
            'OBSERVACIONES': 'Observaciones'
        }

        exclude = ('CREADO', 'COORDS', 'ACTIVO', 'AVISADOS',
                   'UMF', 'OBSERVACIONES', 'PELIGRO', 'PRECISION', 'VECTOR', 'PROBABLE_PARTO')

        widgets = {
            'FECHA_NACIMIENTO': TextInput(
                attrs={'type': 'date'}
            ),
            'FECHA_PARTO':   TextInput(
                attrs={'type': 'date'}
            ),
            'FECHA_MENSTRUACION':  TextInput(
                attrs={'type': 'date'}
            ),
            'FECHA_PRIMERA':  TextInput(
                attrs={'type': 'date'}
            ),
            'FECHA_TRABAJO_SOCIAL':  TextInput(
                attrs={'type': 'date'}
            ),
            'FECHA_ULT_CITA':  TextInput(
                attrs={'type': 'date'}
            ),
            'FECHA_PROX_CITA':  TextInput(
                attrs={'type': 'date'}
            ),
            'FECHA_ENVIO_MF':  TextInput(
                attrs={'type': 'date'}
            ),
            'FECHA_ENVIO_MI':  TextInput(
                attrs={'type': 'date'}
            ),
            'FECHA_ENVIO_CPH':  TextInput(
                attrs={'type': 'date'}
            ),
            'FECHA_ENVIO_GINECO':  TextInput(
                attrs={'type': 'date'}
            ),
            'FECHA_ENVIO_RE':  TextInput(
                attrs={'type': 'date'}
            ),
            'FECHA_ENVIO_PR':  TextInput(
                attrs={'type': 'date'}
            ),
            'FECHA_ENVIO_VI':  TextInput(
                attrs={'type': 'date'}
            ),
            'FECHA_ENVIO_TPDA':  TextInput(
                attrs={'type': 'date'}
            ),
            'FECHA_ENVIO_PVIH':  TextInput(
                attrs={'type': 'date'}
            ),
            'FECHA_ENVIO_SVIH':  TextInput(
                attrs={'type': 'date'}
            ),
            'LOC': LeafletWidget()
        }

    def __init__(self, *args, **kwargs):
        super(EmbarazadaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Guardar', css_class='btn-success'))
        self.helper.form_class = 'form-horizontal'
        self.helper.help_text_inline = True
        self.helper.layout = Layout(
            Fieldset(
                'Datos generales',
                Field('IDE_NOM'),
                Field('IDE_APE_PAT'),
                Field('IDE_APE_MAT'),
                Field('FECHA_NACIMIENTO')
            ),
            Fieldset(
                'Ficha médica',
                Field('NSS'),
                Field('folio'),
                Field('consultorio'),
                Field('turno')
            ),
            Fieldset(
                'Datos escolares y físicos',
                Field('peso'),
                Field('estatura'),
                Field('escolaridad'),
            ),
            Fieldset(
                'Información geográfica',
                Alert(content='<strong>Atención: </strong> Poner dirección o punto geográfico, no los dos',
                      css_class="alert alert-warning"),
                TabHolder(
                    Tab(
                        'Geoposición',
                        'LOC',
                    ),
                    Tab(
                        'Direccion',
                        'NUM_EXT',
                        'NUM_INT',
                        'IDE_CAL',
                        'IDE_CALLE1',
                        'IDE_CALLE2',
                        'IDE_CP',
                        'IDE_COL',
                        'DES_EDO_RES',
                        'DES_MPO_RES',
                        'DES_LOC_RES',
                    )
                )
            ),
            Fieldset(
                'Información obstétrica y control',
                TabHolder(
                    Tab(
                        'Información obstétrica',
                        'gestas',
                        'paras',
                        'abortos',
                        'cesareas',
                        'FECHA_MENSTRUACION',
                        'FECHA_PARTO',
                        active=True
                    ),
                    Tab(
                        'Control de embarazadas',
                        'FECHA_PRIMERA',
                        'FECHA_TRABAJO_SOCIAL',
                        'FECHA_ULT_CITA',
                        'FECHA_PROX_CITA',
                        'FECHA_ENVIO_MF',
                        'FECHA_ENVIO_MI',
                        'FECHA_ENVIO_CPH',
                        'FECHA_ENVIO_GINECO',
                        'FECHA_ENVIO_RE',
                        'FECHA_ENVIO_PR'
                    )
                )

            ),
            Accordion(
                AccordionGroup('Antecedentes ginecológicos y obstétricos',
                               Field('antecedente_cu'),
                               Field('antecedente_p'),
                               Field('periodo_inter'),
                               Field('primer_embarazo_masdecuatro'),
                               Field('antecedente_a', css_class='checkbox-primary'),
                               active=False
                               )
            )

        )


class EmbarazadaFormCrear(EmbarazadaForm):

    def clean(self):
        cleaned_data = super(EmbarazadaForm, self).clean()

        if Embarazada.objects.filter(NSS=cleaned_data['NSS']).exists():
            raise ValidationError('Ya existe en la base de datos: Los números de seguridad social son únicos')
        return self.cleaned_data


class SubirEpidemio(ModelForm):
    class Meta:
        model = ArchivoEpidemio
        fields = ('archivo', )


class SubirEmbarazada(ModelForm):
    class Meta:
        model = ArchivoEmbarazada
        fields = ('archivo',)


class ConsultaEmbarazada(Form):
    NSS = CharField(label='Número de Seguridad Social', validators=[validador_nss])

    def clean(self):
        if self.cleaned_data:
            cleaned_data = super(ConsultaEmbarazada, self).clean()
            existe = Embarazada.objects.filter(NSS=cleaned_data['NSS']).count()
            if existe:
                return self.cleaned_data
            else:
                raise ValidationError('No existe en la base de datos')


class ConsultaDireccion(Form):
    NUM_EXT = IntegerField(label='Número exterior', required=True)
    IDE_CAL = CharField(label='Calle', required=True)
    DES_EDO_RES = ModelChoiceField(
        queryset=Entidad.objects.all(),
        label="Entidad",
        required=False,
        widget=ModelSelect2Widget(
            model=Entidad,
            search_fields=['nomgeo__icontains'],
        )
    )
    DES_MPO_RES = ModelChoiceField(
        queryset=Municipio.objects.all(),
        label="Municipio",
        required=False,
        widget=ModelSelect2Widget(
            model=Municipio,
            search_fields=['nomgeo__icontains'],
            dependent_fields={'DES_EDO_RES': 'entidad'},
        )
    )
    IDE_CP = IntegerField(label='Código postal', validators=[validador_cp], required=True)
    distancia = FloatField(label='Distancia en kilómetros', required=True, initial=1.0)

    def __init__(self, *args, **kwargs):
        super(ConsultaDireccion, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Buscar', css_class='btn-success'))
        self.helper.form_class = 'form'
        self.helper.help_text_inline = True
        self.helper.layout = Layout(
            Field('NUM_EXT'),
            Field('IDE_CAL'),
            Field('DES_EDO_RES'),
            Field('DES_MPO_RES'),
            Field('IDE_CP'),
            Field('distancia')
        )
