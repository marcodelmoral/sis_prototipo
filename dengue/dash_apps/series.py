import json
import locale

import dash_bootstrap_components as dbc
import geopandas as gpd
import pandas as pd
import plotly.express as px
import plotly.io as pio
from dash import dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from django.conf import settings
from django_pandas.io import read_frame
from django_plotly_dash import DjangoDash

from dengue.models import DatosAgregados
from geo.models import Entidad
from geo.serializers import EntidadGeoSerializer

locale.setlocale(locale.LC_TIME, "es_ES")

pio.templates.default = settings.PLOTLY_DEFAULT_THEME

dengue_nombre = "dengue_series"
app = DjangoDash(
    name=dengue_nombre,
    serve_locally=True,
    external_stylesheets=[dbc.themes.DARKLY]
    # app_name=app_name
    )

qs = DatosAgregados.objects.all()

df = read_frame(qs, verbose=True)

df["fecha"] = pd.to_datetime(df["fecha"], format="%Y-%d-%m")
df.sort_values(by="fecha", inplace=True)
# df = df.set_index("fecha")

lista_entidades = list(df["entidad"].unique())
lista_tipo = list(df["tipo"].unique())

opt_map = {
    "Número de casos": "sum",
    "Precipitación": "mean",
    "Temperatura máxima": "mean",
    "Temperatura mínima": "mean",
    "Temperatura promedio": "mean",
    }

columns_replace = {
    ele: f'{ele} ({"suma" if opt_map[ele] == "sum" else "media"})'
    for ele in lista_tipo
    }

entidades_geojson = json.dumps(
    EntidadGeoSerializer(Entidad.objects.all(), many=True).data
    )
df_entidades = gpd.read_file(entidades_geojson)

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1(
                    "Series de tiempo",
                    className="text-center text-primary mb-4",
                    ),
                width=12,
                )
            ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id="entidad-1",
                            multi=True,
                            value=[lista_entidades[0]],
                            options=[{"label": "Todos", "value": "todos"}]
                                    + [
                                        {"label": x, "value": x}
                                        for x in sorted(lista_entidades)
                                        ],
                            ),
                        dcc.Dropdown(
                            id="tipo-1",
                            multi=True,
                            value=[lista_tipo[0]],
                            options=[
                                {"label": x, "value": x} for x in lista_tipo
                                ],
                            ),
                        # dcc.Graph(id="line-fig2", figure={}),
                        dcc.Graph(id="fig-1", figure={}),
                        ],
                    ),
                ],
            justify="start",
            ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id="tipo-2",
                            multi=True,
                            value=[list(columns_replace.values())[0]],
                            options=[
                                {"label": x, "value": x}
                                for x in list(columns_replace.values())
                                ],
                            ),
                        dcc.Graph(id="fig-2", figure={}),
                        ],
                    ),
                ],
            justify="start",
            ),
        dbc.Row(
            dbc.Col(
                [
                    dcc.Dropdown(
                        id="entidad-2",
                        multi=True,
                        value=[lista_entidades[0]],
                        options=[{"label": "Todos", "value": "todos"}]
                                + [
                                    {"label": x, "value": x}
                                    for x in sorted(lista_entidades)
                                    ],
                        ),
                    dcc.Dropdown(
                        id="tipo-3",
                        multi=True,
                        value=[list(columns_replace.values())[0]],
                        options=[
                            {"label": x, "value": x}
                            for x in list(columns_replace.values())
                            ],
                        ),
                    dcc.Graph(id="fig-3", figure={}),
                    ]
                ),
            ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id="year",
                            multi=False,
                            value="todos",
                            options=[{"label": "Todos", "value": "todos"}]
                                    + [
                                        {"label": x, "value": x}
                                        for x in reversed(
                                    list(
                                        range(
                                            df.fecha.min().year,
                                            df.fecha.max().year + 1,
                                            )
                                        )
                                    )
                                        ],
                            ),
                        dcc.Graph(id="fig-bar", figure={}),
                        ]
                    ),
                dbc.Col(
                    [
                        dcc.Graph(id="fig-pie", figure={}),
                        ]
                    ),
                dbc.Col(
                    [
                        dcc.Graph(id="fig-bubble", figure={}),
                        ]
                    ),
                ]
            ),
        dbc.Row(
            dbc.Col(
                [
                    dcc.Dropdown(
                        id="entidad-season1",
                        multi=False,
                        value=lista_entidades[0],
                        options=[
                            {"label": x, "value": x}
                            for x in sorted(lista_entidades)
                            ],
                        ),
                    dcc.Dropdown(
                        id="tipo-season1",
                        multi=False,
                        value=lista_tipo[0],
                        options=[{"label": x, "value": x} for x in lista_tipo],
                        ),
                    dcc.Graph(id="fig-season1", figure={}),
                    ]
                ),
            ),
        dbc.Row(
            dbc.Col(
                [
                    dcc.Dropdown(
                        id="entidad-season2",
                        multi=False,
                        value=lista_entidades[0],
                        options=[
                            {"label": x, "value": x}
                            for x in sorted(lista_entidades)
                            ],
                        ),
                    dcc.Dropdown(
                        id="tipo-season2",
                        multi=False,
                        value=lista_tipo[0],
                        options=[{"label": x, "value": x} for x in lista_tipo],
                        ),
                    dcc.Graph(id="fig-season2", figure={}),
                    ]
                ),
            ),
        dbc.Row(
            dbc.Col(
                [
                    dcc.Dropdown(
                        id="entidad-season3",
                        multi=False,
                        value=lista_entidades[0],
                        options=[
                            {"label": x, "value": x}
                            for x in sorted(lista_entidades)
                            ],
                        ),
                    dcc.Dropdown(
                        id="tipo-season3",
                        multi=False,
                        value=lista_tipo[0],
                        options=[{"label": x, "value": x} for x in lista_tipo],
                        ),
                    dcc.Graph(id="fig-season3", figure={}),
                    ]
                ),
            ),
        ],
    fluid=True,
    )


# Callback section: connecting the components
# ************************************************************************
@app.callback(
    Output("fig-1", "figure"),
    Input("entidad-1", "value"),
    Input("tipo-1", "value"),
    )
def update_graph1(entidad1, tipo1):
    if entidad1 is None or tipo1 is None:
        raise PreventUpdate
    dff = df.copy()
    if entidad1 != ["todos"]:
        dff = dff[dff["entidad"].isin(entidad1)]
    dff = dff[dff["tipo"].isin(tipo1)]
    fig = px.line(
        dff,
        x="fecha",
        y="valor",
        color="tipo",
        title="Series de tiempo",
        line_dash="entidad",
        template="plotly_dark",
        )
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
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
                        dict(
                            count=1, label="YTD", step="year", stepmode="todate"
                            ),
                        dict(
                            count=1,
                            label="1y",
                            step="year",
                            stepmode="backward",
                            ),
                        dict(step="all"),
                        ]
                    )
                ),
            rangeslider=dict(visible=True),
            type="date",
            )
        )
    return fig


@app.callback(Output("fig-2", "figure"), Input("tipo-2", "value"))
def update_graph2(tipo2):
    if tipo2 is None:
        raise PreventUpdate
    df_totales = df.copy()
    df_totales = df_totales.pivot_table(
        values="valor", index=["fecha", "entidad"], columns=["tipo"]
        ).reset_index()
    df_totales["year"] = [d.year for d in df_totales.fecha]

    data = df_totales.groupby("year").agg(opt_map).reset_index()
    data.rename(columns=columns_replace, inplace=True)
    dff_totales = data.melt(
        id_vars="year", value_vars=list(columns_replace.values())
        )
    dff_totales = dff_totales[dff_totales["tipo"].isin(tipo2)]
    fig = px.line(
        dff_totales,
        x="year",
        y="value",
        color="tipo",
        title="Totales",
        template="plotly_dark",
        )
    fig.update_xaxes(rangeslider_visible=True)
    return fig


# todo grafica de barras
@app.callback(
    Output("fig-3", "figure"),
    Input("entidad-2", "value"),
    Input("tipo-3", "value"),
    )
def update_graph3(entidad2, tipo3):
    if entidad2 is None or tipo3 is None:
        raise PreventUpdate

    df_totales_entidades = df.copy()

    if entidad2 != ["todos"]:
        df_totales_entidades = df_totales_entidades[
            df_totales_entidades["entidad"].isin(entidad2)
        ]
        # if not df_totales_entidades.empty:
        #     raise PreventUpdate

    df_totales_entidades = df_totales_entidades.pivot_table(
        values="valor", index=["fecha", "entidad"], columns=["tipo"]
        ).reset_index()
    df_totales_entidades["year"] = [d.year for d in df_totales_entidades.fecha]

    data_entidades = (
        df_totales_entidades.groupby(["year", "entidad"])
        .agg(opt_map)
        .reset_index()
    )
    data_entidades.rename(columns=columns_replace, inplace=True)
    dff_entidades = data_entidades.melt(
        id_vars=["year", "entidad"], value_vars=list(columns_replace.values())
        )
    dff_entidades = dff_entidades[dff_entidades["tipo"].isin(tipo3)]
    fig = px.line(
        dff_entidades,
        x="year",
        y="value",
        color="tipo",
        line_dash="entidad",
        title="Totales por entidad",
        template="plotly_dark",
        )
    fig.update_xaxes(rangeslider_visible=True)
    return fig


@app.callback(
    Output("fig-bar", "figure"),
    Output("fig-pie", "figure"),
    Output("fig-bubble", "figure"),
    Input("year", "value"),
    )
def update_graph_bar(year):
    df_entidades_bar = df_entidades.copy()
    df_entidades_bar.rename(columns={"nomgeo": "entidad"}, inplace=True)
    # print(df_entidades_bar.columns)
    df_bar = df.copy()[df["tipo"] == "Número de casos"]
    df_bar = df_bar.melt(
        id_vars=["entidad", "fecha"], value_vars="valor", value_name="casos"
        )
    df_bar["casos"] = df_bar["casos"].astype(int)
    df_bar["fecha"] = df_bar["fecha"].dt.year
    df_bar.drop(columns="variable", inplace=True)
    if year != "todos":
        df_bar = df_bar[df_bar["fecha"] == year]

    group = (
        df_bar.groupby("entidad")["casos"].sum().sort_values(ascending=False)
    )

    df_bubble = gpd.GeoDataFrame(
        pd.merge(df_entidades_bar, group, on="entidad")
        )
    df_bubble["geometry"] = df_bubble["geometry"].centroid
    df_bubble.sort_values(by="casos", ascending=False, inplace=True)
    fig_bar = px.bar(
        group.reset_index(),
        x="entidad",
        y="casos",
        template="plotly_dark",
        color="entidad",
        )
    fig_bar.update_layout(
        showlegend=False,
        )
    fig_pie = px.pie(
        group.reset_index(),
        values="casos",
        names="entidad",
        template="plotly_dark",
        )
    fig_pie.update_traces(textposition="inside", textinfo="percent+label")
    fig_pie.update_layout(
        showlegend=False,
        )

    fig_bubble = px.scatter_mapbox(
        df_bubble,
        lat=df_bubble.geometry.y,
        lon=df_bubble.geometry.x,
        color="entidad",
        size="casos",
        template="plotly_dark",
        )
    fig_bubble.update_layout(
        mapbox_style="dark",
        mapbox_accesstoken=settings.MAPBOX_KEY,
        showlegend=False,
        )
    # fig_bubble.update_traces(marker_line_width=0)
    fig_bubble.update_geos(fitbounds="locations")
    return fig_bar, fig_pie, fig_bubble


@app.callback(
    Output("fig-season1", "figure"),
    Input("entidad-season1", "value"),
    Input("tipo-season1", "value"),
    )
def update_graph_entidad_season(entidad, tipo):
    if not entidad:
        raise PreventUpdate
    df_season = df.copy()

    df_season = df_season[df_season["entidad"] == entidad]

    df_season = df_season[df_season["tipo"] == tipo]

    df_season["month"] = df_season["fecha"].dt.strftime("%b")
    df_season["year"] = df_season["fecha"].dt.year

    fig = px.line(
        df_season,
        x="month",
        y="valor",
        color="year",
        #  line_dash="entidad",
        # title="Totales por entidad",
        template="plotly_dark",
        )
    fig.update_layout(
        showlegend=False,
        )
    return fig


@app.callback(
    Output("fig-season2", "figure"),
    Input("entidad-season2", "value"),
    Input("tipo-season2", "value"),
    )
def update_graph_entidad_season(entidad, tipo):
    if not entidad:
        raise PreventUpdate
    df_season = df.copy()

    df_season = df_season[df_season["entidad"] == entidad]

    df_season = df_season[df_season["tipo"] == tipo]

    df_season["month"] = df_season["fecha"].dt.strftime("%b")
    df_season["year"] = df_season["fecha"].dt.year

    fig = px.box(
        df_season,
        x="month",
        y="valor",
        boxmode="overlay",
        color="month",
        template="plotly_dark",
        )
    fig.update_layout(
        showlegend=False,
        )
    return fig


@app.callback(
    Output("fig-season3", "figure"),
    Input("entidad-season3", "value"),
    Input("tipo-season3", "value"),
    )
def update_graph_entidad_season(entidad, tipo):
    if not entidad:
        raise PreventUpdate
    df_season = df.copy()

    df_season = df_season[df_season["entidad"] == entidad]

    df_season = df_season[df_season["tipo"] == tipo]

    df_season["month"] = df_season["fecha"].dt.strftime("%b")
    df_season["year"] = df_season["fecha"].dt.year

    fig = px.box(
        df_season,
        x="year",
        y="valor",
        color="year",
        template="plotly_dark",
        )
    fig.update_layout(showlegend=False, xaxis=dict(tickmode="linear"))
    return fig
