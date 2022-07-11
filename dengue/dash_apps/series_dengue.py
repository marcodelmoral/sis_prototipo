import locale

import dash_bootstrap_components as dbc
import plotly.io as pio
from dash import dcc, html
from django.conf import settings
from django_plotly_dash import DjangoDash

from dengue.dash_apps.utils import entidades_dropdown_opciones

locale.setlocale(locale.LC_TIME, "es_ES")

pio.templates.default = settings.PLOTLY_DEFAULT_THEME

dengue_nombre = "series_dengue"
app = DjangoDash(
    name=dengue_nombre,
    serve_locally=True,
    external_stylesheets=[dbc.themes.DARKLY]
    )

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("Series de tiempo", className="text-center text-primary mb-4"),
                width=12,
                )
            ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id="entidades-dropdown",
                            placeholder="Selecciona entidades",
                            multi=True,
                            value=["todos"],
                            options=entidades_dropdown_opciones(),
                            ),
                        dcc.Dropdown(
                            id="tipo-1",
                            multi=True,
                            value=[lista_tipo[0]],
                            options=[{"label": x, "value": x} for x in lista_tipo],
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
                                + [{"label": x, "value": x} for x in sorted(lista_entidades)],
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
                                            df.fecha.min().year, df.fecha.max().year + 1
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
                            {"label": x, "value": x} for x in sorted(lista_entidades)
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
                            {"label": x, "value": x} for x in sorted(lista_entidades)
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
                            {"label": x, "value": x} for x in sorted(lista_entidades)
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
