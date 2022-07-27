import colorsys
from datetime import date

import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from matplotlib.colors import LinearSegmentedColormap
from scipy.stats import chi2, chi2_contingency
from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.stattools import acf, pacf

from dengue.models import DatosAgregados, Vector
from geo.models import Entidad
from prototipo import settings

OPT_MAP = {
    "Número de casos": "sum",
    "Precipitación": "mean",
    "Temperatura máxima": "mean",
    "Temperatura mínima": "mean",
    "Temperatura promedio": "mean",
    }


def entidades_opciones_dropdown(resolver_valor: bool = False, todos=True) -> list[dict[str, str]]:
    """
    TODO: mejorar
    Returns:

    """

    if resolver_valor:
        entidades = [
            {"label": x["nomgeo"], "value": x["nomgeo"]}
            for x in list(Entidad.objects.values("nomgeo"))
            ]
    else:
        entidades = [
            {"label": x["nomgeo"], "value": x["cvegeo"]}
            for x in list(Entidad.objects.values("cvegeo", "nomgeo"))
            ]
    if todos:
        return [{"label": "Todos", "value": "todos"}] + entidades
    return entidades


def vectores_fecha_dropdown(inicio: bool = True) -> date:
    """

    Args:
        inicio:

    Returns:

    """
    if inicio:
        return Vector.objects.order_by("fec_sol_aten")[:1][0].fec_sol_aten
    else:
        return Vector.objects.order_by("-fec_sol_aten")[:1][0].fec_sol_aten


def diagnosticos_dropdown() -> list[dict[str, str]]:
    """

    Returns:

    """
    return [{"label": x[1], "value": x[1]} for x in Vector.DIAGNOSTICO]


def agregados_fecha_dropdown(inicio: bool = True) -> date:
    """

    Args:
        inicio:

    Returns:

    """
    if inicio:
        return DatosAgregados.objects.order_by("fecha")[:1][0].fecha
    else:
        return DatosAgregados.objects.order_by("-fecha")[:1][0].fecha


def datos_agregados_tipo_dropdown(agregados=False) -> list[dict[str, str]]:
    """
    TODO: mejorar
    Returns:
    """

    if agregados:
        return [
            {
                "label": f'{ele[1]} ({"suma" if OPT_MAP[ele[1]] == "sum" else "media"})',
                "value": f'{ele[1]} ({"suma" if OPT_MAP[ele[1]] == "sum" else "media"})',
                }
            for ele in DatosAgregados.TIPO_DATO
            ]
    return [{"label": x[1], "value": x[1]} for x in DatosAgregados.TIPO_DATO]


def prueba_chi_cuadrada(
        df: pd.DataFrame,
        columna_variable_prueba: str,
        columna_variable_dependiente: str,
        nivel_significancia: float = 0.99,
        ) -> dict:
    """
    Prueba de chi cuadrada para verificar la correlación entre dos variables.
    Args:
        df:
        columna_variable_prueba:
        columna_variable_dependiente:
        nivel_significancia:

    Returns:

    """
    tabla = pd.crosstab(df[columna_variable_prueba], df[columna_variable_dependiente])

    estadistico, valor_p, gdl, esperado = chi2_contingency(tabla)

    critico = chi2.ppf(nivel_significancia, gdl)

    hipotesis_critico = "Independiente (No se rechaza H0)"

    if abs(estadistico) >= critico:
        hipotesis_critico = "Dependiente (Se rechaza H0)"

    alfa = 1.0 - nivel_significancia

    hipotesis_valor_p = "Independiente (No se rechaza H0)"

    if valor_p <= alfa:
        hipotesis_valor_p = "Dependiente (Se rechaza H0)"

    return {
        "estadistico": estadistico,
        "valor_p": valor_p,
        "gdl": gdl,
        "esperado": esperado,
        "alfa": alfa,
        "prueba_estadistico": hipotesis_critico,
        "prueba_valor-p": hipotesis_valor_p,
        }


def cmap_aleatorio(
        numero_colores: int,
        intensidad: str = "brillante",
        primero_blanco: bool = True,
        ultimo_blanco: bool = False,
        ):
    """

    Args:
        numero_colores:
        intensidad:
        primero_blanco:
        ultimo_blanco:

    Returns:

    """

    if intensidad not in ("brillante", "opaco"):
        print('Por favor elegir "brillante" u "opaco" para intensidad')
        return

    if intensidad == "brillante":
        randHSVcolors = [
            (
                np.random.uniform(low=0.0, high=1),
                np.random.uniform(low=0.2, high=1),
                np.random.uniform(low=0.9, high=1),
                )
            for i in range(numero_colores)
            ]

        # Convert HSV list to RGB
        randRGBcolors = []
        for HSVcolor in randHSVcolors:
            randRGBcolors.append(
                colorsys.hsv_to_rgb(HSVcolor[0], HSVcolor[1], HSVcolor[2])
                )

        if primero_blanco:
            randRGBcolors[0] = [1, 1, 1]

        if ultimo_blanco:
            randRGBcolors[-1] = [1, 1, 1]

        random_colormap = LinearSegmentedColormap.from_list(
            "new_map", randRGBcolors, N=numero_colores
            )

    if intensidad == "opaco":
        low = 0.6
        high = 0.95
        randRGBcolors = [
            (
                np.random.uniform(low=low, high=high),
                np.random.uniform(low=low, high=high),
                np.random.uniform(low=low, high=high),
                )
            for i in range(numero_colores)
            ]

        if primero_blanco:
            randRGBcolors[0] = [1, 1, 1]

        if ultimo_blanco:
            randRGBcolors[-1] = [1, 1, 1]
        random_colormap = LinearSegmentedColormap.from_list(
            "new_map", randRGBcolors, N=numero_colores
            )

    return [mcolors.rgb2hex(random_colormap(i)) for i in range(random_colormap.N)]


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
        # title_text="Mapa de casos",
        # title_x=0.5,
        margin=dict(l=10, t=60, b=10, r=10),
        )
    return fig


def descomposicion_series(datos, tipo: str = "stl", periodo: int = 12, season: int = 3, trend: int = 3,
                          low_pass: int = 0) -> dict:
    if tipo == "stl":
        descomposicion = STL(datos, period=periodo, seasonal=season, trend=trend, low_pass=low_pass, robust=True).fit()
        trendencia = descomposicion.trend
        estacionalidad = descomposicion.seasonal
        residuales = descomposicion.resid
        return {"tendencia": trendencia, "estacionalidad": estacionalidad, "residuales": residuales}


def create_corr_plot(series, plot_pacf=False):
    corr_array = pacf(series.dropna(), alpha=0.05) if plot_pacf else acf(series.dropna(), alpha=0.05)
    lower_y = corr_array[1][:, 0] - corr_array[0]
    upper_y = corr_array[1][:, 1] - corr_array[0]

    fig = go.Figure()
    [fig.add_scatter(x=(x, x), y=(0, corr_array[0][x]), mode='lines', line_color='#3f3f3f')
     for x in range(len(corr_array[0]))]
    fig.add_scatter(x=np.arange(len(corr_array[0])), y=corr_array[0], mode='markers', marker_color='#1f77b4',
                    marker_size=12)
    fig.add_scatter(x=np.arange(len(corr_array[0])), y=upper_y, mode='lines', line_color='rgba(255,255,255,0)')
    fig.add_scatter(x=np.arange(len(corr_array[0])), y=lower_y, mode='lines', fillcolor='rgba(32, 146, 230,0.3)',
                    fill='tonexty', line_color='rgba(255,255,255,0)')
    fig.update_traces(showlegend=False)
    fig.update_xaxes(range=[-1, 42])
    fig.update_yaxes(zerolinecolor='#000000')

    title = 'Partial Autocorrelation (PACF)' if plot_pacf else 'Autocorrelation (ACF)'
    fig.update_layout(title=title)
    return fig
