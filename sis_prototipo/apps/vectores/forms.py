from crispy_forms.bootstrap import Alert, Field, Tab, TabHolder
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout, Submit
from django.forms import ModelChoiceField, ModelForm, TextInput
from django_select2.forms import ModelSelect2Widget
from leaflet.forms.widgets import LeafletWidget

from sis_prototipo.apps.geo.models import Entidad, Localidad, Municipio
from sis_prototipo.apps.vectores.models import Vector


class VectorForm(ModelForm):
    des_edo_res = ModelChoiceField(
        queryset=Entidad.objects.all(),
        label="Entidad",
        widget=ModelSelect2Widget(
            model=Entidad,
            search_fields=["nomgeo__icontains"],
        ),
    )
    des_mpo_res = ModelChoiceField(
        queryset=Municipio.objects.all(),
        label="Municipio",
        widget=ModelSelect2Widget(
            model=Municipio,
            search_fields=["nomgeo__icontains"],
            dependent_fields={"des_edo_res": "entidad"},
        ),
    )

    des_loc_res = ModelChoiceField(
        queryset=Localidad.objects.all(),
        label="Localidad",
        widget=ModelSelect2Widget(
            model=Localidad,
            search_fields=["nomloc__icontains"],
            dependent_fields={"des_mpo_res": "municipio"},
        ),
    )

    class Meta:
        model = Vector
        labels = {
            "nss": "Número de seguridad social",
            "ide_nom": "Nombre",
            "ide_ape_pat": "Apellido paterno",
            "ide_ape_mat": "Apellido materno",
            "ide_sex": "Sexo",
            "num_ext": "Número exterior",
            "num_int": "Número interior",
            "ide_cal": "Calle",
            "ide_calle1": "Entre calle",
            "ide_calle2": "y calle",
            "ide_col": "Colonia",
            "ide_cp": "Código postal",
            "fec_sol_aten": "Fecha de solicitud de atención",
            "des_diag_final": "Diagnóstico final",
            "geometry": "Punto geográfico",
        }

        exclude = (
            "creado",
            "coords",
            "precision",
            "cve_diag_final",
            "activo",
            "peligro",
        )

        widgets = {
            "fec_sol_aten": TextInput(attrs={"type": "date"}),
            "geometry": LeafletWidget(),
        }

    def __init__(self, *args, **kwargs):
        super(VectorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(
            Submit("submit", "Guardar", css_class="btn-success")
        )
        self.helper.form_class = "form-horizontal"
        self.helper.help_text_inline = True
        self.helper.layout = Layout(
            Fieldset(
                "Datos generales",
                Field("nss"),
                Field("ide_nom"),
                Field("ide_ape_pat"),
                Field("ide_ape_mat"),
                Field("ide_sex"),
            ),
            Fieldset(
                "Diagnóstico", Field("fec_sol_aten"), Field("des_diag_final")
            ),
            Fieldset(
                "Información geográfica",
                Alert(
                    content="<strong>Atención: </strong> Poner dirección o punto geográfico, no los dos",
                    css_class="alert alert-warning",
                ),
                TabHolder(
                    Tab(
                        "Geoposición",
                        "geometry",
                    ),
                    Tab(
                        "Direccion",
                        "num_ext",
                        "num_int",
                        "ide_cal",
                        "ide_calle1",
                        "ide_calle2",
                        "ide_cp",
                        "ide_col",
                        "des_edo_res",
                        "des_mpo_res",
                        "des_loc_res",
                    ),
                ),
            ),
        )
