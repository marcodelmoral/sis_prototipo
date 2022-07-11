from datetime import date

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
