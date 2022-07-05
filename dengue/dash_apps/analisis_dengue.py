import datetime
import locale

from dengue.models import Vector
from geo.models import Entidad, Municipio

locale.setlocale(locale.LC_TIME, "es_ES")

import dash_bootstrap_components as dbc

import plotly.express as px
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from django.conf import settings
from django_pandas.io import read_frame
from django_plotly_dash import DjangoDash


# Preparación de datos
# ==============================================================================


def entidades_dropdown_opciones():
    return [{"label": "Todos", "value": "todos"}] + [
        {"label": x["nomgeo"], "value": x["cvegeo"]} for x in list(Entidad.objects.values("cvegeo", "nomgeo"))
        ]


def vectores_dropdown_fecha_inicio():
    return Vector.objects.order_by("fec_sol_aten")[:1][0].fec_sol_aten


def vectores_dropdown_fecha_final():
    return Vector.objects.order_by("-fec_sol_aten")[:1][0].fec_sol_aten


# Declaración de app
# ==============================================================================
dengue_nombre = "analisis_dengue"
app = DjangoDash(
    name=dengue_nombre, serve_locally=True, external_stylesheets=[dbc.themes.DARKLY]
    )

app.layout = dbc.Container(
    [
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
        dbc.Row(dcc.Graph(id="mapa-vector")),
        dbc.Row(
            html.Div(
                children=[
                    dash_table.DataTable(
                        data=[],
                        id="tabla-vector",
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
                            # "maxWidth": 0,
                            },
                        style_table={
                            "overflowX": "auto",
                            "width": "calc(100% - 15px)",
                            },
                        )
                    ]
                )
            ),
        dbc.Row(
            dbc.Col(
                html.H3(
                    "Análisis de casos", className="text-center text-light mb-4"
                    ),
                width=12,
                )
            ),
        # dbc.Row(
        #     [dcc.Dropdown(
        #         id="analisis-dropdown",
        #         placeholder="Selecciona diagnóstico",
        #         multi=True,
        #         value=["todos"],
        #         options=[{"label": "Todos", "value": "todos"}]
        #                 + [
        #                     {"label": x, "value": x}
        #                     for x in [c[1] for c in Vector.DIAGNOSTICO]
        #                     ],
        #         )]
        #     ),
        dbc.Row([
            dbc.Col(dcc.Graph(id="grafica-diagnostico")),
            dbc.Col(dcc.Graph(id="grafica-diagnostico-sexo"))
            ])
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
    Output("mapa-vector", "figure"),
    Output("tabla-vector", "data"),
    Output("grafica-diagnostico", "figure"),
    Output("grafica-diagnostico-sexo", "figure"),
    Input("municipios-dropdown", "value"),
    Input("entidades-dropdown", "value"),
    Input("rango-fechas", "start_date"),
    Input("rango-fechas", "end_date"),
    )
def update_map(municipios, entidad, fecha_inicial, fecha_final):
    vectores = Vector.objects.all()

    if municipios is None or entidad is None:
        raise PreventUpdate

    if entidad != ["todos"]:
        vectores = vectores.filter(municipio__entidad__cve_ent__in=entidad)

    if municipios != ["todos"]:
        vectores = vectores.filter(municipio__in=municipios)

    if fecha_inicial is not None and fecha_final is not None:
        vectores = vectores.filter(fec_sol_aten__range=[fecha_inicial, fecha_final])
        if not vectores:
            raise PreventUpdate

    geo_df = read_frame(vectores, verbose=True)
    # geo_df.set_index("fol_id", inplace=True)
    geo_df['edad'] = geo_df['ide_fec_nac'].apply(
        lambda x: datetime.datetime.today().year - x.year -
                  ((datetime.datetime.today().month, datetime.datetime.today().day) < (x.month, x.day))
        )
    geo_df["nombre"] = geo_df["ide_nom"] + " " + geo_df["ide_ape_pat"] + " " + geo_df["ide_ape_mat"]
    geo_df["direccion"] = (
            geo_df["num_ext"]
            + " "
            + geo_df["ide_cal"]
            + " "
            + geo_df["ide_cp"]
            + ", "
            + geo_df["ide_col"]
    )
    geo_df["lat"] = geo_df["geometry"].apply(lambda x: x.y)
    geo_df["lon"] = geo_df["geometry"].apply(lambda x: x.x)
    print(geo_df.columns)
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
    columnas_hover_data = list(geo_df.columns)
    for i, ele in enumerate(geo_df.head().to_dict("records")[0].items()):
        print(i, ele)

    df_grupo = geo_df.groupby("cve_diag_final").size().reset_index()
    df_grupo.rename(columns={0: "Cantidad de casos", "cve_diag_final": "Diagnóstico"}, inplace=True)
    df_grupo_sexo = geo_df.groupby(["cve_diag_final", "ide_sex"]).size().reset_index()
    df_grupo_sexo.rename(columns={0: "Cantidad de casos", "cve_diag_final": "Diagnóstico", "ide_sex": "Sexo"},
                         inplace=True)
    print(df_grupo_sexo)
    fig = px.scatter_mapbox(
        geo_df,
        lat="lat",
        lon="lon",
        hover_data=columnas_hover_data,
        template="plotly_dark",
        color="cve_diag_final",
        width=1500,
        height=600,
        )
    fig.update_layout(
        mapbox_style="dark",
        mapbox_accesstoken=settings.MAPBOX_KEY,
        legend_title_text="Diagnóstico final",
        margin=dict(l=10, t=10, b=10, r=10),
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

    fig_pie = px.pie(
        df_grupo,
        values="Cantidad de casos",
        names="Diagnóstico",
        template="plotly_dark",
        title="Proporción de casos por diagnóstico final",
        )
    fig_pie.update_traces(
        # textposition="inside",
        # hoverinfo='label+percent+name',
        textinfo="label+value+percent",
        # hole=.3
        )
    fig_pie.update_layout(
        showlegend=False,
        )
    fig_diag_sexo = px.bar(
        df_grupo_sexo,
        x="Diagnóstico",
        y="Cantidad de casos",
        color="Sexo",
        barmode="stack",
        template="plotly_dark",
        title="Proporción de casos por diagnóstico final y sexo",
        text_auto=True,
        # labels=dict(cve_diag_final="Diagnóstico", ide_sex="Sexo")
        )
    return fig, geo_df.to_dict("records"), fig_pie, fig_diag_sexo
