import calendar
import json
import locale

import dash_bootstrap_components as dbc
import geopandas as gpd
import pandas as pd
import plotly.express as px
import plotly.io as pio
from darts.timeseries import TimeSeries
from darts.utils.statistics import check_seasonality, stationarity_tests
from dash import dcc, html
from dash.dependencies import Input, Output
from django.conf import settings
from django_pandas.io import read_frame
from django_plotly_dash import DjangoDash

from prototipo.apps.geo.models import Entidad
from prototipo.apps.geo.serializers import EntidadGeoSerializer
from prototipo.apps.vectores.dash_apps.utils import (
    OPT_MAP,
    agregados_fecha_dropdown,
    create_corr_plot, datos_agregados_tipo_dropdown,
    descomposicion_series, entidades_opciones_dropdown,
    mapa_init,
)
from prototipo.apps.vectores.models import DatosAgregados

locale.setlocale(locale.LC_TIME, "es_ES")

pio.templates.default = settings.PLOTLY_DEFAULT_THEME

nombre = "series_dengue"
app = DjangoDash(
    name=nombre, serve_locally=True, external_stylesheets=[dbc.themes.DARKLY]
)

app.layout = dbc.Container(
    [
        html.Div(id="carga-inicial"),
        dcc.Store(id="datos-procesados"),
        dbc.Row(
            dbc.Col(
                html.H1(
                    "Análisis de series de tiempo",
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
                                            agregados_fecha_dropdown(
                                                inicio=False
                                            ).year
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
                )
            ]
        ),
        dbc.Row(
            [
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
        dcc.Tabs(
            id="tabs",
            value="tab1",
            colors={
                "border": "white",
                "primary": "white",
                "background": "#222222"
            },
            # parent_className="custom-tabs",
            # className="custom-tabs-container",
            children=[
                dcc.Tab(
                    label="Exploración",
                    value="tab1",
                    # className='custom-tab',
                    # selected_className='custom-tab--selected',
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Dropdown(
                                        id="tipo-dropdown",
                                        placeholder="Selecciona una tipo de "
                                                    "dato",
                                        multi=True,
                                        value=[
                                            [
                                                x["value"]
                                                for x in
                                                datos_agregados_tipo_dropdown()
                                            ][0]
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
                                        dcc.Loading(
                                            dcc.Graph(
                                                id="fig-series",
                                                figure={}
                                            ),
                                            type="cube",
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Dropdown(
                                        id="tipo-agregados-dropdown",
                                        placeholder="Selecciona una tipo de "
                                                    "dato",
                                        multi=True,
                                        value=[
                                            [
                                                x["value"]
                                                for x in
                                                datos_agregados_tipo_dropdown(
                                                    agregados=True
                                                )
                                            ][0]
                                        ],
                                        options=datos_agregados_tipo_dropdown(
                                            agregados=True
                                        ),
                                    )
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Loading(
                                            dcc.Graph(
                                                id="fig-series-agregados",
                                                figure={}
                                            ),
                                            type="cube",
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Dropdown(
                                            id="entidad-estacionalidad-dropdown",
                                            multi=False,
                                            value=
                                            entidades_opciones_dropdown(
                                                resolver_valor=True,
                                                todos=False
                                            )[0]["value"],
                                            options=entidades_opciones_dropdown(
                                                resolver_valor=True,
                                                todos=False
                                            ),
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        dcc.Dropdown(
                                            id="tipo-estacionalidad-dropdown",
                                            multi=False,
                                            value=[
                                                x["value"]
                                                for x in
                                                datos_agregados_tipo_dropdown(
                                                    agregados=False
                                                )
                                            ][0],
                                            options=datos_agregados_tipo_dropdown(
                                                agregados=False
                                            ),
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
                                            dcc.Graph(
                                                id="fig-series-estacionalidad-estado",
                                                figure={}
                                            ),
                                            type="cube",
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
                                            dcc.Graph(
                                                id="fig-barras-estacionalidad-estado",
                                                figure={}
                                            ),
                                            type="cube",
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
                                            dcc.Graph(
                                                id="fig-barras-estacionalidad-estado-año",
                                                figure={}
                                            ),
                                            type="cube",
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ],
                ),
                dcc.Tab(
                    # className='custom-tab',
                    # selected_className='custom-tab--selected',
                    label="Estadísticas",
                    value="tab2",
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Dropdown(
                                            id="entidad-analisis-dropdown",
                                            multi=False,
                                            value="Datos agregados",
                                            options=[{
                                                "label": "Datos "
                                                         "agregados",
                                                "value": "Datos "
                                                         "agregados"
                                            }] +
                                                    entidades_opciones_dropdown(
                                                        resolver_valor=True,
                                                        todos=False
                                                    ),
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        dcc.Dropdown(
                                            id="tipo-analisis-dropdown",
                                            multi=False,
                                            value=[
                                                x["value"]
                                                for x in
                                                datos_agregados_tipo_dropdown(
                                                    agregados=False
                                                )
                                            ][0],
                                            options=datos_agregados_tipo_dropdown(
                                                agregados=False
                                            ),
                                        ),
                                    ]
                                ),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id="periodo-analisis-dropdown",
                                        placeholder="Selecciona una periodo",
                                        multi=False,
                                        value="mes",
                                        options=[{
                                            "label": "Por año",
                                            "value": "año"
                                        },
                                            {
                                                "label": "Por mes",
                                                "value": "mes"
                                            }]
                                    )
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dcc.Loading(
                                    dcc.Graph(id="fig-serie-analisis", figure={}),
                                    type="cube",
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dcc.Loading(
                                    dcc.Graph(
                                        id="fig-tendencia-analisis", figure={}
                                    ),
                                    type="cube",
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dcc.Loading(
                                    dcc.Graph(
                                        id="fig-estacionalidad-analisis",
                                        figure={}
                                    ),
                                    type="cube",
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dcc.Loading(
                                    dcc.Graph(
                                        id="fig-residuales-analisis", figure={}
                                    ),
                                    type="cube",
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Loading(
                                            dcc.Graph(
                                                id="fig-series-correlacion-estado",
                                                figure={}
                                            ),
                                            type="cube",
                                        ),
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        dcc.Loading(
                                            dcc.Graph(
                                                id="fig-series-parcial-estado",
                                                figure={}
                                            ),
                                            type="cube",
                                        ),
                                    ]
                                ),
                            ]
                        ),

                    ]
                ),
            ],
        ),
    ],
    fluid=True,
)


@app.callback(
    Output("datos-procesados", "data"),
    Input("carga-inicial", "children"),
)
def prepara_datos_callback(_) -> dict:
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
)
def mapa_burbujas_callback(datos_json, ano):
    # TODO: Agregar porcentajes a la grafica de barras o animar un grafico de pastel
    entidades_geojson = json.dumps(
        EntidadGeoSerializer(Entidad.objects.all(), many=True).data
    )
    df_entidades = gpd.read_file(entidades_geojson)
    df_entidades.rename(columns={"nomgeo": "entidad"}, inplace=True)
    datos = pd.read_json(datos_json, orient="split")

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
        periodo = "año"
    else:
        periodo = "mes"

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
        zoom=3,
        animation_frame=periodo,
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
        color="entidad",
        animation_frame=periodo,
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
    Input("tipo-dropdown", "value"),
)
def serie_estados_callback(datos_json, tipos):
    datos = pd.read_json(datos_json, orient="split")
    datos["fecha"] = pd.to_datetime(datos["fecha"])
    datos.sort_values(by=["fecha", "entidad"], inplace=True)

    datos_totales = datos.pivot_table(
        values="valor", index=["fecha", "año", "mes", "entidad"], columns=["tipo"]
    ).reset_index()

    datos_totales = datos_totales.groupby("fecha").agg(OPT_MAP).reset_index()

    datos_totales = datos_totales.melt(
        id_vars="fecha",
        value_vars=[x[1] for x in DatosAgregados.TIPO_DATO],
        var_name="tipo",
        value_name="valor",
    )
    datos_totales["entidad"] = "Agregados"
    datos = pd.concat([datos, datos_totales], axis=0)
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
        title_text="Serie de tiempo para entidades por mes",
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
)
def serie_agregados_callback(datos_json, tipos):
    datos = pd.read_json(datos_json, orient="split")
    datos["fecha"] = pd.to_datetime(datos["fecha"])
    datos.sort_values(by=["año", "entidad"], inplace=True)

    datos = datos.pivot_table(
        values="valor", index=["fecha", "año", "mes", "entidad"], columns=["tipo"]
    ).reset_index()

    datos_totales = datos.groupby("año").agg(OPT_MAP).reset_index()

    columnas = {
        ele[1]: f'{ele[1]} ({"suma" if OPT_MAP[ele[1]] == "sum" else "media"})'
        for ele in DatosAgregados.TIPO_DATO
    }
    datos_totales.rename(columns=columnas, inplace=True)
    datos_totales = datos_totales.melt(
        id_vars="año", value_vars=list(columnas.values())
    )
    datos_totales["entidad"] = "Agregados"

    datos_entidades = datos.groupby(["año", "entidad"]).agg(OPT_MAP).reset_index()
    datos_entidades.rename(columns=columnas, inplace=True)
    datos_entidades = datos_entidades.melt(
        id_vars=["año", "entidad"], value_vars=list(columnas.values())
    )
    datos = pd.concat([datos_entidades, datos_totales], axis=0)
    datos = datos[datos["tipo"].isin(tipos)]
    fig = px.line(
        datos,
        x="año",
        y="value",
        color="entidad",
        line_dash="tipo",
        template="plotly_dark",
    )
    fig.update_layout(
        title_text="Serie de tiempo agregadas para entidades por año",
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
    Output("fig-series-estacionalidad-estado", "figure"),
    Output("fig-barras-estacionalidad-estado", "figure"),
    Output("fig-barras-estacionalidad-estado-año", "figure"),
    Input("datos-procesados", "data"),
    Input("entidad-estacionalidad-dropdown", "value"),
    Input("tipo-estacionalidad-dropdown", "value"),
)
def serie_agregados_callback(datos, entidad, tipo):
    datos = pd.read_json(datos, orient="split")
    datos["fecha"] = pd.to_datetime(datos["fecha"])
    datos.sort_values(by=["año", "entidad"], inplace=True, ascending=False)
    datos = datos[datos["entidad"] == entidad]

    datos = datos[datos["tipo"] == tipo]

    datos["mes"] = datos["mes"].apply(lambda x: calendar.month_name[x].capitalize())
    fig_estacionalidad_mes = px.line(
        datos,
        x="mes",
        y="valor",
        color="año",
    )
    fig_estacionalidad_mes.update_layout(
        title_text="Serie de estacionalidad por mes",
        title_x=0.5,
        xaxis_title="Mes",
        yaxis_title="Valor",
    )

    fig_barras_mes = px.box(
        datos,
        x="mes",
        y="valor",
        boxmode="overlay",
        color="mes",
    )
    fig_barras_mes.update_layout(
        showlegend=False,
        title_text="Gráfico de caja para estacionalidad por mes",
        title_x=0.5,
        xaxis_title="Mes",
        yaxis_title="Valor",
    )

    fig_barras_ano = px.box(
        datos,
        x="año",
        y="valor",
        boxmode="overlay",
        color="año",
    )
    fig_barras_ano.update_layout(
        showlegend=False,
        title_text="Gráfico de caja para estacionalidad por año",
        title_x=0.5,
        xaxis_title="Año",
        yaxis_title="Valor",
        xaxis=dict(tickmode="linear"),
    )

    return fig_estacionalidad_mes, fig_barras_mes, fig_barras_ano


@app.callback(
    Output("fig-serie-analisis", "figure"),
    Output("fig-tendencia-analisis", "figure"),
    Output("fig-estacionalidad-analisis", "figure"),
    Output("fig-residuales-analisis", "figure"),
    Output("fig-series-correlacion-estado", "figure"),
    Output("fig-series-parcial-estado", "figure"),
    Input("datos-procesados", "data"),
    Input("entidad-analisis-dropdown", "value"),
    Input("tipo-analisis-dropdown", "value"),
    Input("periodo-analisis-dropdown", "value"),
)
def serie_analisis_callback(datos_json, entidad, tipo, periodo):
    datos = pd.read_json(datos_json, orient="split")
    datos["fecha"] = pd.to_datetime(datos["fecha"])
    datos["año"] = pd.to_datetime(datos["año"], format="%Y")
    datos = datos[datos["tipo"] == tipo]

    if periodo == "mes":
        periodo = "fecha"

    if entidad == "Datos agregados":
        datos = datos.pivot_table(
            values="valor", index=["fecha", "año", "mes", "entidad"], columns=["tipo"]
        ).reset_index()
        datos = datos.groupby(periodo).agg(OPT_MAP[tipo]).reset_index()

        datos = datos.melt(
            id_vars=periodo,
            value_vars=tipo,
            var_name="tipo",
            value_name="valor",
        )
        datos["entidad"] = "Agregados"
    else:
        datos = datos[datos["entidad"] == entidad]

    if periodo == "año":
        datos = datos.groupby(["año", "entidad"]).agg(OPT_MAP[tipo]).reset_index()
        datos = datos.melt(
            id_vars=["año", "entidad"], value_vars="valor", value_name="valor"
        )
    datos.index = datos[periodo]
    # datos.index.freq = "MS" if periodo == "fecha" else "AS"
    # print(datos.index.inferred_freq)
    ts_datos = TimeSeries.from_series(datos["valor"])
    fig_serie = px.line(
        datos,
        x=periodo,
        y="valor",
    )
    estacionalidad, periodo_estacion = check_seasonality(ts_datos, max_lag=24)
    estacionariedad = stationarity_tests(ts_datos)
    estacionalidad_string = f"estacional (periodo = {periodo_estacion})" if estacionalidad else "no estacional"
    estacionariedad_string = "estacionaria" if estacionariedad else "no estacionaria"
    fig_serie.update_layout(
        title_text=f"Serie de tiempo {estacionalidad_string} {estacionariedad_string}",
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
        ),
    )
    # TODO: Slider de periodo
    # TODO: Selector de periodo (mes, año, trimeste, semestre, día, )
    descomposicion = descomposicion_series(datos["valor"], trend=13, low_pass=13)
    descomposicion = pd.DataFrame(descomposicion)
    descomposicion[periodo] = datos[periodo]
    fig_tendencia = px.line(
        descomposicion,
        x=periodo,
        y="tendencia",
    )
    fig_tendencia.update_layout(
        title_text="Tendencia",
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
        ),
    )
    fig_estacionalidad = px.line(
        descomposicion,
        x=periodo,
        y="estacionalidad",
    )
    fig_estacionalidad.update_layout(
        title_text="Estacionalidad",
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
        ),
    )
    fig_residuales = px.scatter(
        descomposicion,
        x=periodo,
        y="residuales",
    )
    fig_residuales.update_layout(
        title_text="Residuales",
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
        ),
    )
    if estacionariedad:
        # https://robjhyndman.com/hyndsight/ljung-box-test/
        lags = 2 * periodo_estacion
    else:
        lags = 10
    return fig_serie, fig_tendencia, fig_estacionalidad, fig_residuales, create_corr_plot(
        datos['valor'], lags
    ), create_corr_plot(datos['valor'], lags, plot_pacf=True)
