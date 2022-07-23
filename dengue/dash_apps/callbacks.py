from datetime import date, datetime

from dash.exceptions import PreventUpdate
from django.db.models import F
from django_pandas.io import read_frame

from dengue.models import Vector
from geo.models import Municipio


def rellena_municipio(entidades: list | str):
    """

    Args:
        entidades:

    Returns:

    """
    municipios = Municipio.objects.all()

    if isinstance(entidades, list):
        if entidades != ["todos"]:
            municipios = municipios.filter(entidad__in=entidades)
    elif isinstance(entidades, str):
        municipios = municipios.filter(entidad=entidades)
    else:
        raise PreventUpdate

    lista_municipios = list(municipios.values("cvegeo", "nomgeo"))
    return [{"label": x["nomgeo"], "value": x["cvegeo"]} for x in lista_municipios]


def prepara_datos(municipio: str | list, entidad: str | list, fecha_inicial: date, fecha_final: date) -> str:
    """

    Args:
        municipio:
        entidad:
        fecha_inicial:
        fecha_final:

    Returns:

    """
    vectores = Vector.objects.all().annotate(entidad=F("municipio__entidad__nomgeo"))
    if municipio is None or entidad is None:
        raise PreventUpdate

    if isinstance(municipio, list) and isinstance(entidad, list):

        if entidad != ["todos"]:
            vectores = vectores.filter(municipio__entidad__cve_ent__in=entidad)

        if municipio != ["todos"]:
            vectores = vectores.filter(municipio__in=municipio)

    elif isinstance(municipio, str) and isinstance(entidad, str):

        vectores = vectores.filter(municipio=municipio)
    else:
        raise PreventUpdate

    if fecha_inicial and fecha_final:
        vectores = vectores.filter(fec_sol_aten__range=[fecha_inicial, fecha_final])

    if not vectores:
        raise PreventUpdate

    df = read_frame(vectores, verbose=True)

    df["edad"] = df["ide_fec_nac"].apply(
        lambda x: datetime.today().year
                  - x.year
                  - (
                          (datetime.today().month, datetime.today().day)
                          < (x.month, x.day)
                  )
        )
    df["nombre"] = (
            df["ide_nom"] + " " + df["ide_ape_pat"] + " " + df["ide_ape_mat"]
    )
    df["direccion"] = (
            df["num_ext"]
            + " "
            + df["ide_cal"]
            + ", "
            + df["ide_cp"]
            + ", "
            + df["ide_col"]
    )
    df["lat"] = df["geometry"].apply(lambda x: x.y)
    df["lon"] = df["geometry"].apply(lambda x: x.x)

    df = df.drop(
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
    df.fillna(" ", inplace=True)

    # debug
    for i, ele in enumerate(df.head().to_dict("records")[0].items()):
        print(i, ele)

    return df.to_json(date_format="iso", orient="split")
