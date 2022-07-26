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

from dengue.dash_apps.utils import (
    OPT_MAP, agregados_fecha_dropdown,
    datos_agregados_tipo_dropdown,
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
            center=dict(lat=20.31296, lon=-99.5364),
            style="dark",
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
                                            agregados_fecha_dropdown(inicio=False).year
                                            + 1,
                                            )
                                        )
                                    )
                                        ],
                            ),
                        ]
                    ),
                ]
            ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Loading(
                            dcc.Graph(id="fig-mapa-burbujas", figure=mapa_init()),
                            type="cube",
                            ),
                        ]
                    ),
                dbc.Col(
                    [
                        dcc.Loading(dcc.Graph(id="fig-barras", figure={}), type="cube"),
                        ]
                    ),
                ]
            ),
        dbc.Row(
            dbc.Col(
                html.H3(
                    "Analisis de series de tiempo",
                    className="text-left text-light mb-4",
                    ),
                width=12,
                )
            ),
        dbc.Row(
            [
                # dbc.Col(
                #     dcc.Dropdown(
                #         id="entidades-dropdown",
                #         placeholder="Selecciona una entidad",
                #         multi=True,
                #         value=["todos"],
                #         options=entidades_opciones_dropdown(resolver_valor=True),
                #         ),
                #     ),
                dbc.Col(
                    dcc.Dropdown(
                        id="tipo-dropdown",
                        placeholder="Selecciona una tipo de dato",
                        multi=True,
                        value=[
                            [x["value"] for x in datos_agregados_tipo_dropdown()][0]
                            ],
                        options=datos_agregados_tipo_dropdown(),
                        )
                    ),
                ]
            ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Loading(dcc.Graph(id="fig-series", figure={}), type="cube"),
                        ]
                    ),
                ]
            ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id="tipo-agregados-dropdown",
                        placeholder="Selecciona una tipo de dato",
                        multi=True,
                        value=[
                            [
                                x["value"]
                                for x in datos_agregados_tipo_dropdown(agregados=True)
                                ][0]
                            ],
                        options=datos_agregados_tipo_dropdown(agregados=True),
                        )
                    ),
                dbc.Col(
                    dcc.Dropdown(
                        id="periodo-dropdown",
                        placeholder="Selecciona una periodo",
                        multi=False,
                        value="año",
                        options=[{"label": "Por año", "value": "año"}, {"label": "Por mes", "value": "mes"}]
                        )
                    ),
                ]
            ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Loading(dcc.Graph(id="fig-series-agregados", figure={}), type="cube"),
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
    df["año"] = df["fecha"].dt.year
    df["mes"] = df["fecha"].dt.month
    return df.to_json(date_format="iso", orient="split")


@app.callback(
    Output("fig-mapa-burbujas", "figure"),
    Output("fig-barras", "figure"),
    Input("datos-procesados", "data"),
    Input("ano-dropdown", "value"),
    # Input("mes-dropdown", "value"),
    )
def mapa_burbujas_callback(datos, ano):
    # TODO: Agregar porcentajes a la grafica de barras o animar un grafico de pastel
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
        id_vars=["entidad", "fecha", "año", "mes"],
        value_vars="valor",
        value_name="casos",
        )
    datos["casos"] = datos["casos"].astype(int)
    datos.drop(columns="variable", inplace=True)
    if ano == "todos":
        datos_totales = (
            datos.groupby("entidad")["casos"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )
        datos_totales["año"] = "Totales"
        datos_anuales = datos.groupby(["entidad", "año"])["casos"].sum().reset_index()
        datos_anuales.sort_values(by="año", ascending=True, inplace=True)

        datos_agrupados = pd.concat([datos_totales, datos_anuales], axis=0)
        datos = gpd.GeoDataFrame(pd.merge(df_entidades, datos_agrupados, on="entidad"))

        datos["geometry"] = datos["geometry"].centroid

        fig_mapa_burbujas = px.scatter_mapbox(
            datos,
            lat=datos.geometry.y,
            lon=datos.geometry.x,
            color="entidad",
            size="casos",
            template="plotly_dark",
            zoom=3,
            animation_frame="año",
            animation_group="entidad",
            size_max=40,
            )
        fig_mapa_burbujas.update_layout(
            mapbox_style="dark",
            mapbox_accesstoken=settings.MAPBOX_KEY,
            title_text="Mapa de burbujas para casos",
            title_x=0.5,
            showlegend=False,
            )

        fig_mapa_burbujas.update_geos(fitbounds="locations")

        fig_barras = px.bar(
            datos,
            x="entidad",
            y="casos",
            template="plotly_dark",
            color="entidad",
            animation_frame="año",
            animation_group="entidad",
            )
        fig_barras.update_layout(
            showlegend=False,
            title_text="Gráfico de barras para casos",
            title_x=0.5,
            )

        return fig_mapa_burbujas, fig_barras
    else:
        datos = datos[datos["año"] == ano]
        datos_agrupados = (
            datos.groupby(["entidad", "mes"])["casos"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )
        datos = gpd.GeoDataFrame(pd.merge(df_entidades, datos_agrupados, on="entidad"))

        datos["geometry"] = datos["geometry"].centroid
        datos.sort_values(by="mes", ascending=True, inplace=True)
        datos["mes"] = datos["mes"].apply(lambda x: calendar.month_name[x].capitalize())
        fig_mapa_burbujas = px.scatter_mapbox(
            datos,
            lat=datos.geometry.y,
            lon=datos.geometry.x,
            color="entidad",
            size="casos",
            template="plotly_dark",
            zoom=3,
            animation_frame="mes",
            animation_group="entidad",
            size_max=40,
            )
        fig_mapa_burbujas.update_layout(
            mapbox_style="dark",
            mapbox_accesstoken=settings.MAPBOX_KEY,
            title_text="Mapa de burbujas para casos",
            title_x=0.5,
            showlegend=False,
            )

        fig_mapa_burbujas.update_geos(fitbounds="locations")

        fig_barras = px.bar(
            datos,
            x="entidad",
            y="casos",
            template="plotly_dark",
            color="entidad",
            animation_frame="mes",
            animation_group="entidad",
            )
        fig_barras.update_layout(
            showlegend=False,
            title_text="Gráfico de barras para casos",
            title_x=0.5,
            )

        return fig_mapa_burbujas, fig_barras


@app.callback(
    Output("fig-series", "figure"),
    Input("datos-procesados", "data"),
    # Input("entidades-dropdown", "value"),
    Input("tipo-dropdown", "value"),
    )
def serie_estados_callback(datos, tipos):
    datos = pd.read_json(datos, orient="split")
    datos["fecha"] = pd.to_datetime(datos["fecha"])
    datos.sort_values(by=["fecha", "entidad"], inplace=True)
    # if entidades != ["todos"]:
    #     datos = datos[datos["entidad"].isin(entidades)]
    datos = datos[datos["tipo"].isin(tipos)]
    fig = px.line(
        datos,
        x="fecha",
        y="valor",
        color="entidad",
        line_dash="tipo",
        template="plotly_dark",
        )
    fig.update_layout(
        title_text="Serie de tiempo para entidades",
        title_x=0.5,
        xaxis_title="Fecha",
        yaxis_title="Valor",
        xaxis=dict(
            rangeselector=dict(
                bgcolor="rgb(68, 68, 68)",
                buttons=list(
                    [
                        dict(
                            count=1,
                            label="1m",
                            step="month",
                            stepmode="backward",
                            ),
                        dict(
                            count=6,
                            label="6m",
                            step="month",
                            stepmode="backward",
                            ),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(
                            count=1,
                            label="1y",
                            step="year",
                            stepmode="backward",
                            ),
                        dict(step="all"),
                        ]
                    ),
                ),
            rangeslider=dict(visible=True),
            type="date",
            ),
        )
    return fig


@app.callback(
    Output("fig-series-agregados", "figure"),
    Input("datos-procesados", "data"),
    Input("tipo-agregados-dropdown", "value"),
    Input("periodo-dropdown", "value")
    )
def serie_agregados_callback(datos, tipos, periodo):
    # TODO: ver si se pueden agregar por mes
    if periodo == "mes":
        periodo = "fecha"

    datos = pd.read_json(datos, orient="split")
    datos["fecha"] = pd.to_datetime(datos["fecha"])
    datos.sort_values(by=["fecha", "entidad"], inplace=True)

    datos = datos.pivot_table(
        values="valor", index=["fecha", "año", "mes", "entidad"], columns=["tipo"]
        ).reset_index()

    datos_totales = datos.groupby("fecha").agg(OPT_MAP).reset_index()

    columnas = {
        ele[1]: f'{ele[1]} ({"suma" if OPT_MAP[ele[1]] == "sum" else "media"})'
        for ele in DatosAgregados.TIPO_DATO
        }
    datos_totales.rename(columns=columnas, inplace=True)
    datos_totales = datos_totales.melt(
        id_vars="fecha", value_vars=list(columnas.values())
        )
    datos_totales["entidad"] = "Agregados"
    # datos_totales = datos_totales[datos_totales["tipo"].isin(tipos)]

    datos_entidades = (
        datos.groupby(["fecha", "entidad"])
        .agg(OPT_MAP)
        .reset_index()
    )
    datos_entidades.rename(columns=columnas, inplace=True)
    datos_entidades = datos_entidades.melt(
        id_vars=["fecha", "entidad"], value_vars=list(columnas.values())
        )
    datos = pd.concat([datos_entidades, datos_totales], axis=0)
    print(datos)
    datos = datos[datos["tipo"].isin(tipos)]
    fig = px.line(
        datos,
        x="fecha",
        y="value",
        color="entidad",
        line_dash="tipo",
        template="plotly_dark",
        )
    fig.update_layout(
        title_text="Serie de tiempo agregadas para entidades",
        title_x=0.5,
        xaxis_title="Fecha",
        yaxis_title="Valor",
        xaxis=dict(
            rangeselector=dict(
                bgcolor="rgb(68, 68, 68)",
                buttons=list(
                    [
                        dict(
                            count=1,
                            label="1m",
                            step="month",
                            stepmode="backward",
                            ),
                        dict(
                            count=6,
                            label="6m",
                            step="month",
                            stepmode="backward",
                            ),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(
                            count=1,
                            label="1y",
                            step="year",
                            stepmode="backward",
                            ),
                        dict(step="all"),
                        ]
                    ),
                ),
            rangeslider=dict(visible=True),
            type="date",
            ),
        )

    return fig
