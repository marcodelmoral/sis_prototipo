import calendar
import locale

import dash_bootstrap_components as dbc
import pandas as pd
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

locale.setlocale(locale.LC_TIME, "es_ES")

pio.templates.default = settings.PLOTLY_DEFAULT_THEME

nombre = "series_dengue"
app = DjangoDash(
    name=nombre, serve_locally=True, external_stylesheets=[dbc.themes.DARKLY]
    )

app.layout = dbc.Container(
    [
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
                            id="selector-periodo-dropdown",
                            placeholder="Selecciona un periodo",
                            multi=False,
                            value="Año",
                            options=[
                                {"label": "Año", "value": "Año"},
                                {"label": "Mes", "value": "Mes"},
                                ],
                            ),
                        ]
                    ),
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id="periodo-dropdown",
                            multi=False,
                            value=None,
                            options=[]
                            ),
                        ]
                    ),
                ]
            ),
        dbc.Row([
            dbc.Col(
                [
                    dcc.Graph(id="fig-mapa-burbujas", figure=go.Figure(go.Scattergeo()))
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
    Output("periodo-dropdown", "options"),
    Output("periodo-dropdown", "value"),
    Output("periodo-dropdown", "placeholder"),
    Input("selector-periodo-dropdown", "value"),
    )
def rellena_periodo_callback(periodo):
    print(periodo)
    if periodo == "Año":
        fecha = agregados_fecha_dropdown()
        return (
            [{"label": "Todos", "value": "todos"}]
            + [
                {"label": x, "value": x}
                for x in reversed(
                    list(
                        range(
                            fecha[0].year,
                            fecha[1].year + 1,
                            )
                        )
                    )
                ], "todos", "Selecciona un año"
            )
    elif periodo == "Mes":
        return [mes.capitalize() for mes in calendar.month_name[1:]], "Enero", "Selecciona un mes"


@app.callback(
    Output("datos-procesados", "data"),
    Input("selector-periodo-dropdown", "value"),
    )
def prepara_datos_callback(_):
    qs = DatosAgregados.objects.all()
    df = read_frame(qs, verbose=True)

    df["fecha"] = pd.to_datetime(df["fecha"], format="%Y-%d-%m")
    df.sort_values(by="fecha", inplace=True)
    print("datos descargados")
    return df.to_json(date_format="iso", orient="split")


@app.callback(
    Output("fig-bubble", "figure"),
    Input("datos-procesados", "data"),
    Input("periodo-dropdown", "value"),
    )
def mapa_burbujas_callback(datos, periodo):
    datos = pd.read_json(datos, orient="split")
    datos.rename(columns={"nomgeo": "entidad"}, inplace=True)
    datos = datos[datos["tipo"] == "Número de casos"]
    datos = datos.melt(
        id_vars=["entidad", "fecha"], value_vars="valor", value_name="casos"
        )
    datos["casos"] = datos["casos"].astype(int)
    datos["fecha"] = datos["fecha"].dt.year
    datos.drop(columns="variable", inplace=True)
    print(datos, "procesados")
    if periodo == "Año":
        return None
    elif periodo == "Mes":
        return None
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
