import datetime
import locale

import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from django.conf import settings
from django_plotly_dash import DjangoDash
from sklearn.cluster import DBSCAN

from sis_prototipo.apps.vectores.dash_apps.callbacks import (
    prepara_datos,
    rellena_municipio,
)
from sis_prototipo.apps.vectores.dash_apps.utils import (
    cmap_aleatorio,
    entidades_opciones_dropdown,
    mapa_init,
    vectores_fecha_dropdown,
)

locale.setlocale(locale.LC_TIME, "es_ES.utf8")

pio.templates.default = settings.PLOTLY_DEFAULT_THEME

# Declaración de app
# ==============================================================================
nombre = "clustering_dengue"
app = DjangoDash(
    name=nombre, external_stylesheets=[dbc.themes.DARKLY]
)

app.layout = dbc.Container(
    [
        html.Div(id="dummy-load"),
        dcc.Store(id="datos-procesados"),
        dbc.Row(
            dbc.Col(
                html.H1("Clustering", className="text-center text-light mb-4"),
                width=12,
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id="entidades-dropdown",
                        placeholder="Selecciona una entidad",
                        multi=False
                    ),
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="municipios-dropdown",
                        placeholder="Selecciona un municipio",
                        multi=False,
                        # value=None,
                    ),
                ),
                dbc.Col(
                    dcc.DatePickerRange(
                        id="rango-fechas",
                        start_date_placeholder_text="Inicio",
                        end_date_placeholder_text="Final",
                        calendar_orientation="vertical",
                        min_date_allowed=datetime.date(2000, 1, 12),
                        max_date_allowed=datetime.date(2040, 1, 12),
                        clearable=True,
                        display_format="D/MMM/YYYY",
                    ),
                ),
            ]
        ),
        dbc.Row(
            [
                dcc.Slider(0, 500, 10, value=100, id="distancia-slider"),
            ]
        ),
        dbc.Row(
            [
                dcc.Slider(2, 10, 1, value=2, id="muestras-slider"),
            ]
        ),
        dbc.Row(
            dcc.Loading(
                dcc.Graph(id="mapa-vector", figure=mapa_init()),
                type="cube",
            )
        ),
        dbc.Row(
            dcc.Loading(
                html.Div(
                    id="tabla-vector",
                    children=[dash_table.DataTable(id="tabla1")],
                ),
                type="cube",
            )
        ),
    ],
    fluid=True,
)


# Callbacks
# ==============================================================================
@app.callback(
    Output("entidades-dropdown", "options"),
    Output("entidades-dropdown", "value"),
    Input("dummy-load", "children"),
)
def llenar_entidades_dropdown(_):
    value = None
    options = entidades_opciones_dropdown()
    return options, value

@app.callback(
    Output("municipios-dropdown", "options"),
    Input("entidades-dropdown", "value"),
)
def rellena_municipio_callback(entidades):
    return rellena_municipio(entidades)

@app.callback(
    Output("rango-fechas", "start_date"),
    Output("rango-fechas", "end_date"),
    Output("rango-fechas", "min_date_allowed"),
    Output("rango-fechas", "max_date_allowed"),
    Input("dummy-load", "children")
)
def llena_rango_fechas(_):
    start_date = vectores_fecha_dropdown()
    end_date = vectores_fecha_dropdown(inicio=False)
    return start_date, end_date, start_date, end_date


@app.callback(
    Output("datos-procesados", "data"),
    Input("municipios-dropdown", "value"),
    Input("entidades-dropdown", "value"),
    Input("rango-fechas", "start_date"),
    Input("rango-fechas", "end_date"),
)
def prepara_datos_callback(municipio, entidad, fecha_inicial, fecha_final):
    # TODO: Creo que se puede mejorar para que se descarguen los datos al cargar la pagina y no cada vez que se
    #  aplica el dropdown
    return prepara_datos(municipio, entidad, fecha_inicial, fecha_final)


@app.callback(
    Output("mapa-vector", "figure"),
    Output("tabla-vector", "children"),
    Input("datos-procesados", "data"),
    Input("distancia-slider", "value"),
    Input("muestras-slider", "value"),
)
def mapa(datos, distancia, numero_muestras):
    distancia = distancia / 1000
    print(f"km: {distancia}, numero_muestras: {numero_muestras}")

    if datos is None:
        raise PreventUpdate

    datos = pd.read_json(datos, orient="split")
    datos.drop_duplicates(subset=["fol_id"], inplace=True)
    coords = datos[["lat", "lon"]].values
    print(coords)
    modelo = DBSCAN(
        eps=distancia / 6371.0,
        min_samples=numero_muestras,
        algorithm="ball_tree",
        metric="haversine",
        n_jobs=-1,
    ).fit(np.radians(coords))

    etiquetas = modelo.labels_

    # debug
    numero_grupos = len(set(etiquetas))
    print(f"num_clusters: {numero_grupos}")

    cmap = cmap_aleatorio(
        numero_grupos if numero_grupos > 1 else 2,  # Solo funciona con n > 1
        intensidad="brillante",
        primero_blanco=True,
        ultimo_blanco=False,
    )

    datos["grupo"] = etiquetas
    datos.sort_values("grupo", inplace=True)
    datos["grupo"] = datos["grupo"].astype(str)

    columnas_hover_data = list(datos.columns)

    fig = px.scatter_mapbox(
        datos,
        lat="lat",
        lon="lon",
        color_discrete_map=dict(zip(datos["grupo"].unique(), cmap)),
        hover_data=columnas_hover_data,
        template="plotly_dark",
        color="grupo",
        width=1500,
        height=600,
        zoom=11,
    )

    fig.update_layout(
        title_text=f"Mapa de casos: {distancia} km, {numero_muestras} muestras",
        title_x=0.5,
        mapbox_style="dark",
        mapbox_accesstoken=settings.MAPBOX_KEY,
        legend_title_text="Grupo",
        margin=dict(l=10, t=60, b=10, r=10),
        legend=dict(
            font=dict(
                # size=8,
            )
        ),
    )

    fig.update_traces(
        marker=dict(size=12),
        hovertemplate="<b>ID:</b> %{customdata[0]} <br><br>"
        "<b>Grupo: </b>%{customdata[13]} <br>"
        "<b>Municipio:</b> %{customdata[2]} <br>"
        "<b>Coordenadas: </b>%{lat}, %{lon}<br>"
        "<b>Nombre: </b>%{customdata[9]} <br>"
        "<b>Fecha de nacimiento: </b>%{customdata[3]} <br>"
        "<b>Fecha de solicitud de atención: </b>%{customdata[6]} <br>"
        "<b>Dirección: </b>%{customdata[10]} <br>"
        "<b>Sexo: </b>%{customdata[1]} <br>"
        "<b>Ocupación: </b>%{customdata[5]} <br>"
        "<extra></extra>",
    )
    fig.update_geos(fitbounds="locations")
    tabla = dash_table.DataTable(
        id="tabla-output",
        columns=[{"name": c, "id": c} for c in datos.columns],
        data=datos.to_dict("records"),
        style_header={"backgroundColor": "rgb(30, 30, 30)", "color": "white"},
        style_data={
            "backgroundColor": "rgb(50, 50, 50)",
            "color": "white",
            "whiteSpace": "normal",
            "height": "auto",
        },
    )
    return fig, tabla
