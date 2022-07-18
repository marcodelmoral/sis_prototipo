from datetime import date

import pandas as pd
from scipy.stats import chi2, chi2_contingency

from dengue.models import Vector
from geo.models import Entidad


def entidades_dropdown_opciones() -> list[dict[str, str]]:
    return [{"label": "Todos", "value": "todos"}] + [
        {"label": x["nomgeo"], "value": x["cvegeo"]}
        for x in list(Entidad.objects.values("cvegeo", "nomgeo"))
        ]


def vectores_dropdown_fecha(inicio: bool = True) -> date:
    if inicio:
        return Vector.objects.order_by("fec_sol_aten")[:1][0].fec_sol_aten
    else:
        return Vector.objects.order_by("-fec_sol_aten")[:1][0].fec_sol_aten


def diagnosticos_dropdown_barras() -> list[dict[str, str]]:
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

    estadistico, valor_p, gld, esperado = chi2_contingency(tabla)

    critico = chi2.ppf(nivel_significancia, gld)

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
        "gdl": gld,
        "esperado": esperado,
        "alfa": alfa,
        "prueba_estadistico": hipotesis_critico,
        "prueba_valor-p": hipotesis_valor_p,
        }
