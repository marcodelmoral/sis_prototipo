import locale

import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.io as pio
from dash import dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from django.conf import settings
from django_plotly_dash import DjangoDash

from geo.models import Entidad, Municipio

locale.setlocale(locale.LC_TIME, "es_ES")

pio.templates.default = settings.PLOTLY_DEFAULT_THEME


def entidades_dropdown_opciones() -> list[dict[str, str]]:
    return [{"label": "Todos", "value": "todos"}] + [
        {"label": x["nomgeo"], "value": x["cvegeo"]}
        for x in list(Entidad.objects.values("cvegeo", "nomgeo"))
        ]


# Declaración de app
# ==============================================================================
dengue_nombre = "exploracion_mgn"
app = DjangoDash(
    name=dengue_nombre, serve_locally=True, external_stylesheets=[dbc.themes.DARKLY]
    )

app.layout = dbc.Container(
    [
        dcc.Store(id="datos-procesados"),
        dbc.Row(
            dbc.Col(
                html.H1(
                    "Exploración espacial", className="text-center text-light mb-4"
                    ),
                width=12,
                )
            ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id="entidades-dropdown",
                        placeholder="Selecciona entidades",
                        multi=True,
                        value=["todos"],
                        options=entidades_dropdown_opciones(),
                        ),
                    ),
                dbc.Col(
                    dcc.Dropdown(
                        id="municipios-dropdown",
                        placeholder="Selecciona municipios",
                        multi=True,
                        value=["todos"],
                        ),
                    ),
                ]
            ),
        dbc.Row(dcc.Graph(id="mapa-mgn"))
        ],
    fluid=True,
    )


# Callbacks
# ==============================================================================


@app.callback(
    Output("municipios-dropdown", "options"), Input("entidades-dropdown", "value")
    )
def rellena_municipio_dropdown(entidades):
    municipios = Municipio.objects.all()
    if entidades != ["todos"]:
        municipios = municipios.filter(entidad__in=entidades)
    lista_municipios = list(municipios.values("cvegeo", "nomgeo"))
    return [{"label": "Todos", "value": "todos"}] + [
        {"label": x["nomgeo"], "value": x["cvegeo"]} for x in lista_municipios
        ]


@app.callback(
    Output("mapa-vector", "figure"),
    Input("municipios-dropdown", "value"),
    Input("entidades-dropdown", "value"),
    )
def mapa(entidades, municipios):
    if municipios is None or entidades is None:
        raise PreventUpdate

    entidades = Entidad.objects.filter(cvegeo__in=entidades)

    municipios = Municipio.objects.filter(cvegeo__in=municipios)

    # manzanas = Manzana.objects.filter(municipio__cvegeo__in=municipios)

    fig = px.scatter_mapbox(
        datos,
        lat="lat",
        lon="lon",
        hover_data=columnas_hover_data,
        template="plotly_dark",
        color="cve_diag_final",
        width=1500,
        height=600,
        )
    fig.update_layout(
        title_text="Mapa de casos",
        title_x=0.5,
        mapbox_style="dark",
        mapbox_accesstoken=settings.MAPBOX_KEY,
        legend_title_text="Diagnóstico final",
        margin=dict(l=10, t=60, b=10, r=10),
        legend=dict(
            font=dict(
                # size=8,
                )
            ),
        )
    fig.update_traces(
        # marker=dict(size=6),
        hovertemplate="<b>ID:</b> %{customdata[0]} <br><br>"
                      "<b>Municipio:</b> %{customdata[2]} <br>"
                      "<b>Coordenadas: </b>%{lat}, %{lon}<br>"
                      "<b>Nombre: </b>%{customdata[7]} <br>"
                      "<b>Fecha de nacimiento: </b>%{customdata[3]} <br>"
                      "<b>Fecha de solicitud de atención: </b>%{customdata[6]} <br>"
                      "<b>Dirección: </b>%{customdata[8]} <br>"
                      "<b>Sexo: </b>%{customdata[1]} <br>"
                      "<b>Ocupación: </b>%{customdata[5]} <br>"
                      "<extra></extra>",
        )
    fig.update_geos(fitbounds="locations")
    return fig
