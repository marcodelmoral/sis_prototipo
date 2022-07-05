import datetime
import json

import dash_bootstrap_components as dbc
import geopandas as gpd
import pandas as pd
import plotly.express as px
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from django.conf import settings
from django_pandas.io import read_frame
from django_plotly_dash import DjangoDash

from dengue.models import Vector
from dengue.serializers import VectorSerializer
from geo.models import Entidad, Municipio
# Configura
# =======================================================================
from geo.serializers import MunicipioSerializer

vector_qs = Vector.objects.all()
municipios_qs = Municipio.objects.all()
entidades_dict = list(Entidad.objects.values("cvegeo", "nomgeo"))
dengue_nombre = "dengue_mapa"
app = DjangoDash(
    name=dengue_nombre, serve_locally=True, external_stylesheets=[dbc.themes.DARKLY]
    )
# Municipio.objects.all().annotate(num_casos=Count('vector', filter=Q(vector__fec_sol_aten__range=["2012-01-01", "2020-01-08"])))
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("Mapa de vectores", className="text-center text-primary mb-4"),
                width=12,
                )
            ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id="entidad-dd",
                            multi=True,
                            value=[],
                            options=[{"label": "Todos", "value": "todos"}]
                                    + [
                                        {"label": x["nomgeo"], "value": x["cvegeo"]}
                                        for x in entidades_dict
                                        ],
                            ),
                        dcc.Dropdown(
                            id="municipio-dd",
                            multi=True,
                            value=None,
                            ),
                        dcc.DatePickerRange(
                            id="fecha",
                            start_date_placeholder_text="Start Period",
                            end_date_placeholder_text="End Period",
                            calendar_orientation="vertical",
                            min_date_allowed=datetime.date(2000, 1, 12),
                            max_date_allowed=datetime.date(2040, 1, 12),
                            clearable=True,
                            start_date=datetime.date.today()
                            ),
                        dcc.Graph(id="mapa-vector", figure={}),
                        ],
                    ),
                dbc.Col(
                    [
                        dash_table.DataTable(
                            data=[],
                            id="table",
                            page_size=10,
                            style_header={
                                "backgroundColor": "rgb(30, 30, 30)",
                                "color": "white",
                                },
                            style_data={
                                "backgroundColor": "rgb(50, 50, 50)",
                                "color": "white",
                                # 'whiteSpace': 'normal',
                                "height": "auto",
                                },
                            style_cell={
                                "overflow": "hidden",
                                "textOverflow": "ellipsis",
                                "maxWidth": 0,
                                },
                            style_table={"overflowX": "auto"},
                            )
                        ],
                    ),
                ],
            justify="start",
            ),
        dbc.Row(
            dbc.Col(
                html.H1("Mapa de choro", className="text-center text-primary mb-4"),
                width=12,
                )
            ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id="entidad-ddd",
                            multi=True,
                            value=[],
                            options=[{"label": "Todos", "value": "todos"}]
                                    + [
                                        {"label": x["nomgeo"], "value": x["cvegeo"]}
                                        for x in entidades_dict
                                        ],
                            ),
                        dcc.DatePickerRange(
                            id="fechadd",
                            start_date_placeholder_text="Start Period",
                            end_date_placeholder_text="End Period",
                            calendar_orientation="vertical",
                            min_date_allowed=datetime.date(2000, 1, 12),
                            max_date_allowed=datetime.date(2040, 1, 12),
                            clearable=True,
                            start_date=datetime.date.today()
                            ),
                        dcc.Graph(id="choro-vector", figure={}),
                        ]
                    ),
                ],
            justify="start",
            ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id="entidad-dddd",
                            multi=True,
                            value=[],
                            options=[{"label": "Todos", "value": "todos"}]
                                    + [
                                        {"label": x["nomgeo"], "value": x["cvegeo"]}
                                        for x in entidades_dict
                                        ],
                            ),
                        dcc.DatePickerRange(
                            id="fechaddd",
                            start_date_placeholder_text="Start Period",
                            end_date_placeholder_text="End Period",
                            calendar_orientation="vertical",
                            min_date_allowed=datetime.date(2000, 1, 12),
                            max_date_allowed=datetime.date(2040, 1, 12),
                            clearable=True,
                            start_date=datetime.date.today()
                            ),
                        dcc.Graph(id="choro-vectorr", figure={}),
                        ]
                    ),
                ],
            justify="start",
            ),
        ],
    fluid=True,
    )


@app.callback(Output("municipio-dd", "options"), Input("entidad-dd", "value"))
def update_dp(filter_value):
    muns = municipios_qs.all()
    if filter_value != ["todos"]:
        muns = muns.filter(entidad__in=filter_value)
    muns_list = list(muns.values("cvegeo", "nomgeo"))
    return [{"label": "Todos", "value": "todos"}] + [
        {"label": x["nomgeo"], "value": x["cvegeo"]} for x in muns_list
        ]


@app.callback(
    Output("mapa-vector", "figure"),
    Output("table", "data"),
    Input("municipio-dd", "value"),
    Input("entidad-dd", "value"),
    Input("fecha", "start_date"),
    Input("fecha", "end_date"),
    )
def update_map(municipios, entidad, start_date, end_date):
    if municipios is None or entidad is None:
        raise PreventUpdate

    vectores = vector_qs.all()
    if entidad != ["todos"]:
        vectores = vectores.filter(municipio__entidad__cve_ent__in=entidad)
    if municipios != ["todos"]:
        vectores = vectores.filter(municipio__in=municipios)
    if end_date:
        vectores = vectores.filter(fed_sol_aten__range=[start_date, end_date])
        if not vectores:
            raise PreventUpdate
    vector_serialized = VectorSerializer(vectores, many=True)
    geojson = json.dumps(vector_serialized.data)
    geo_df = gpd.read_file(geojson)
    hover_columns = list(geo_df.columns)
    hover_columns.remove("geometry")
    fig = px.scatter_mapbox(
        geo_df,
        lat=geo_df.geometry.y,
        lon=geo_df.geometry.x,
        zoom=10,
        hover_data=hover_columns,
        template="plotly_dark",
        color=geo_df.des_diag_final,
        animation_frame="fec_sol_aten",
        animation_group="municipio",
        )
    fig.update_layout(
        mapbox_style="dark", mapbox_accesstoken=settings.MAPBOX_KEY, autosize=True
        )
    fig.update_geos(fitbounds="locations")
    return fig, pd.DataFrame(geo_df.drop(columns="geometry")).to_dict("records")


@app.callback(
    Output("choro-vector", "figure"),
    # Output("table", "data"),
    Input("entidad-ddd", "value"),
    Input("fechadd", "start_date"),
    Input("fechadd", "end_date"),
    )
def update_choro(entidad, start_date, end_date):
    if not entidad:
        raise PreventUpdate

    vectores = vector_qs.all()
    muns = municipios_qs.all()

    if entidad != ["todos"]:
        vectores = vectores.filter(municipio__entidad__cve_ent__in=entidad)
        muns = muns.filter(entidad__in=entidad)
        # print(muns)

    if end_date:
        vectores = vectores.filter(fed_sol_aten__range=[start_date, end_date])
        if not vectores:
            raise PreventUpdate

    geojson = json.dumps(MunicipioSerializer(muns, many=True).data)
    gdf = gpd.read_file(geojson)
    gdf.rename(columns={"id": "cvegeo"}, inplace=True)

    vectores_df = read_frame(vectores, verbose=False)
    vectores_count = (
        vectores_df.groupby(["municipio", "fec_sol_aten"])
        .count()["fol_id"]
        .reset_index()
    )
    vectores_count.rename(
        columns={"fol_id": "count", "municipio": "cvegeo"}, inplace=True
        )

    data = gpd.GeoDataFrame(pd.merge(gdf, vectores_count, on="cvegeo"))

    # data_slider = []
    # for fecha in data['fec_sol_aten'].unique():
    #     # print(fecha)
    #     df_year = data[data['fec_sol_aten'] == fecha]
    #
    #     # for col in df_year.columns:
    #     #     df_year[col] = df_year[col].astype(str)
    #     # print(df_year)
    #     # print(df_year.__geo_interface__)
    #     data_one_year = dict(
    #         type='choropleth',
    #         geojson=df_year.__geo_interface__,
    #         locations=df_year.index,
    #         z=df_year['count'],
    #         # locationmode=df_year['cvegeo'],
    #         # locationmode='country names',
    #         # colorscale="greens",
    #         )
    #
    #     data_slider.append(data_one_year)
    #
    # steps = []
    #
    # for i in range(len(data_slider)):
    #     step = dict(method='restyle',
    #                 args=['visible', [False] * len(data_slider)],
    #                 label='{}'.format(i))
    #     step['args'][1][i] = True
    #     steps.append(step)
    #
    # sliders = [dict(active=0, pad={"t": 1}, steps=steps)]
    #
    # layout = dict(geo=dict(fitbounds='locations', mapbox_style="dark",
    #                        mapbox_accesstoken=settings.MAPBOX_KEY
    #                        ),
    #               sliders=sliders,
    #               )
    # fig = dict(data=data_slider, layout=layout)

    fig = px.choropleth_mapbox(
        data,
        geojson=data.geometry,
        locations=data.cvegeo,
        title="Titulo",
        # featureidkey='properties.cvegeo',
        color="count",
        center={"lat": 18.85, "lon": -97.1},
        # mapbox_style="open-street-map",
        hover_data=["count"],
        color_continuous_scale="Cividis_r",
        width=950,
        height=700,
        animation_frame="fec_sol_aten",
        # animation_group="nomgeo",
        template="plotly_dark",
        )
    fig.update_layout(mapbox_style="dark", mapbox_accesstoken=settings.MAPBOX_KEY)
    fig.update_traces(marker_line_width=0)
    fig.update_geos(fitbounds="locations")
    return fig


@app.callback(
    Output("choro-vectorr", "figure"),
    # Output("table", "data"),
    Input("entidad-dddd", "value"),
    Input("fechaddd", "start_date"),
    Input("fechaddd", "end_date"),
    )
def update_choroo(entidad, start_date, end_date):
    if not entidad:
        raise PreventUpdate

    vectores = vector_qs.all()
    muns = municipios_qs.all()

    if entidad != ["todos"]:
        vectores = vectores.filter(municipio__entidad__cve_ent__in=entidad)
        muns = muns.filter(entidad__in=entidad)
        # print(muns)

    if end_date:
        vectores = vectores.filter(fed_sol_aten__range=[start_date, end_date])
        if not vectores:
            raise PreventUpdate

    geojson = json.dumps(MunicipioSerializer(muns, many=True).data)
    gdf = gpd.read_file(geojson)
    gdf.rename(columns={"id": "cvegeo"}, inplace=True)

    vectores_df = read_frame(vectores, verbose=False)
    vectores_count = (
        vectores_df.groupby(["municipio", "fec_sol_aten"])
        .count()["fol_id"]
        .reset_index()
    )
    vectores_count.rename(
        columns={"fol_id": "count", "municipio": "cvegeo"}, inplace=True
        )

    data = gpd.GeoDataFrame(pd.merge(gdf, vectores_count, on='cvegeo', how='left'))
    data.sort_values(by="fec_sol_aten", inplace=True)
    data['count'].fillna(0, inplace=True)
    data_slider = []
    for fecha in data['fec_sol_aten'].unique():
        # print(fecha)
        df_year = data[data['fec_sol_aten'] == fecha]

        # for col in df_year.columns:
        #     df_year[col] = df_year[col].astype(str)
        # print(df_year)
        # print(df_year.__geo_interface__)
        data_one_year = dict(
            type='choropleth',
            geojson=df_year.__geo_interface__,
            locations=df_year.index,
            z=df_year['count'].astype(int),
            # locationmode=df_year['cvegeo'],
            # locationmode='country names',
            # colorscale="greens",
            )

        data_slider.append(data_one_year)

    steps = []

    # for i in range(len(data_slider)):
    #     step = dict(method='restyle',
    #                 args=['visible', [False] * len(data_slider)],
    #                 label='{}'.format(i))
    #     step['args'][1][i] = True
    #     steps.append(step)
    # print(data['fec_sol_aten'].unique())
    for i, fecha in zip(range(len(data_slider)), data['fec_sol_aten'].unique()):
        step = dict(method='restyle',
                    args=['visible', [False] * len(data_slider)],
                    label='{}'.format(fecha))
        step['args'][1][i] = True
        steps.append(step)

    sliders = [dict(active=0, pad={"t": 1}, steps=steps)]

    layout = dict(geo=dict(fitbounds='locations', mapbox_style="dark",
                           mapbox_accesstoken=settings.MAPBOX_KEY
                           ),
                  sliders=sliders,
                  mapbox_style="dark",
                  mapbox_accesstoken=settings.MAPBOX_KEY
                  )
    # print(layout)
    fig = dict(data=data_slider, layout=layout)

    return fig
