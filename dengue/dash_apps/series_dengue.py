import calendar
import json
import locale

import dash_bootstrap_components as dbc
import geopandas as gpd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from dash import dcc, html
from dash.dependencies import Input, Output
from django.conf import settings
from django_pandas.io import read_frame
from django_plotly_dash import DjangoDash

from dengue.dash_apps.utils import (agregados_fecha_dropdown,
                                    )
from dengue.models import DatosAgregados
from geo.models import Entidad
from geo.serializers import EntidadGeoSerializer

locale.setlocale(locale.LC_TIME, "es_ES")

pio.templates.default = settings.PLOTLY_DEFAULT_THEME

nombre = "series_dengue"
app = DjangoDash(
    name=nombre, serve_locally=True, external_stylesheets=[dbc.themes.DARKLY]
    )


def mapa_init():
    fig = go.Figure()
    fig.add_trace(go.Scattermapbox())
    fig.update_layout(
        mapbox=dict(
            accesstoken=settings.MAPBOX_KEY,
            zoom=5,
            center=dict(
                lat=20.31296,
                lon=-99.5364
                ),
            style='dark'
            ),
        title_text="Mapa de casos",
        title_x=0.5,
        margin=dict(l=10, t=60, b=10, r=10),
        )
    return fig


app.layout = dbc.Container(
    [
        html.Div(id="carga-inicial"),
        dcc.Store(id="datos-procesados"),
        dbc.Row(
            dbc.Col(
                html.H1(
                    "Tablero de datos ",
                    className="text-center text-light mb-4",
                    ),
                width=12,
                )
            ),
        dbc.Row(
            dbc.Col(
                html.H3(
                    "Resumen nacional de casos",
                    className="text-left text-light mb-4",
                    ),
                width=12,
                )
            ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id="ano-dropdown",
                            placeholder="Selecciona un año",
                            multi=False,
                            value="todos",
                            options=[{"label": "Todos", "value": "todos"}]
                                    + [
                                        {"label": x, "value": x}
                                        for x in reversed(
                                    list(
                                        range(
                                            agregados_fecha_dropdown().year,
                                            agregados_fecha_dropdown(inicio=False).year + 1,
                                            )
                                        )
                                    )
                                        ],
                            ),
                        ]
                    ),
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id="mes-dropdown",
                            placeholder="Selecciona un mes",
                            multi=False,
                            value=None,
                            options=[{"label": "Todos", "value": "todos"}] + [
                                {"label": mes.capitalize(), "value": i + 1} for i, mes in
                                enumerate(calendar.month_name[1:])]
                            ),
                        ]
                    ),
                ]
            ),
        dbc.Row([
            dbc.Col(
                [
                    dcc.Graph(id="fig-mapa-burbujas", figure=mapa_init()),
                    ]
                ),
            ]),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id="fig-barras", figure={}),
                        ]
                    ),
                dbc.Col(
                    [
                        dcc.Graph(id="fig-pastel", figure={}),
                        ]
                    ),

                ]
            ),
        ],
    fluid=True,
    )


@app.callback(
    Output("datos-procesados", "data"),
    Input("carga-inicial", "children"),
    )
def prepara_datos_callback(_):
    qs = DatosAgregados.objects.all()
    df = read_frame(qs, verbose=True)
    df["fecha"] = pd.to_datetime(df["fecha"], format="%Y-%d-%m")
    df["ano"] = df["fecha"].dt.year
    df["mes"] = df["fecha"].dt.month
    print("datos descargados")
    return df.to_json(date_format="iso", orient="split")


# @app.callback(
#     Output("mes-dropdown", "value"),
#     Input("ano-dropdown", "value"),
#     )
# def valida_periodo(ano):
#     if ano == "todos":
#         return "todos"


@app.callback(
    Output("fig-mapa-burbujas", "figure"),
    Input("datos-procesados", "data"),
    Input("ano-dropdown", "value"),
    Input("mes-dropdown", "value"),
    )
def mapa_burbujas_callback(datos, ano, mes):
    entidades_geojson = json.dumps(
        EntidadGeoSerializer(Entidad.objects.all(), many=True).data
        )
    df_entidades = gpd.read_file(entidades_geojson)
    df_entidades.rename(columns={"nomgeo": "entidad"}, inplace=True)
    datos = pd.read_json(datos, orient="split")

    datos["fecha"] = pd.to_datetime(datos["fecha"])
    datos.sort_values(by="fecha", inplace=True)

    datos = datos[datos["tipo"] == "Número de casos"]
    datos = datos.melt(
        id_vars=["entidad", "fecha", "ano", "mes"], value_vars="valor", value_name="casos"
        )
    datos["casos"] = datos["casos"].astype(int)
    # datos["ano"] = datos["fecha"].dt.year
    # datos["mes"] = datos["fecha"].dt.month
    datos.drop(columns="variable", inplace=True)
    print(datos[['ano', 'mes']])
    print(datos.head())
    if ano != "todos":
        datos = datos[datos["ano"] == ano]
        if mes != "todos":
            datos = datos[datos["mes"] == mes]

    datos_agrupados = (
        datos.groupby("entidad")["casos"].sum().sort_values(ascending=False)
    )
    datos = gpd.GeoDataFrame(
        pd.merge(df_entidades, datos_agrupados, on="entidad")
        )

    datos["geometry"] = datos["geometry"].centroid
    datos.sort_values(by="casos", ascending=False, inplace=True)
    print(datos.columns)
    print(datos)
    fig_mapa_burbujas = px.scatter_mapbox(
        datos,
        lat=datos.geometry.y,
        lon=datos.geometry.x,
        color="entidad",
        size="casos",
        template="plotly_dark",
        zoom=5,
        )
    fig_mapa_burbujas.update_layout(
        mapbox_style="dark",
        mapbox_accesstoken=settings.MAPBOX_KEY,
        showlegend=False,
        )
    # fig_bubble.update_traces(marker_line_width=0)
    fig_mapa_burbujas.update_geos(fitbounds="locations")
    return fig_mapa_burbujas

    # df_entidades_bar = df_entidades.copy()
    # df_entidades_bar.rename(columns={"nomgeo": "entidad"}, inplace=True)
    # # print(df_entidades_bar.columns)
    # df_bar = df.copy()[df["tipo"] == "Número de casos"]
    # df_bar = df_bar.melt(
    #     id_vars=["entidad", "fecha"], value_vars="valor", value_name="casos"
    #     )
    # df_bar["casos"] = df_bar["casos"].astype(int)
    # df_bar["fecha"] = df_bar["fecha"].dt.year
    # df_bar.drop(columns="variable", inplace=True)
    # if year != "todos":
    #     df_bar = df_bar[df_bar["fecha"] == year]
    #
    # group = (
    #     df_bar.groupby("entidad")["casos"].sum().sort_values(ascending=False)
    # )
    #
    # df_bubble = gpd.GeoDataFrame(
    #     pd.merge(df_entidades_bar, group, on="entidad")
    #     )
    # df_bubble["geometry"] = df_bubble["geometry"].centroid
    # df_bubble.sort_values(by="casos", ascending=False, inplace=True)
    # fig_bar = px.bar(
    #     group.reset_index(),
    #     x="entidad",
    #     y="casos",
    #     template="plotly_dark",
    #     color="entidad",
    #     )
    # fig_bar.update_layout(
    #     showlegend=False,
    #     )
    # fig_pie = px.pie(
    #     group.reset_index(),
    #     values="casos",
    #     names="entidad",
    #     template="plotly_dark",
    #     )
    # fig_pie.update_traces(textposition="inside", textinfo="percent+label")
    # fig_pie.update_layout(
    #     showlegend=False,
    #     )
    #
    # fig_bubble = px.scatter_mapbox(
    #     df_bubble,
    #     lat=df_bubble.geometry.y,
    #     lon=df_bubble.geometry.x,
    #     color="entidad",
    #     size="casos",
    #     template="plotly_dark",
    #     )
    # fig_bubble.update_layout(
    #     mapbox_style="dark",
    #     mapbox_accesstoken=settings.MAPBOX_KEY,
    #     showlegend=False,
    #     )
    # # fig_bubble.update_traces(marker_line_width=0)
    # fig_bubble.update_geos(fitbounds="locations")
    # return fig_bar, fig_pie, fig_bubble
