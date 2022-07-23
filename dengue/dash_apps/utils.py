from datetime import date

import pandas as pd
from scipy.stats import chi2, chi2_contingency

from dengue.models import Vector
from geo.models import Entidad
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as mcolors
import colorsys
import numpy as np


def entidades_opciones_dropdown() -> list[dict[str, str]]:
    """

    Returns:

    """
    return [{"label": "Todos", "value": "todos"}] + [
        {"label": x["nomgeo"], "value": x["cvegeo"]}
        for x in list(Entidad.objects.values("cvegeo", "nomgeo"))
        ]


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
