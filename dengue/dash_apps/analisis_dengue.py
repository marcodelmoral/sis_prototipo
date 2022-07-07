import datetime
import locale

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.io as pio
from dash import dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from django.conf import settings
from django.db.models import F
from django_pandas.io import read_frame
from django_plotly_dash import DjangoDash

from dengue.models import Vector
from geo.models import Entidad, Municipio

locale.setlocale(locale.LC_TIME, "es_ES")

pio.templates.default = settings.PLOTLY_DEFAULT_THEME


# Preparación de datos
# ==============================================================================


def entidades_dropdown_opciones():
    return [{"label": "Todos", "value": "todos"}] + [
        {"label": x["nomgeo"], "value": x["cvegeo"]}
        for x in list(Entidad.objects.values("cvegeo", "nomgeo"))
        ]


def vectores_dropdown_fecha_inicio():
    return Vector.objects.order_by("fec_sol_aten")[:1][0].fec_sol_aten


def vectores_dropdown_fecha_final():
    return Vector.objects.order_by("-fec_sol_aten")[:1][0].fec_sol_aten


def diagnosticos_dropdown_barras():
    return [{"label": x[1], "value": x[1]} for x in Vector.DIAGNOSTICO]


# Declaración de app
# ==============================================================================
dengue_nombre = "analisis_dengue"
app = DjangoDash(
    name=dengue_nombre, serve_locally=True, external_stylesheets=[dbc.themes.DARKLY]
    )

app.layout = dbc.Container(
    [
        dcc.Store(id="datos-procesados"),
        dbc.Row(
            dbc.Col(
                html.H1(
                    "Distribución espacial", className="text-center text-light mb-4"
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
                dbc.Col(
                    dcc.DatePickerRange(
                        id="rango-fechas",
                        start_date_placeholder_text="Inicio",
                        end_date_placeholder_text="Final",
                        # calendar_orientation="vertical",
                        min_date_allowed=datetime.date(2000, 1, 12),
                        max_date_allowed=datetime.date(2040, 1, 12),
                        clearable=True,
                        start_date=vectores_dropdown_fecha_inicio(),
                        end_date=vectores_dropdown_fecha_final(),
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
                    value=[x["value"] for x in diagnosticos_dropdown_barras()],
                    options=diagnosticos_dropdown_barras(),
                    )
                ]
            ),
        dbc.Row(dcc.Graph(id="mapa-vector")),
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
                dbc.Col(dcc.Graph(id="grafica-barras-entidad")),
                ]
            ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="grafica-barras-municipio")),
                ]
            ),
        dbc.Row(
            dbc.Col(
                html.H3("Análisis de casos", className="text-center text-light mb-4"),
                width=12,
                )
            ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="grafica-diagnostico")),
                dbc.Col(dcc.Graph(id="grafica-diagnostico-sexo")),
                ]
            ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="grafica-diagnostico-ocupacion")),
                ]
            ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="grafica-diagnostico-edad")),
                ]
            ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="grafica-diagnostico-sunburst")),
                ]
            ),
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
    Output("datos-procesados", "data"),
    Input("municipios-dropdown", "value"),
    Input("entidades-dropdown", "value"),
    Input("rango-fechas", "start_date"),
    Input("rango-fechas", "end_date"),
    )
def prepara_datos(entidades, municipios, fecha_inicial, fecha_final):
    vectores = Vector.objects.all().annotate(entidad=F("municipio__entidad__nomgeo"))
    if municipios is None or entidades is None:
        raise PreventUpdate

    if entidades != ["todos"]:
        vectores = vectores.filter(municipio__entidad__cve_ent__in=entidades)

    if municipios != ["todos"]:
        vectores = vectores.filter(municipio__in=municipios)

    if fecha_inicial is not None and fecha_final is not None:
        vectores = vectores.filter(fec_sol_aten__range=[fecha_inicial, fecha_final])

    if not vectores:
        raise PreventUpdate

    geo_df = read_frame(vectores, verbose=True)

    geo_df["edad"] = geo_df["ide_fec_nac"].apply(
        lambda x: datetime.datetime.today().year
                  - x.year
                  - (
                          (datetime.datetime.today().month, datetime.datetime.today().day)
                          < (x.month, x.day)
                  )
        )
    geo_df["nombre"] = (
            geo_df["ide_nom"] + " " + geo_df["ide_ape_pat"] + " " + geo_df["ide_ape_mat"]
    )
    geo_df["direccion"] = (
            geo_df["num_ext"]
            + " "
            + geo_df["ide_cal"]
            + ", "
            + geo_df["ide_cp"]
            + ", "
            + geo_df["ide_col"]
    )
    geo_df["lat"] = geo_df["geometry"].apply(lambda x: x.y)
    geo_df["lon"] = geo_df["geometry"].apply(lambda x: x.x)

    geo_df = geo_df.drop(
        columns=[
            "id",
            "geometry",
            "ide_nom",
            "ide_ape_pat",
            "ide_ape_mat",
            "ide_cal",
            "ide_cp",
            "ide_col",
            "num_ext",
            "num_int",
            ]
        )
    geo_df.fillna(" ", inplace=True)

    for i, ele in enumerate(geo_df.head().to_dict("records")[0].items()):
        print(i, ele)
    print(geo_df.columns)
    return geo_df.to_json(date_format="iso", orient="split")


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
        columns={0: "Cantidad de casos", "cve_diag_final": "Diagnóstico"}, inplace=True
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
    df_grupo.rename(columns={0: "Cantidad de casos", "ide_sex": "Sexo"}, inplace=True)

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
        columns={0: "Cantidad de casos", "des_ocupacion": "Ocupación"}, inplace=True
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
    df_grupo.rename(columns={0: "Cantidad de casos", "edad": "Edad"}, inplace=True)
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
        title="Proporción de casos", title_x=0.5, margin=dict(t=60, l=0, r=0, b=0)
        )
    fig.update_traces(textinfo="label+percent entry+percent parent")
    return fig
