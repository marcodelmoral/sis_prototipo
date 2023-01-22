import datetime
import locale

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.io as pio
from dash import dcc, html
from dash.dependencies import Input, Output
from django.conf import settings
from django_plotly_dash import DjangoDash

from sis_prototipo.apps.vectores.dash_apps.callbacks import (
    prepara_datos,
    rellena_municipio,
)
from sis_prototipo.apps.vectores.dash_apps.utils import (
    diagnosticos_dropdown,
    entidades_opciones_dropdown,
    vectores_fecha_dropdown,
)

locale.setlocale(locale.LC_TIME, "es_ES.utf8")

pio.templates.default = settings.PLOTLY_DEFAULT_THEME
# TODO: Hay un bug en la generacion de datos para los dropdowns. Hay que revisar que no se jalen cuando se inicializa la app de dash
# Declaración de app
# ==============================================================================
nombre = "analisis_dengue"
app = DjangoDash(
    name=nombre, external_stylesheets=[dbc.themes.DARKLY], serve_locally=True
)

app.layout = dbc.Container(
    [
        html.Div(id="dummy-load", style={'display': 'none'}),
        dcc.Store(id="datos-procesados"),
        dbc.Row(
            dbc.Col(
                html.H1(
                    "Distribución espacial",
                    className="text-center text-light mb-4",
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
                    ),
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="municipios-dropdown",
                        placeholder="Selecciona municipios",
                        multi=True,
                        # value=["todos"],
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
                dcc.Dropdown(
                    id="grafica-barras-dropdown",
                    placeholder="Selecciona el diagnóstico",
                    multi=True,
                    # value=[x["value"] for x in diagnosticos_dropdown()],
                    # options=diagnosticos_dropdown(),
                )
            ]
        ),
        dbc.Row(
            dcc.Loading(
                dcc.Graph(id="mapa-vector"),
                type="cube",
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Loading(
                        dcc.Graph(id="grafica-diagnostico-sunburst"),
                        type="cube",
                    )
                ),
            ]
        ),
        # dbc.Row(
        #     html.Div(
        #         children=[
        #             dash_table.DataTable(
        #                 data=[],
        #                 id="tabla-vector",
        #                 page_size=10,
        #                 style_header={
        #                     "backgroundColor": "rgb(30, 30, 30)",
        #                     "color": "white",
        #                     },
        #                 style_data={
        #                     "backgroundColor": "rgb(50, 50, 50)",
        #                     "color": "white",
        #                     # 'whiteSpace': 'normal',
        #                     "height": "auto",
        #                     },
        #                 style_cell={
        #                     "overflow": "hidden",
        #                     "textOverflow": "ellipsis",
        #                     # "maxWidth": 0,
        #                     },
        #                 style_table={
        #                     "overflowX": "auto",
        #                     "width": "calc(100% - 15px)",
        #                     },
        #                 )
        #             ]
        #         )
        #     ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Loading(
                        dcc.Graph(id="grafica-barras-entidad"),
                        type="cube",
                    )
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Loading(
                        dcc.Graph(id="grafica-barras-municipio"),
                        type="cube",
                    )
                ),
            ]
        ),
        dbc.Row(
            dbc.Col(
                html.H3(
                    "Análisis de casos", className="text-center text-light mb-4"
                ),
                width=12,
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Loading(
                        dcc.Graph(id="grafica-diagnostico"),
                        type="cube",
                    )
                ),
                dbc.Col(
                    dcc.Loading(
                        dcc.Graph(id="grafica-diagnostico-sexo"),
                        type="cube",
                    )
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Loading(
                        dcc.Graph(id="grafica-diagnostico-ocupacion"),
                        type="cube",
                    )
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Loading(
                        dcc.Graph(id="grafica-diagnostico-edad"),
                        type="cube",
                    )
                ),
            ]
        )
    ],
    fluid=True,
)


# Callbacks
# ==============================================================================

@app.callback(
    Output("grafica-barras-dropdown", "options"),
    Output("grafica-barras-dropdown", "value"),
    Input("dummy-load", "children"),
)
def llenar_diagnosticos_dropdown(_):
    options = diagnosticos_dropdown()
    value = [x["value"] for x in options]

    return options, value

@app.callback(
    Output("entidades-dropdown", "options"),
    Output("entidades-dropdown", "value"),
    Input("dummy-load", "children"),
)
def llenar_entidades_dropdown(_):
    value = ["todos"]
    options = entidades_opciones_dropdown()
    return options, value

@app.callback(
    Output("municipios-dropdown", "options"),
    Output("municipios-dropdown", "value"),
    Input("entidades-dropdown", "value"),
)
def rellena_municipio_callback(entidades):
    return rellena_municipio(entidades), ["todos"]

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
    return prepara_datos(municipio, entidad, fecha_inicial, fecha_final)


@app.callback(
    Output("mapa-vector", "figure"),
    Input("datos-procesados", "data"),
    Input("grafica-barras-dropdown", "value"),
)
def mapa(datos, diagnostico):
    datos = pd.read_json(datos, orient="split")
    datos = datos.loc[datos["cve_diag_final"].isin(diagnostico)]
    columnas_hover_data = list(datos.columns)

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


# @app.callback(
#     Output("tabla-vector", "data"),
#     Input("datos-procesados", "data"),
#     Input("grafica-barras-dropdown", "value"),
#     )
# def tabla(datos, diagnostico):
#     datos = pd.read_json(datos, orient="split")
#     datos = datos.loc[datos["cve_diag_final"].isin(diagnostico)]
#     return datos.to_dict("records")


@app.callback(
    Output("grafica-barras-entidad", "figure"),
    Input("datos-procesados", "data"),
    Input("grafica-barras-dropdown", "value"),
)
def grafica_barras_entidad(datos, diagnostico):
    datos = pd.read_json(datos, orient="split")
    datos = datos.loc[datos["cve_diag_final"].isin(diagnostico)]

    df_grupo = datos.groupby("entidad").size().reset_index()
    df_grupo.rename(
        columns={0: "Cantidad de casos", "entidad": "Entidad"}, inplace=True
    )
    df_grupo.sort_values("Cantidad de casos", inplace=True)
    fig = px.bar(
        df_grupo,
        x="Entidad",
        y="Cantidad de casos",
        color="Entidad",
        template="plotly_dark",
        text_auto=True,
    )
    fig.update_layout(
        title_text="Casos por entidad",
        title_x=0.5,
        showlegend=False,
        margin=dict(t=60, l=0, r=0, b=0),
    )
    return fig


@app.callback(
    Output("grafica-barras-municipio", "figure"),
    Input("datos-procesados", "data"),
    Input("grafica-barras-dropdown", "value"),
)
def grafica_barras_municipio(datos, diagnostico):
    datos = pd.read_json(datos, orient="split")
    datos = datos.loc[datos["cve_diag_final"].isin(diagnostico)]

    df_grupo = datos.groupby("municipio").size().reset_index()
    df_grupo.rename(
        columns={0: "Cantidad de casos", "municipio": "Municipio"}, inplace=True
    )
    df_grupo.sort_values("Cantidad de casos", inplace=True, ascending=False)
    fig = px.bar(
        df_grupo,
        x="Municipio",
        y="Cantidad de casos",
        color="Municipio",
        template="plotly_dark",
        text_auto=True,
    )
    fig.update_layout(
        title="Casos por municipio",
        title_x=0.5,
        showlegend=False,
        margin=dict(t=60, l=0, r=0, b=0),
    )
    return fig


@app.callback(
    Output("grafica-diagnostico", "figure"),
    Input("datos-procesados", "data"),
    Input("grafica-barras-dropdown", "value"),
)
def grafica_diagnostico_barras(datos, diagnostico):
    datos = pd.read_json(datos, orient="split")

    datos = datos.loc[datos["cve_diag_final"].isin(diagnostico)]

    df_grupo = datos.groupby("cve_diag_final").size().reset_index()
    df_grupo.sort_values("cve_diag_final", ascending=False, inplace=True)
    df_grupo.rename(
        columns={0: "Cantidad de casos", "cve_diag_final": "Diagnóstico"},
        inplace=True,
    )

    fig = px.bar(
        df_grupo,
        x="Diagnóstico",
        y="Cantidad de casos",
        color="Diagnóstico",
        template="plotly_dark",
        text_auto=True,
    )
    fig.update_layout(
        title="Casos por diagnóstico",
        title_x=0.5,
        showlegend=False,
        margin=dict(t=60, l=0, r=0, b=0),
    )
    return fig


@app.callback(
    Output("grafica-diagnostico-sexo", "figure"),
    Input("datos-procesados", "data"),
    Input("grafica-barras-dropdown", "value"),
)
def grafica_diagnostico_sexo(datos, diagnostico):
    datos = pd.read_json(datos, orient="split")

    datos = datos.loc[datos["cve_diag_final"].isin(diagnostico)]

    df_grupo = datos.groupby("ide_sex").size().reset_index()
    df_grupo.rename(
        columns={0: "Cantidad de casos", "ide_sex": "Sexo"}, inplace=True
    )

    fig = px.bar(
        df_grupo,
        x="Sexo",
        y="Cantidad de casos",
        color="Sexo",
        template="plotly_dark",
        text_auto=True,
    )
    fig.update_layout(
        title="Casos por sexo",
        title_x=0.5,
        showlegend=False,
        margin=dict(t=60, l=0, r=0, b=0),
    )
    return fig


@app.callback(
    Output("grafica-diagnostico-ocupacion", "figure"),
    Input("datos-procesados", "data"),
    Input("grafica-barras-dropdown", "value"),
)
def grafica_diagnostico_ocupacion(datos, diagnostico):
    datos = pd.read_json(datos, orient="split")

    datos = datos.loc[datos["cve_diag_final"].isin(diagnostico)]

    df_grupo = datos.groupby("des_ocupacion").size().reset_index()
    df_grupo.rename(
        columns={0: "Cantidad de casos", "des_ocupacion": "Ocupación"},
        inplace=True,
    )
    df_grupo.sort_values("Cantidad de casos", inplace=True, ascending=False)
    fig = px.bar(
        df_grupo,
        y="Ocupación",
        x="Cantidad de casos",
        color="Ocupación",
        orientation="h",
        template="plotly_dark",
        text_auto=True,
    )
    fig.update_layout(
        showlegend=False,
        title="Casos por ocupación",
        title_x=0.5,
        margin=dict(t=60, l=0, r=0, b=0),
    )
    return fig


@app.callback(
    Output("grafica-diagnostico-edad", "figure"),
    Input("datos-procesados", "data"),
    Input("grafica-barras-dropdown", "value"),
)
def grafica_diagnostico_edad(datos, diagnostico):
    datos = pd.read_json(datos, orient="split")
    datos = datos.loc[datos["cve_diag_final"].isin(diagnostico)]
    df_grupo = datos.groupby("edad").size().reset_index()
    df_grupo.rename(
        columns={0: "Cantidad de casos", "edad": "Edad"}, inplace=True
    )
    df_grupo.sort_values("Edad", inplace=True)
    df_grupo["Edad"] = df_grupo["Edad"].astype(str)
    fig = px.bar(
        df_grupo,
        x="Edad",
        y="Cantidad de casos",
        color="Edad",
        template="plotly_dark",
        text_auto=True,
    )
    fig.update_layout(
        title="Casos por edad",
        title_x=0.5,
        showlegend=False,
        margin=dict(t=60, l=0, r=0, b=0),
    )
    return fig


@app.callback(
    Output("grafica-diagnostico-sunburst", "figure"),
    Input("datos-procesados", "data"),
)
def grafica_diagnostico_sunburst(datos):
    datos = pd.read_json(datos, orient="split")
    df_grupo = (
        datos.groupby(["cve_diag_final", "ide_sex", "des_ocupacion"])
        .size()
        .reset_index()
    )
    df_grupo["Total"] = "Total"
    df_grupo.rename(
        columns={
            0: "Cantidad de casos",
            "cve_diag_final": "Diagnóstico",
            "ide_sex": "Sexo",
            "des_ocupacion": "Ocupación",
        },
        inplace=True,
    )

    df_grupo.sort_values("Diagnóstico", ascending=False, inplace=True)
    fig = px.sunburst(
        df_grupo,
        path=["Total", "Diagnóstico", "Sexo", "Ocupación"],
        color="Diagnóstico",
        values="Cantidad de casos",
        template="plotly_dark",
        branchvalues="total",
    )
    fig.update_layout(
        title="Proporción de casos",
        title_x=0.5,
        margin=dict(t=60, l=0, r=0, b=0),
    )
    fig.update_traces(textinfo="label+percent entry+percent parent")
    return fig
