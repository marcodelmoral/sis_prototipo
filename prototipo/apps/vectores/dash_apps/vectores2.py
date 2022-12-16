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
from django.db.models import Count
from django_pandas.io import read_frame
from django_plotly_dash import DjangoDash

from prototipo.apps.geo.models import Entidad, Municipio
# Configura
# =======================================================================
from prototipo.apps.geo.serializers import MunicipioGeoCountSerializer, MunicipioGeoSerializer
from prototipo.apps.vectores.models import Vector
from prototipo.apps.vectores.serializers import VectorSerializer

vector_qs = Vector.objects.all()
municipios_qs = Municipio.objects.all()
entidades_dict = list(Entidad.objects.values("cvegeo", "nomgeo"))

qs_fechas = list(Vector.objects.order_by('fec_sol_aten')[:1].union(
    Vector.objects.order_by('-fec_sol_aten')[:1],
    all=True)
)

year_range = list(range(qs_fechas[0].fec_sol_aten.year, qs_fechas[1].fec_sol_aten.year + 1))
month_range = ['Enero',
               'Febrero',
               'Marzo',
               'Abril',
               'Mayo',
               'Junio',
               'Julio',
               'Agosto',
               'Septiembre',
               'Octubre',
               'Noviembre',
               'Diciembre']

dengue_nombre = "dengue_mapa2"
app = DjangoDash(
    name=dengue_nombre, serve_locally=True, external_stylesheets=[dbc.themes.DARKLY]
)
# Municipio.objects.all().annotate(
#     num_casos=Count('vector', filter=Q(vector__fec_sol_aten__range=["2012-01-01", "2020-01-08"])))
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
                            # end_date=date(2017, 6, 21),
                            # display_format='M-D-Y-Q',
                            # start_date_placeholder_text='M-D-Y-Q'
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
                            multi=False,
                            value=[],
                            options=[{"label": "Todos", "value": "todos"}]
                                    + [
                                        {"label": x["nomgeo"], "value": x["cvegeo"]}
                                        for x in entidades_dict
                                    ],
                        ),

                        dcc.Dropdown(
                            id="year",
                            multi=False,
                            value=[],
                            options=[{"label": x, "value": x} for x in year_range],
                        ),
                        dcc.Dropdown(
                            id="month",
                            multi=False,
                            value=[],
                            options=[{"label": x, 'value': y} for x, y in zip(month_range, range(1, 13))],
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
                            multi=False,
                            value=[],
                            options=[
                                {"label": x["nomgeo"], "value": x["cvegeo"]}
                                for x in entidades_dict
                            ],
                        ),
                        # dcc.DatePickerRange(
                        #     id="fechaddd",
                        #     start_date_placeholder_text="Start Period",
                        #     end_date_placeholder_text="End Period",
                        #     calendar_orientation="vertical",
                        #     min_date_allowed=datetime.date(2000, 1, 12),
                        #     max_date_allowed=datetime.date(2040, 1, 12),
                        #     clearable=True,
                        #     start_date=datetime.date.today()
                        #     ),
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
    Input("year", "value"),
    Input("month", "value"),
)
def update_choro(entidad, year, month):
    print(entidad, year, month)
    if not entidad:
        raise PreventUpdate

    if not year or not month:
        raise PreventUpdate

    vectores = vector_qs.all()
    muns = municipios_qs.all()

    vectores = vectores.filter(municipio__entidad__cve_ent=entidad)
    # print(vectores)
    muns = muns.filter(entidad=entidad)
    # print(muns)

    vectores = vectores.filter(fec_sol_aten__year=year, fec_sol_aten__month=month)
    # print(vectores)
    if not vectores:
        raise PreventUpdate

    geojson = json.dumps(MunicipioGeoSerializer(muns, many=True).data)
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
    vectores_count.sort_values(by="fec_sol_aten", inplace=True)
    print(vectores_count.dtypes)
    vectores_count['fec_sol_aten'] = vectores_count['fec_sol_aten'].astype(str)
    data = gpd.GeoDataFrame(pd.merge(gdf, vectores_count, on="cvegeo", how='left'))
    data.sort_values(by="fec_sol_aten", inplace=True)
    # print(data.dtypes)
    data['fec_sol_aten'] = data['fec_sol_aten'].astype(str)
    # print(geojson)
    fig = px.choropleth_mapbox(
        data,
        geojson=data.geometry,
        locations=data.cvegeo,
        title="Titulo",
        # featureidkey='properties.cvegeo',
        color="count",
        # center={"lat": 18.85, "lon": -97.1},
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
    # print(fig)
    return fig


@app.callback(
    Output("choro-vectorr", "figure"),
    # Output("table", "data"),
    Input("entidad-dddd", "value"),
    # Input("fechaddd", "start_date"),
    # Input("fechaddd", "end_date"),
)
def update_choroo(entidad):
    if not entidad:
        raise PreventUpdate

    muns = municipios_qs.all()

    muns = muns.filter(entidad=entidad)
    # print(muns)

    muns_count = muns.values('cvegeo', 'nomgeo', 'vector__fec_sol_aten', 'geometry').annotate(num_casos=Count('vector'))

    geojson = json.dumps(MunicipioGeoCountSerializer(muns_count, many=True).data)
    gdf = gpd.read_file(geojson)
    print(gdf.columns)
    gdf['num_casos'] = gdf['num_casos'].fillna(0).astype(str)
    gdf.rename(columns={"id": "cvegeo"}, inplace=True)
    gdf['vector__fec_sol_aten'] = pd.to_datetime(gdf['vector__fec_sol_aten'])
    gdf.sort_values('vector__fec_sol_aten', inplace=True)
    gdf = gdf[(gdf['vector__fec_sol_aten'].dt.year == 2017) & (gdf['vector__fec_sol_aten'].dt.month == 10)]
    gdf['vector__fec_sol_aten'] = gdf['vector__fec_sol_aten'].astype(str)
    print(gdf[['cvegeo', 'num_casos', 'vector__fec_sol_aten']])
    fig = px.choropleth_mapbox(
        gdf,
        geojson=gdf.geometry,
        locations=gdf.index,
        title="Titulo",
        # featureidkey='properties.cvegeo',
        color="num_casos",
        center={"lat": 18.85, "lon": -97.1},
        # mapbox_style="open-street-map",
        # hover_data=["num"],
        color_continuous_scale="Cividis_r",
        width=950,
        height=700,
        animation_frame="vector__fec_sol_aten",
        animation_group="nomgeo",
        template="plotly_dark",
    )
    fig.update_layout(mapbox_style="dark", mapbox_accesstoken=settings.MAPBOX_KEY)
    fig.update_traces(marker_line_width=0)
    fig.update_geos(fitbounds="locations")

    return fig
