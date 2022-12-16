from django.contrib.gis.db import models


class EmbarazadaManager(models.QuerySet):
    def save(self):
        for embarazada in self:
            embarazada.save()

    def geocodifica(self, embarazadas):
        for embarazada in embarazadas:
            embarazada.geocodifica()
        return embarazadas

    def mandar_correo(self, embarazadas):
        for embarazada in embarazadas:
            embarazada.correo()

    def precisos(self):
        return self.filter(PRECISION=True)

    def activos(self):
        return self.filter(ACTIVO=True)

    def en_peligro(self):
        return self.filter(PELIGRO=True)

    def imprecisos(self):
        return self.filter(PRECISION=False)

    def probable_parto(self):
        return self.filter(PROBABLE_PARTO=True)

    def avisado(self):
        return self.filter(AVISADO=True)

    def sin_avisar(self):
        return self.filter(AVISADO=False)
