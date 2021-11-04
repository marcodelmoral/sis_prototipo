from django.contrib.gis.db import models

# TODO: sacar datos poblacionales en otra tabla
# TODO: quitarles el multi
entidad_mapping = {
    'cvegeo': 'CVEGEO',
    'cve_ent': 'CVE_ENT',
    'nomgeo': 'NOMGEO',
    'geom': 'MULTIPOLYGON',
    }

municipio_mapping = {
    'cvegeo': 'CVEGEO',
    'cve_ent': 'CVE_ENT',
    'cve_mun': 'CVE_MUN',
    'nomgeo': 'NOMGEO',
    'geom': 'MULTIPOLYGON',
    }

localidad_mapping = {
    'cvegeo': 'CVEGEO',
    'cve_ent': 'CVE_ENT',
    'cve_mun': 'CVE_MUN',
    'cve_loc': 'CVE_LOC',
    'nomgeo': 'NOMGEO',
    'ambito': 'AMBITO',
    'geom': 'MULTIPOLYGON',
    # 'area': 'AREA' # le puse el area
    }

# Le quite lo de agebu
ageb_mapping = {
    'cvegeo': 'CVEGEO',
    'cve_ent': 'CVE_ENT',
    'cve_mun': 'CVE_MUN',
    'cve_loc': 'CVE_LOC',
    'cve_ageb': 'CVE_AGEB',
    'geom': 'MULTIPOLYGON',
    }

# agebr_mapping = {
#     'cvegeo': 'CVEGEO',
#     'cve_ent': 'CVE_ENT',
#     'cve_mun': 'CVE_MUN',
#     'cve_ageb': 'CVE_AGEB',
#     'geom': 'MULTIPOLYGON',
# }

manzana_mapping = {
    'cvegeo': 'CVEGEO',
    'cve_ent': 'CVE_ENT',
    'cve_mun': 'CVE_MUN',
    'cve_loc': 'CVE_LOC',
    'cve_ageb': 'CVE_AGEB',
    'cve_mza': 'CVE_MZA',
    'ambito': 'AMBITO',
    'tipomza': 'TIPOMZA',
    'geom': 'MULTIPOLYGON',
    }

servicio_mapping = {
    'cvegeo': 'CVEGEO',
    'cve_ent': 'CVE_ENT',
    'cve_mun': 'CVE_MUN',
    'cve_loc': 'CVE_LOC',
    'cve_ageb': 'CVE_AGEB',
    'cve_mza': 'CVE_MZA',
    'condicion': 'CONDICION',
    'geografico': 'GEOGRAFICO',
    'nomserv': 'NOMSERV',
    'tipo': 'TIPO',
    'cve_serv': 'CVE_SERV',
    'ambito': 'AMBITO',
    'area': 'AREA',
    'geom': 'MULTIPOINT',
    }


# Poblacion por cada subdivision
# Quizas numero de subdivisiones
# Preguntar que informacion o inferencia
# Por ejemplo, sumar columnas y sacar numero de niños
class DivisionGeografica(models.Model):
    # Identificacion geografica
    geom = models.MultiPolygonField(srid=4326)
    cve_ent = models.CharField(max_length=2)
    # Relacion de indicadores
    # Poblacion
    # Se deben permitir nulos puesto que hay datos que no estan en los datos de
    # INEGI pero no son 0
    # Se coloca el verbose_name, que es el nombre de la variable de INEGI
    # Se coloca el help_text, que es la descripcion y categoria del campo
    POBTOT = models.PositiveIntegerField(null=True,
                                         blank=True,
                                         verbose_name='Población total',
                                         help_text='Total de personas que '
                                                   'residen habitualmente en '
                                                   'el país, entidad '
                                                   'federativa, municipio y '
                                                   'localidad. Incluye la '
                                                   'estimación del número de personas en viviendas particulares sin '
                                                   'información de ocupantes. Incluye a la población que no '
                                                   'especificó su edad.')
    POBMAS = models.PositiveIntegerField(null=True,
                                         blank=True,
                                         verbose_name='Población masculina',
                                         help_text='Total de hombres que '
                                                   'residen habitualmente en '
                                                   'el país, entidad '
                                                   'federativa, municipio y '
                                                   'localidad. Incluye la '
                                                   'estimación del número de hombres en viviendas particulares sin información de ocupantes. Incluye a la población que no especificó su edad.')
    POBFEM = models.PositiveIntegerField(null=True,
                                         blank=True,
                                         verbose_name='Población femenina',
                                         help_text='Total de mujeres que '
                                                   'residen habitualmente en '
                                                   'el país, entidad '
                                                   'federativa, municipio y '
                                                   'localidad. Incluye la '
                                                   'estimación del número de mujeres en viviendas particulares sin información de ocupantes. Incluye a la población que no especificó su edad.')

    # P_0A2 = models.PositiveIntegerField(null=True,
    #                                     blank=True,
    #                                     verbose_name='Población de 0 a 2 años',
    #                                     help_text='Personas de 0 a 2 años de edad.')
    # P_0A2_M = models.PositiveIntegerField(null=True,
    #                                       blank=True,
    #                                       verbose_name='Población masculina de 0 a 2 años',
    #                                       help_text='Hombres de 0 a 2 años de edad.')
    # P_0A2_F = models.PositiveIntegerField(null=True,
    #                                       blank=True,
    #                                       verbose_name='Población femenina de 0 a 2 años',
    #                                       help_text='Mujeres de 0 a 2 años de edad.')
    # P_3YMAS = models.PositiveIntegerField(null=True,
    #                                       blank=True,
    #                                       verbose_name='Población de 3 años y más',
    #                                       help_text='Personas de 3 a 130 años de edad.')
    # P_3YMAS_M = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población masculina de 3 años y más',
    #                                         help_text='Hombres de 3 a 130 años de edad.')
    # P_3YMAS_F = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población femenina de 3 años y más ',
    #                                         help_text='Mujeres de 3 a 130 años de edad.')
    # P_5YMAS = models.PositiveIntegerField(null=True,
    #                                       blank=True,
    #                                       verbose_name='Población de 5 años y más',
    #                                       help_text='Personas de 5 a 130 años de edad.')
    # P_5YMAS_M = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población masculina de 5 años y más',
    #                                         help_text='Hombres de 5 a 130 años de edad.')
    # P_5YMAS_F = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población femenina de 5 años y más ',
    #                                         help_text='Mujeres de 5 a 130 años de edad.')
    # P_12YMAS = models.PositiveIntegerField(null=True,
    #                                        blank=True,
    #                                        verbose_name='Población de 12 años y más',
    #                                        help_text='Personas de 12 a 130 años de edad.')
    # P_12YMAS_M = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población masculina de 12 años y más',
    #                                          help_text='Hombres de 12 a 130 años de edad.')
    # P_12YMAS_F = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población femenina de 12 años y más ',
    #                                          help_text='Mujeres de 12 a 130 años de edad.')
    # P_15YMAS = models.PositiveIntegerField(null=True,
    #                                        blank=True,
    #                                        verbose_name='Población de 15 años y más',
    #                                        help_text='Personas de 15 a 130 años de edad.')
    # P_15YMAS_M = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población masculina de 15 años y más',
    #                                          help_text='Hombres de 15 a 130 años de edad.')
    # P_15YMAS_F = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población femenina de 15 años y más ',
    #                                          help_text='Mujeres de 15 a 130 años de edad.')
    # P_18YMAS = models.PositiveIntegerField(null=True,
    #                                        blank=True,
    #                                        verbose_name='Población de 18 años y más',
    #                                        help_text='Personas de 18 a 130 años de edad.')
    # P_18YMAS_M = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población masculina de 18 años y más',
    #                                          help_text='Hombres de 18 a 130 años de edad.')
    # P_18YMAS_F = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población femenina de 18 años y más ',
    #                                          help_text='Mujeres de 18 a 130 años de edad.')
    # P_3A5 = models.PositiveIntegerField(null=True,
    #                                     blank=True,
    #                                     verbose_name='Población de 3 a 5 años',
    #                                     help_text='Personas de 3 a 5 años de edad.')
    # P_3A5_M = models.PositiveIntegerField(null=True,
    #                                       blank=True,
    #                                       verbose_name='Población masculina de 3 a 5 años',
    #                                       help_text='Hombres de 3 a 5 años de edad.')
    # P_3A5_F = models.PositiveIntegerField(null=True,
    #                                       blank=True,
    #                                       verbose_name='Población femenina de 3 a 5 años',
    #                                       help_text='Mujeres de 3 a 5 años de edad.')
    # P_6A11 = models.PositiveIntegerField(null=True,
    #                                      blank=True,
    #                                      verbose_name='Población de 6 a 11 años',
    #                                      help_text='Personas de 6 a 11 años de edad.')
    # P_6A11_M = models.PositiveIntegerField(null=True,
    #                                        blank=True,
    #                                        verbose_name='Población masculina de 6 a 11 años',
    #                                        help_text='Hombres de 6 a 11 años de edad.')
    # P_6A11_F = models.PositiveIntegerField(null=True,
    #                                        blank=True,
    #                                        verbose_name='Población femenina de 6 a 11 años',
    #                                        help_text='Mujeres de 6 a 11 años de edad.')
    # P_8A14 = models.PositiveIntegerField(null=True,
    #                                      blank=True,
    #                                      verbose_name='Población de 8 a 14 años',
    #                                      help_text='Personas de 8 a 14 años de edad.')
    # P_8A14_M = models.PositiveIntegerField(null=True,
    #                                        blank=True,
    #                                        verbose_name='Población masculina de 8 a 14 años',
    #                                        help_text='Hombres de 8 a 14 años de edad.')
    # P_8A14_F = models.PositiveIntegerField(null=True,
    #                                        blank=True,
    #                                        verbose_name='Población femenina de 8 a 14 años',
    #                                        help_text='Mujeres de 8 a 14 años de edad.')
    # P_12A14 = models.PositiveIntegerField(null=True,
    #                                       blank=True,
    #                                       verbose_name='Población de 12 a 14 años',
    #                                       help_text='Personas de 12 a 14 años de edad.')
    # P_12A14_M = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población masculina de 12 a 14 años',
    #                                         help_text='Hombres de 12 a 14 años de edad.')
    # P_12A14_F = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población femenina de 12 a 14 años',
    #                                         help_text='Mujeres de 12 a 14 años de edad.')
    # P_15A17 = models.PositiveIntegerField(null=True,
    #                                       blank=True,
    #                                       verbose_name='Población de 15 a 17 años',
    #                                       help_text='Personas de 15 a 17 años de edad.')
    # P_15A17_M = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población masculina de 15 a 17 años',
    #                                         help_text='Hombres de 15 a 17 años de edad.')
    # P_15A17_F = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población femenina de 15 a 17 años',
    #                                         help_text='Mujeres de 15 a 17 años de edad.')
    # P_18A24 = models.PositiveIntegerField(null=True,
    #                                       blank=True,
    #                                       verbose_name='Población de 18 a 24 años',
    #                                       help_text='Personas de 18 a 24 años de edad.')
    # P_18A24_M = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población masculina de 18 a 24 años',
    #                                         help_text='Hombres de 18 a 24 años de edad.')
    # P_18A24_F = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población femenina de 18 a 24 años',
    #                                         help_text='Mujeres de 18 a 24 años de edad.')
    # P_15A49 = models.PositiveIntegerField(null=True,
    #                                       blank=True,
    #                                       verbose_name='Población de 15 a 49 años',
    #                                       help_text='Personas de 15 a 49 años de edad.')
    # P_15A49_M = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población masculina de 15 a 49 años',
    #                                         help_text='Hombres de 15 a 49 años de edad.')
    # P_15A49_F = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población femenina de 15 a 49 años',
    #                                         help_text='Mujeres de 15 a 49 años de edad.')
    # P_60YMAS = models.PositiveIntegerField(null=True,
    #                                        blank=True,
    #                                        verbose_name='Población de 60 años y más',
    #                                        help_text='Personas de 60 a 130 años de edad.')
    # P_60YMAS_M = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población masculina de 60 años y más',
    #                                          help_text='Hombres de 60 a 130 años de edad.')
    # P_60YMAS_F = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población femenina de 60 años y más',
    #                                          help_text='Mujeres de 60 a 130 años de edad.')
    # REL_H_M = models.PositiveIntegerField(null=True,
    #                                       blank=True,
    #                                       verbose_name='Relación hombres-mujeres',
    #                                       help_text='Resultado de dividir el total de hombres entre el total de mujeres y multiplicarlo por cien. Indica el número de hombres por cada 100 mujeres..')
    # POB0_14 = models.PositiveIntegerField(null=True,
    #                                       blank=True,
    #                                       verbose_name='Población de cero a 14 años',
    #                                       help_text='Personas de cero a 14 años de edad.')
    # POB15_64 = models.PositiveIntegerField(null=True,
    #                                        blank=True,
    #                                        verbose_name='Población de 15 a 64 años',
    #                                        help_text='Personas de 15 a 64 años de edad.')
    # POB65_MAS = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población de 65 años y más',
    #                                         help_text='Personas de 65 a 130 años de edad.')
    # # Fecundidad
    # PROM_HNV = models.PositiveIntegerField(null=True,
    #                                        blank=True,
    #                                        verbose_name='Promedio de hijos nacidos vivos',
    #                                        help_text='Resultado de dividir el total de hijos '
    #                                                  'nacidos vivos de las mujeres de 12 a 130 años de edad, '
    #                                                  'entre el total de mujeres del mismo grupo de edad. '
    #                                                  'Excluye a las mujeres que no especificaron el número de hijos..')
    # # Migración
    # PNACENT = models.PositiveIntegerField(null=True,
    #                                       blank=True,
    #                                       verbose_name='Población nacida en la entidad',
    #                                       help_text='Personas nacidas en la misma entidad federativa.')
    # PNACENT_M = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población masculina nacida en la entidad',
    #                                         help_text='Hombres nacidos en la misma entidad federativa.')
    # PNACENT_F = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población femenina nacida en la entidad',
    #                                         help_text='Mujeres nacidas en la misma entidad federativa.')
    # PNACOE = models.PositiveIntegerField(null=True,
    #                                      blank=True,
    #                                      verbose_name='Población nacida en otra entidad',
    #                                      help_text='Personas nacidas en otra entidad federativa.')
    # PNACOE_M = models.PositiveIntegerField(null=True,
    #                                        blank=True,
    #                                        verbose_name='Población masculina nacida en otra entidad',
    #                                        help_text='Hombres nacidos en otra entidad federativa.')
    # PNACOE_F = models.PositiveIntegerField(null=True,
    #                                        blank=True,
    #                                        verbose_name='Población femenina nacida en otra entidad',
    #                                        help_text='Mujeres nacidas en otra entidad federativa.')
    # PRES2005 = models.PositiveIntegerField(null=True,
    #                                        blank=True,
    #                                        verbose_name='Población de 5 años y más residente en la entidad en junio de 2005',
    #                                        help_text='Personas de 5 a 130 años de edad que en los años '
    #                                                  '2005 y 2010 residían en la misma entidad federativa.')
    # PRES2005_M = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población masculina de 5 años y más residente en la entidad en junio de 2005',
    #                                          help_text='Hombres de 5 a 130 años de edad que en los años '
    #                                                    '2005 y 2010 residían en la misma entidad federativa.')
    # PRES2005_F = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población femenina de 5 años y más residente en la entidad en junio de 2005',
    #                                          help_text='Mujeres de 5 a 130 años de edad que en los años '
    #                                                    '2005 y 2010 residían en la misma entidad federativa.')
    # PRESOE05 = models.PositiveIntegerField(null=True,
    #                                        blank=True,
    #                                        verbose_name='Población de 5 años y más residente en otra entidad en junio de 2005',
    #                                        help_text='Personas de 5 a 130 años de edad que en el año 2005 residían en otra entidad federativa.')
    # PRESOE05_M = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población masculina de 5 años y más residente en otra entidad en junio de 2005',
    #                                          help_text='Hombres de 5 a 130 años de edad que en el año 2005 residían en otra entidad federativa.')
    # PRESOE05_F = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población femenina de 5 años y más residente en otra entidad en junio de 2005',
    #                                          help_text='Mujeres de 5 a 130 años de edad que en el año 2005 residían en otra entidad federativa.')
    # # Población indígena
    # P3YM_HLI = models.PositiveIntegerField(null=True,
    #                                        blank=True,
    #                                        verbose_name='Población de 3 años y más que habla alguna lengua indígena',
    #                                        help_text='Personas de 3 a 130 años de edad que hablan alguna lengua indígena.')
    # P3YM_HLI_M = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población masculiina de 3 años y más que habla alguna lengua indígena',
    #                                          help_text='Hombres de 3 a 130 años de edad que hablan alguna lengua indígena.')
    # P3YM_HLI_F = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población femenina de 3 años y más que habla alguna lengua indígena',
    #                                          help_text='Mujeres de 3 a 130 años de edad que hablan alguna lengua indígena.')
    # P3HLINHE = models.PositiveIntegerField(null=True,
    #                                        blank=True,
    #                                        verbose_name='Población de 3 años y más que habla alguna lengua indígena y no habla español',
    #                                        help_text='Personas de 3 a 130 años de edad que hablan alguna lengua indígena y además no hablan español.')
    # P3HLINHE_M = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población masculina de 3 años y más que habla alguna lengua indígena y no habla español',
    #                                          help_text='Hombres de 3 a 130 años de edad que hablan alguna lengua indígena y además no hablan español.')
    # P3HLINHE_F = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población femeninade 3 años y más que habla alguna lengua indígena y no habla español',
    #                                          help_text='Mujeres de 3 a 130 años de edad que hablan alguna lengua indígena y además no hablan español.')
    # P3HLI_HE = models.PositiveIntegerField(null=True,
    #                                        blank=True,
    #                                        verbose_name='Población de 3 años y más que habla alguna lengua indígena y habla español',
    #                                        help_text='Personas de 3 a 130 años de edad que hablan alguna lengua indígena y además hablan español.')
    # P3HLI_HE_M = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población masculina de 3 años y más que habla alguna lengua indígena y habla español',
    #                                          help_text='Hombres de 3 a 130 años de edad que hablan alguna lengua indígena y además hablan español.')
    # P3HLI_HE_F = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población femenina de 3 años y más que habla alguna lengua indígena y habla español',
    #                                          help_text='Mujeres de 3 a 130 años de edad que hablan alguna lengua indígena y además hablan español.')
    # P5_HLI = models.PositiveIntegerField(null=True,
    #                                      blank=True,
    #                                      verbose_name='Población de 5 años y más que habla alguna lengua indígena',
    #                                      help_text='Personas de 5 años y más que hablan alguna lengua indígena.')
    # P5_HLI_NHE = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población de 5 años y más que habla alguna lengua indígena y no habla español',
    #                                          help_text='Personas de 5 años y más que hablan alguna lengua indígena y no hablan español..')
    # P5_HLI_HE = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población de 5 años y más que habla alguna lengua indígena y habla español',
    #                                         help_text='Personas de 5 años y más que hablan alguna lengua indígena y que hablan español..')
    # PHOG_IND = models.PositiveIntegerField(null=True,
    #                                        blank=True,
    #                                        verbose_name='Población en hogares censales indígenas',
    #                                        help_text='Total de personas que forman hogares censales donde el jefe del hogar o su cónyuge hablan alguna lengua indígena.')
    # #Discapacidad
    # PCON_LIM = models.PositiveIntegerField(null=True,
    #                                        blank=True,
    #                                        verbose_name='Población con limitación en la actividad',
    #                                        help_text='Personas que tienen dificultad para el desempeño y/o realización de tareas en la vida cotidiana.')
    # PCLIM_MOT = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población con limitación para caminar o moverse, subir o bajar',
    #                                         help_text='Personas con dificultad para caminar o moverse, subir o bajar.')
    # PCLIM_VIS = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población con limitación para ver, aún usando lentes',
    #                                         help_text='Personas con dificultad para ver, aún cuando usen lentes.')
    # PCLIM_LENG = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población con limitación para hablar, comunicarse o conversars',
    #                                          help_text='Personas con dificultad para comunicarse con los demás o que tienen '
    #                                                    'limitaciones para la recepción y producción de mensajes para hacerse '
    #                                                    'entender a través del lenguaje, signos y símbolos..')
    # PCLIM_AUD = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población con limitación para escuchar',
    #                                         help_text='Personas con dificultad para escuchar, aún usando aparato auditivo.')
    # PCLIM_MOT2 = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población con limitación para vestirse, bañarse o comer',
    #                                          help_text='Personas con dificultad para bañarse, vestirse y/o comer.')
    # PCLIM_MEN = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población con limitación para poner atención o aprender cosas sencillas',
    #                                         help_text='Personas con dificultad para mantener un nivel de atención en cosas sencillas.')
    # PCLIM_MEN2 = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población con limitación mental',
    #                                          help_text='Personas con dificultad o con alguna limitación mental.')
    # PSIN_LIM = models.PositiveIntegerField(null=True,
    #                                        blank=True,
    #                                        verbose_name='Población sin limitación en la actividad',
    #                                        help_text='Personas que no tienen dificultad para el desempeño y/o realización de tareas en la vida cotidiana.')
    # #Características educativas
    # P3A5_NOA = models.PositiveIntegerField(null=True,
    #                                        blank=True,
    #                                        verbose_name='Población de 3 a 5 años que no asiste a la escuela',
    #                                        help_text='Personas de 3 a 5 años de edad que no van a la escuela.')
    # P3A5_NOA_M = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población masculina de 3 a 5 años que no asiste a la escuela',
    #                                          help_text='Hombres de 3 a 5 años de edad que no van a la escuela.')
    # P3A5_NOA_F = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población femenina de 3 a 5 años que no asiste a la escuela',
    #                                          help_text='Mujeres de 3 a 5 años de edad que no van a la escuela.')
    # P6A11_NOA = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población de 6 a 11 años que no asiste a la escuela',
    #                                         help_text='Personas de 6 a 11 años de edad que no van a la escuela.')
    # P6A11_NOAM = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población masculina de 6 a 11 años que no asiste a la escuela',
    #                                          help_text='Hombres de 6 a 11 años de edad que no van a la escuela.')
    # P6A11_NOAF = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población femenina de 6 a 11 años que no asiste a la escuela',
    #                                          help_text='Mujeres de 6 a 11 años de edad que no van a la escuela.')
    # P12A14NOA = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población de 12 a 14 años que no asiste a la escuela',
    #                                         help_text='Personas de 12 a 14 años de edad que no van a la escuela.')
    # P12A14NOAM = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población masculina de 12 a 14 años que no asiste a la escuela',
    #                                          help_text='Hombres de 12 a 14 años de edad que no van a la escuela.')
    # P12A14NOAF = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población femenina de 12 a 14 años que no asiste a la escuela',
    #                                          help_text='Mujeres de 12 a 14 años de edad que no van a la escuela.')
    # P15A17A = models.PositiveIntegerField(null=True,
    #                                       blank=True,
    #                                       verbose_name='Población de 15 a 17 años que asiste a la escuela',
    #                                       help_text='Personas de 15 a 17 años de edad que van a la escuela.')
    # P15A17A_M = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población masculina de 15 a 17 años que asiste a la escuela',
    #                                         help_text='Hombres de 15 a 17 años de edad que van a la escuela.')
    # P15A17A_F = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población femenina de 15 a 17 años que asiste a la escuela',
    #                                         help_text='Mujeres de 15 a 17 años de edad que van a la escuela.')
    # P18A24A = models.PositiveIntegerField(null=True,
    #                                       blank=True,
    #                                       verbose_name='Población de 18 a 24 años que asiste a la escuela',
    #                                       help_text='Personas de 18 a 24 años de edad que van a la escuela.')
    # P18A24A_M = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población masculina de 18 a 24 años que asiste a la escuela',
    #                                         help_text='Hombres de 18 a 24 años de edad que van a la escuela.')
    # P18A24A_F = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población femenina de 18 a 24 años que asiste a la escuela',
    #                                         help_text='Mujeres de 18 a 24 años de edad que van a la escuela.')
    # P8A14AN = models.PositiveIntegerField(null=True,
    #                                       blank=True,
    #                                       verbose_name='Población de 8 a 14 años que no saben leer y escribir',
    #                                       help_text='Personas de 8 a 14 años de edad que no saben leer y escribir.')
    # P8A14AN_M = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población mascuina de 8 a 14 años que no saben leer y escribir',
    #                                         help_text='Hombres de 8 a 14 años de edad que no saben leer y escribir.')
    # P8A14AN_F = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población femenina de 8 a 14 años que no saben leer y escribir',
    #                                         help_text='Mujeres de 8 a 14 años de edad que no saben leer y escribir.')
    # P15YM_AN = models.PositiveIntegerField(null=True,
    #                                        blank=True,
    #                                        verbose_name='Población de 15 años y más analfabeta',
    #                                        help_text='Personas de 15 a 130 años de edad que no saben leer ni escribir.')
    # P15YM_AN_M = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población masculina de 15 años y más analfabeta',
    #                                          help_text='Hombres de 15 a 130 años de edad que no saben leer ni escribir.')
    # P15YM_AN_F = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población femenina de 15 años y más analfabeta',
    #                                          help_text='Mujeres de 15 a 130 años de edad que no saben leer ni escribir.')
    # P15YM_SE = models.PositiveIntegerField(null=True,
    #                                        blank=True,
    #                                        verbose_name='Población de 15 años y más sin escolaridad',
    #                                        help_text='Personas de 15 a 130 años de edad que no aprobaron ningún grado de escolaridad o que solo tienen nivel preescolar')
    # P15YM_SE_M = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población masculina de 15 años y más sin escolaridad',
    #                                          help_text='Hombres de 15 a 130 años de edad que no aprobaron ningún grado de escolaridad o que solo tienen nivel preescolar')
    # P15YM_SE_F = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población femenina de 15 años y más sin escolaridad',
    #                                          help_text='Mujeres de 15 a 130 años de edad que no aprobaron ningún grado de escolaridad o que solo tienen nivel preescolar')
    # P15PRI_IN = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población de 15 años y más con primaria incompleta',
    #                                         help_text='Personas de 15 a 130 años de edad que tienen como máxima '
    #                                                   'escolaridad hasta el quinto grado aprobado en primaria. '
    #                                                   'Incluye a las personas que no especificaron los grados '
    #                                                   'aprobados en el nivel señalado.')
    # P15PRI_INM = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población masculina de 15 años y más con primaria incompleta',
    #                                          help_text='Hombres de 15 a 130 años de edad que tienen como máxima '
    #                                                    'escolaridad hasta el quinto grado aprobado en primaria. '
    #                                                    'Incluye a las personas que no especificaron los grados '
    #                                                    'aprobados en el nivel señalado.')
    # P15PRI_INF = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población femenina de 15 años y más con primaria incompleta',
    #                                          help_text='Mujeres de 15 a 130 años de edad que tienen como máxima '
    #                                                    'escolaridad hasta el quinto grado aprobado en primaria. '
    #                                                    'Incluye a las personas que no especificaron los grados '
    #                                                    'aprobados en el nivel señalado.')
    # P15PRI_CO = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población de 15 años y más con primaria completa',
    #                                         help_text='Personas de 15 a 130 años de edad que tienen como máxima escolaridad 6 grados aprobados en primaria.')
    # P15PRI_COM = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población masculina de 15 años y más con primaria completa',
    #                                          help_text='Hombres de 15 a 130 años de edad que tienen como máxima escolaridad 6 grados aprobados en primaria.')
    # P15PRI_COF = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población femenina de 15 años y más con primaria completa',
    #                                          help_text='Mujeres de 15 a 130 años de edad que tienen como máxima escolaridad 6 grados aprobados en primaria.')
    # P15SEC_IN = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población de 15 años y más con secundaria incompleta',
    #                                         help_text='Personas de 15 a 130 años de edad que tienen como máxima '
    #                                                   'escolaridad hasta segundo grado aprobado de secundaria. '
    #                                                   'Incluye a las personas que no especificaron los grados '
    #                                                   'aprobados en el nivel señalado.')
    # P15SEC_INM = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población masculina de 15 años y más con secundaria incompleta',
    #                                          help_text='Hombres de 15 a 130 años de edad que tienen como máxima '
    #                                                    'escolaridad hasta segundo grado aprobado de secundaria. '
    #                                                    'Incluye a las personas que no especificaron los grados '
    #                                                    'aprobados en el nivel señalado.')
    # P15SEC_INF = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población femenina de 15 años y más con secundaria incompleta',
    #                                          help_text='Mujeres de 15 a 130 años de edad que tienen como máxima '
    #                                                    'escolaridad hasta segundo grado aprobado de secundaria. '
    #                                                    'Incluye a las personas que no especificaron los grados '
    #                                                    'aprobados en el nivel señalado.')
    # P15SEC_CO = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población de 15 años y más con secundaria completa',
    #                                         help_text='Personas de 15 a 130 años de edad que tienen como máxima escolaridad 3 grados aprobados en secundaria.')
    # P15SEC_COM = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población masculina de 15 años y más con secundaria completa',
    #                                          help_text='Hombres de 15 a 130 años de edad que tienen como máxima escolaridad 3 grados aprobados en secundaria.')
    # P15SEC_COF = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población femenina de 15 años y más con secundaria completa',
    #                                          help_text='Mujeres de 15 a 130 años de edad que tienen como máxima escolaridad 3 grados aprobados en secundaria.')
    # P18YM_PB = models.PositiveIntegerField(null=True,
    #                                        blank=True,
    #                                        verbose_name='Población de 18 años y más con educación pos-básica',
    #                                        help_text='Personas de 18 a 130 años de edad que tienen como máxima '
    #                                                  'escolaridad algún grado aprobado en: preparatoria ó bachillerato; '
    #                                                  'normal básica, estudios técnicos o comerciales con secundaria terminada; '
    #                                                  'estudios técnicos o comerciales con preparatoria terminada; '
    #                                                  'normal de licenciatura; licenciatura o profesional; maestría o doctorado. '
    #                                                  'Incluye a las personas que no especificaron los grados aprobados en los niveles señalados.')
    # P18YM_PB_M = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población masculina de 18 años y más con educación pos-básica',
    #                                          help_text='Hombres de 18 a 130 años de edad que tienen como máxima '
    #                                                    'escolaridad algún grado aprobado en: preparatoria ó bachillerato; '
    #                                                    'normal básica, estudios técnicos o comerciales con secundaria terminada; '
    #                                                    'estudios técnicos o comerciales con preparatoria terminada; '
    #                                                    'normal de licenciatura; licenciatura o profesional; maestría o doctorado. '
    #                                                    'Incluye a las personas que no especificaron los grados aprobados en los niveles señalados.')
    # P18YM_PB_F = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población femenina de 18 años y más con educación pos-básica',
    #                                          help_text='Mujeres de 18 a 130 años de edad que tienen como máxima '
    #                                                    'escolaridad algún grado aprobado en: preparatoria ó bachillerato; '
    #                                                    'normal básica, estudios técnicos o comerciales con secundaria terminada; '
    #                                                    'estudios técnicos o comerciales con preparatoria terminada; '
    #                                                    'normal de licenciatura; licenciatura o profesional; maestría o doctorado. '
    #                                                    'Incluye a las personas que no especificaron los grados aprobados en los niveles señalados.')
    # GRAPROES = models.PositiveIntegerField(null=True,
    #                                        blank=True,
    #                                        verbose_name='Grado promedio de escolaridad',
    #                                        help_text='Resultado de dividir el monto de grados escolares aprobados '
    #                                                  'por las personas de 15 a 130 años de edad entre las personas '
    #                                                  'del mismo grupo de edad. Excluye a las personas que no especificaron los grados aprobados.')
    # GRAPROES_M = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Grado promedio de escolaridad de la población masculina',
    #                                          help_text='Resultado de dividir el monto de grados escolares aprobados '
    #                                                    'por las personas de 15 a 130 años de edad entre los hombres '
    #                                                    'del mismo grupo de edad. Excluye a las personas que no especificaron los grados aprobados.')
    # GRAPROES_F = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Grado promedio de escolaridad de la población femenina',
    #                                          help_text='Resultado de dividir el monto de grados escolares aprobados '
    #                                                    'por las personas de 15 a 130 años de edad entre las mujeres '
    #                                                    'del mismo grupo de edad. Excluye a las personas que no especificaron los grados aprobados.')
    # # Características económicas
    # PEA = models.PositiveIntegerField(null=True,
    #                                   blank=True,
    #                                   verbose_name='Población económicamente activa',
    #                                   help_text='Personas de 12 años y más que trabajaron; tenían trabajo pero no trabajaron o; '
    #                                             'buscaron trabajo en la semana de referencia.')
    # PEA_M = models.PositiveIntegerField(null=True,
    #                                     blank=True,
    #                                     verbose_name='Población masculina económicamente activa',
    #                                     help_text='Hombres de 12 años y más que trabajaron; tenían trabajo pero no trabajaron o; '
    #                                               'buscaron trabajo en la semana de referencia.')
    # PEA_F = models.PositiveIntegerField(null=True,
    #                                     blank=True,
    #                                     verbose_name='Población femenina económicamente activa',
    #                                     help_text='Mujeres de 12 años y más que trabajaron; tenían trabajo pero no trabajaron o; '
    #                                               'buscaron trabajo en la semana de referencia.')
    # PE_INAC = models.PositiveIntegerField(null=True,
    #                                       blank=True,
    #                                       verbose_name='Población no económicamente activa',
    #                                       help_text='Personas de 12 años y más pensionadas o jubiladas, estudiantes, dedicadas '
    #                                                 'a los quehaceres del hogar, que tienen alguna limitación física o mental '
    #                                                 'permanente que le impide trabajar.')
    # PE_INAC_M = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población masculina no económicamente activa',
    #                                         help_text='Hombres de 12 años y más pensionadas o jubiladas, estudiantes, dedicadas '
    #                                                   'a los quehaceres del hogar, que tienen alguna limitación física o mental '
    #                                                   'permanente que le impide trabajar.')
    # PE_INAC_F = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población femenina no económicamente activa',
    #                                         help_text='Mujeres de 12 años y más pensionadas o jubiladas, estudiantes, dedicadas '
    #                                                   'a los quehaceres del hogar, que tienen alguna limitación física o mental '
    #                                                   'permanente que le impide trabajar.')
    # POCUPADA = models.PositiveIntegerField(null=True,
    #                                        blank=True,
    #                                        verbose_name='Población ocupada',
    #                                        help_text='Personas de 12 a 130 años de edad que trabajaron o que no trabajaron '
    #                                                  'pero sí tenían trabajo en la semana de referencia.')
    # POCUPADA_M = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población masculina ocupada',
    #                                          help_text='Hombres de 12 a 130 años de edad que trabajaron o que no trabajaron '
    #                                                    'pero sí tenían trabajo en la semana de referencia.')
    # POCUPADA_F = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población femenina ocupada',
    #                                          help_text='Mujeres de 12 a 130 años de edad que trabajaron o que no trabajaron '
    #                                                    'pero sí tenían trabajo en la semana de referencia.')
    # PDESOCUP = models.PositiveIntegerField(null=True,
    #                                        blank=True,
    #                                        verbose_name='Población desocupada',
    #                                        help_text='Personas de 12 a 130 años de edad que no tenían trabajo, '
    #                                                  'pero buscaron trabajo en la semana de referencia.')
    # PDESOCUP_M = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población masculina desocupada',
    #                                          help_text='Hombres de 12 a 130 años de edad que no tenían trabajo, '
    #                                                    'pero buscaron trabajo en la semana de referencia.')
    # PDESOCUP_F = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población femenina desocupada',
    #                                          help_text='Mujeres de 12 a 130 años de edad que no tenían trabajo, '
    #                                                    'pero buscaron trabajo en la semana de referencia.')
    # #Servicios de salud
    # PSINDER = models.PositiveIntegerField(null=True,
    #                                       blank=True,
    #                                       verbose_name='Población sin derechohabiencia a servicios de salud',
    #                                       help_text='Total de personas que no tienen derecho a recibir servicios '
    #                                                 'médicos en ninguna institución pública o privada.')
    # PDER_SS = models.PositiveIntegerField(null=True,
    #                                       blank=True,
    #                                       verbose_name='Población derechohabiente a servicios de salud',
    #                                       help_text='Total de personas que tienen derecho a recibir servicios '
    #                                                 'médicos en alguna institución de salud pública o privada como: '
    #                                                 'el Instituto Mexicano del Seguro Social (IMSS), el Instituto de '
    #                                                 'Seguridad y Servicios Sociales de los Trabajadores del Estado '
    #                                                 '(ISSSTE e ISSSTE estatal), Petróleos Mexicanos (PEMEX), '
    #                                                 'la Secretaría de la Defensa Nacional (SEDENA) o la Secretaría de '
    #                                                 'Marina Armada de México (SEMAR), el Seguro Popular o para una '
    #                                                 'Nueva Generación (Incluye al Sistema de Protección Social en '
    #                                                 'Salud que coordina la Secretaría de Salud) o en otra.')
    # PDER_IMSS = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población derechohabiente del IMSS',
    #                                         help_text='Total de personas que tienen derecho a recibir servicios '
    #                                                   'médicos en el Instituto Mexicano del Seguro Social (IMSS).')
    # PDER_ISTE = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población derechohabiente del ISSSTE',
    #                                         help_text='Total de personas que tienen derecho a recibir servicios '
    #                                                   'médicos en el Instituto de Seguridad y Servicios Sociales '
    #                                                   'de los Trabajadores del Estado.')
    # PDER_ISTEE = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población derechohabiente del ISSSTE estatal',
    #                                          help_text='Total de personas que tienen derecho a recibir servicios '
    #                                                    'médicos en los institutos de seguridad social de los '
    #                                                    'estados (ISSSET, ISSSEMyM, ISSSTEZAC, ISSSPEA o ISSSTESON).')
    # PDER_SEGP = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población derechohabiente del seguro popular o Seguro Médico para una Nueva Generación',
    #                                         help_text='Total de personas que tienen derecho a recibir servicios '
    #                                                   'médicos en la Secretaría de Salud, mediante el Sistema de Protección '
    #                                                   'Social en Salud (Seguro Popular).')
    # #Situación conyugal
    # P12YM_SOLT = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población casada o unida de 12 años y más',
    #                                          help_text='Personas de 12 a 130 años de edad que viven con su pareja en unión libre; '
    #                                                    'casadas solo por el civil; casadas religiosamente o; casadas por el civil y religiosamente.')
    # P12YM_CASA = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población casada o unida de 12 años y más',
    #                                          help_text='Personas de 12 a 130 años de edad que viven con su pareja en unión libre; '
    #                                                    'casadas solo por el civil; casadas solo religiosamente o; casadas por el civil y religiosamente.')
    # P12YM_SEPA = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población que estuvo casada o unida de 12 años y más',
    #                                          help_text='Personas de 12 a 130 años de edad que están separadas, divorciadas o viudas.')
    # #Religión
    # PCATOLICA = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población con religión católica',
    #                                         help_text='Personas con religión católica.')
    # PNCATOLICA = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Protestantes, Evangélicas y Bíblicas diferentes de evangélicas',
    #                                          help_text='Personas con religiones Protestantes Históricas, '
    #                                                    'Pentecostales, Neopentecostales, Iglesia del Dios Vivo, '
    #                                                    'Columna y Apoyo de la Verdad, la Luz del Mundo, Cristianas, '
    #                                                    'Evangélicas y Bíblicas diferentes de las Evangélicas.')
    # POTRAS_REL = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población con otras religiones diferentes a las anteriores',
    #                                          help_text='Personas con religiones de Origen oriental, Judaico, Islámico, '
    #                                                    'New Age, Escuelas esotéricas, Raíces étnicas, Espiritualistas, '
    #                                                    'Ortodoxos, Otros movimientos religiosos y Cultos populares.')
    # PSIN_RELIG = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Población con otras religiones diferentes a las anteriores',
    #                                          help_text='Personas sin adscripción religiosa. Incluye ateísmo.')
    # #Hogares censales
    # TOTHOG = models.PositiveIntegerField(null=True,
    #                                      blank=True,
    #                                      verbose_name='Total de hogares censales',
    #                                      help_text='Hogares en viviendas particulares habitadas. '
    #                                                'Se considera un hogar en cada vivienda particular. '
    #                                                'Incluye casa independiente; departamento en edificio; '
    #                                                'vivienda en vecindad; vivienda en cuarto de azotea; '
    #                                                'local no construido para habitación; vivienda móvil; '
    #                                                'refugio o clase no especificada.')
    # HOGJEF_M = models.PositiveIntegerField(null=True,
    #                                        blank=True,
    #                                        verbose_name='Hogares censales con jefatura masculina',
    #                                        help_text='Hogares en viviendas particulares habitadas donde el jefe es hombre. '
    #                                                  'Se considera un hogar en cada vivienda particular. '
    #                                                  'Incluye casa independiente; departamento en edificio; '
    #                                                  'vivienda en vecindad; vivienda en cuarto de azotea; '
    #                                                  'local no construido para habitación; vivienda móvil; '
    #                                                  'refugio o clase no especificada.')
    # HOGJEF_F = models.PositiveIntegerField(null=True,
    #                                        blank=True,
    #                                        verbose_name='Hogares censales con jefatura femenina',
    #                                        help_text='Hogares en viviendas particulares habitadas donde el jefe es mujer. '
    #                                                  'Se considera un hogar en cada vivienda particular. '
    #                                                  'Incluye casa independiente; departamento en edificio; '
    #                                                  'vivienda en vecindad; vivienda en cuarto de azotea; '
    #                                                  'local no construido para habitación; vivienda móvil; '
    #                                                  'refugio o clase no especificada.')
    # POBHOG = models.PositiveIntegerField(null=True,
    #                                      blank=True,
    #                                      verbose_name='Población en hogares censales',
    #                                      help_text='Personas en hogares censales. Se considera un hogar en '
    #                                                'cada vivienda particular. Incluye casa independiente; '
    #                                                'departamento en edificio; vivienda en vecindad; vivienda '
    #                                                'en cuarto de azotea; local no construido para habitación; '
    #                                                'vivienda móvil; refugio o clase no especificada.')
    # PHOGJEF_M = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población en hogares censales con jefatura masculina',
    #                                         help_text='Personas en hogares censales donde el jefe es hombre. '
    #                                                   'Se considera un hogar en cada vivienda particular. '
    #                                                   'Incluye casa independiente; departamento en edificio; '
    #                                                   'vivienda en vecindad; vivienda en cuarto de azotea; '
    #                                                   'local no construido para habitación; vivienda móvil; '
    #                                                   'refugio o clase no especificada.')
    # PHOGJEF_F = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Población en hogares censales con jefatura femenina',
    #                                         help_text='Personas en hogares censales donde el jefe es mujer. '
    #                                                   'Se considera un hogar en cada vivienda particular. '
    #                                                   'Incluye casa independiente; departamento en edificio; '
    #                                                   'vivienda en vecindad; vivienda en cuarto de azotea; '
    #                                                   'local no construido para habitación; vivienda móvil; '
    #                                                   'refugio o clase no especificada.')
    # #Viviendas
    # VIVTOT = models.PositiveIntegerField(null=True,
    #                                      blank=True,
    #                                      verbose_name='Total de viviendas',
    #                                      help_text='Viviendas particulares habitadas, deshabitadas, '
    #                                                'de uso temporal y colectivas. Incluye a las viviendas '
    #                                                'particulares sin información de sus ocupantes.')
    # TVIVHAB = models.PositiveIntegerField(null=True,
    #                                       blank=True,
    #                                       verbose_name='Total de viviendas habitadas',
    #                                       help_text='Viviendas particulares y colectivas habitadas. '
    #                                                 'Incluye a las viviendas particulares sin '
    #                                                 'información de sus ocupantes.')
    # TVIVPAR = models.PositiveIntegerField(null=True,
    #                                       blank=True,
    #                                       verbose_name='Total de viviendas particulares',
    #                                       help_text='Viviendas particulares habitadas, '
    #                                                 'deshabitadas y de uso temporal. '
    #                                                 'Excluye a las viviendas particulares '
    #                                                 'sin información de ocupantes.')
    # VIVPAR_HAB = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Viviendas particulares habitadas',
    #                                          help_text='Viviendas particulares habitadas de cualquier clase: '
    #                                                    'casa independiente, departamento en edificio, vivienda '
    #                                                    'o cuarto en vecindad, vivienda o cuarto de azotea, '
    #                                                    'local no construido para habitación, vivienda móvil, '
    #                                                    'refugios o clase no especificada. Excluye a las viviendas '
    #                                                    'particulares sin información de ocupantes.')
    # TVIVPARHAB = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Total de viviendas particulares habitadas',
    #                                          help_text='Viviendas particulares habitadas de cualquier clase: '
    #                                                    'casa independiente, departamento en edificio, vivienda '
    #                                                    'o cuarto en vecindad, vivienda o cuarto de azotea, '
    #                                                    'local no construido para habitación, vivienda móvil, '
    #                                                    'refugios o clase no especificada. Incluye a las viviendas '
    #                                                    'particulares sin información de ocupantes.')
    # VIVPAR_DES = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Viviendas particulares deshabitadas',
    #                                          help_text='Viviendas particulares deshabitadas.')
    # VIVPAR_UT = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Viviendas particulares de uso temporal',
    #                                         help_text='Viviendas particulares de uso temporal.')
    # OCUPVIVPAR = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Ocupantes en viviendas particulares habitadas',
    #                                          help_text='Personas que residen en viviendas '
    #                                                    'particulares habitadas de cualquier clase: '
    #                                                    'casa independiente, departamento en edificio, '
    #                                                    'vivienda o cuarto en vecindad, vivienda o cuarto '
    #                                                    'de azotea, local no construido para habitación, '
    #                                                    'vivienda móvil, refugios o clase no especificada. '
    #                                                    'Excluye la estimación del número de personas en '
    #                                                    'viviendas particulares sin información de ocupantes.')
    # PROM_OCUP = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Promedio de ocupantes en viviendas particulares habitadas',
    #                                         help_text='Resultado de dividir el número de personas que residen '
    #                                                   'en viviendas particulares habitadas, entre el número '
    #                                                   'de esas viviendas. Excluye la estimación del número de '
    #                                                   'personas y de viviendas particulares sin información de ocupantes.')
    # PRO_OCUP_C = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Promedio de ocupantes por cuarto en viviendas particulares habitadas',
    #                                          help_text='Resultado de dividir el número de personas que residen '
    #                                                    'en viviendas particulares habitadas entre el número de '
    #                                                    'cuartos de esas viviendas. Comprende las viviendas '
    #                                                    'particulares para las que se captaron las características '
    #                                                    'de la vivienda, clasificadas como casa independiente, '
    #                                                    'departamento en edificio, vivienda o cuarto en vecindad '
    #                                                    'y vivienda o cuarto en azotea y a las que no '
    #                                                    'especificaron clase de vivienda.')
    # VPH_PISODT = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Viviendas particulares habitadas con piso de material diferente de tierra',
    #                                          help_text='Viviendas particulares habitadas con piso de cemento o firme, '
    #                                                    'madera, mosaico u otro material. Comprende las viviendas '
    #                                                    'particulares para las que se captaron las características '
    #                                                    'de la vivienda, clasificadas como casa independiente, '
    #                                                    'departamento en edificio, vivienda o cuarto en vecindad y '
    #                                                    'vivienda o cuarto en azotea y a las que no especificaron clase de vivienda.')
    # VPH_PISOTI = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Viviendas particulares habitadas con piso de tierra',
    #                                          help_text='Viviendas particulares habitadas con piso de tierra. '
    #                                                    'Comprende las viviendas particulares para las que se '
    #                                                    'captaron las características de la vivienda, clasificadas '
    #                                                    'como casa independiente, departamento en edificio, vivienda '
    #                                                    'o cuarto en vecindad y vivienda o cuarto en azotea y a las '
    #                                                    'que no especificaron clase de vivienda.')
    # VPH_1DOR = models.PositiveIntegerField(null=True,
    #                                        blank=True,
    #                                        verbose_name='Viviendas particulares habitadas con un dormitorio',
    #                                        help_text='Viviendas particulares habitadas donde sólo uno de '
    #                                                  'los cuartos se usa para dormir. Comprende las viviendas '
    #                                                  'particulares para las que se captaron las características '
    #                                                  'de la vivienda, clasificadas como casa independiente, '
    #                                                  'departamento en edificio, vivienda o cuarto en vecindad '
    #                                                  'y vivienda o cuarto en azotea y a las que no '
    #                                                  'especificaron clase de vivienda.')
    # VPH_2YMASD = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Viviendas particulares habitadas con dos dormitorios y más',
    #                                          help_text='Viviendas particulares habitadas que usan para dormir '
    #                                                    'entre 2 y 25 cuartos.Comprende las viviendas particulares '
    #                                                    'para las que se captaron las características de la vivienda, '
    #                                                    'clasificadas como casa independiente, departamento en edificio, '
    #                                                    'vivienda o cuarto en vecindad y vivienda o cuarto en azotea '
    #                                                    'y a las que no especificaron clase de vivienda.')
    # VPH_1CUART = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Viviendas particulares habitadas con un solo cuarto',
    #                                          help_text='Viviendas particulares habitadas que tienen un solo cuarto. '
    #                                                    'Comprende las viviendas particulares para las que se captaron '
    #                                                    'las características de la vivienda, clasificadas como casa '
    #                                                    'independiente, departamento en edificio, vivienda o cuarto '
    #                                                    'en vecindad y vivienda o cuarto en azotea y a las que no '
    #                                                    'especificaron clase de vivienda. Excluye la estimación '
    #                                                    'del número de personas y de viviendas particulares '
    #                                                    'sin información de ocupantes.')
    # VPH_2CUART = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Viviendas particulares habitadas con dos cuartos',
    #                                          help_text='Viviendas particulares habitadas que tienen dos cuartos. '
    #                                                    'Comprende las viviendas particulares para las que se '
    #                                                    'captaron las características de la vivienda, clasificadas '
    #                                                    'como casa independiente, departamento en edificio, vivienda '
    #                                                    'o cuarto en vecindad y vivienda o cuarto en azotea y a las '
    #                                                    'que no especificaron clase de vivienda. Excluye la '
    #                                                    'estimación del número de personas y de viviendas '
    #                                                    'particulares sin información de ocupantes.')
    # VPH_3YMASC = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Viviendas particulares habitadas con 3 cuartos y más',
    #                                          help_text='Viviendas particulares habitadas que tienen entre '
    #                                                    '3 y 25 cuartos. Comprende las viviendas particulares '
    #                                                    'para las que se captaron las características de la '
    #                                                    'vivienda, clasificadas como casa independiente, '
    #                                                    'departamento en edificio, vivienda o cuarto en '
    #                                                    'vecindad y vivienda o cuarto en azotea y a las '
    #                                                    'que no especificaron clase de vivienda.')
    # VPH_C_ELEC = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Viviendas particulares habitadas que disponen de luz eléctrica',
    #                                          help_text='Viviendas particulares habitadas que tienen luz eléctrica. '
    #                                                    'Comprende las viviendas particulares para las que se '
    #                                                    'captaron las características de la vivienda, clasificadas '
    #                                                    'como casa independiente, departamento en edificio, '
    #                                                    'vivienda o cuarto en vecindad y vivienda o cuarto en azotea '
    #                                                    'y a las que no especificaron clase de vivienda.')
    # VPH_S_ELEC = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Viviendas particulares habitadas que no disponen de luz eléctrica',
    #                                          help_text='Viviendas particulares habitadas que no tienen luz eléctrica. '
    #                                                    'Comprende las viviendas particulares para las que se captaron l'
    #                                                    'as características de la vivienda, clasificadas como casa '
    #                                                    'independiente, departamento en edificio, vivienda o cuarto '
    #                                                    'en vecindad y vivienda o cuarto en azotea y a las que no '
    #                                                    'especificaron clase de vivienda.')
    # VPH_AGUADV = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Viviendas particulares habitadas que disponen de agua entubada en el ámbito de la vivienda',
    #                                          help_text='Viviendas particulares habitadas que tienen disponibilidad '
    #                                                    'de agua entubada dentro de la vivienda, o fuera de la vivienda '
    #                                                    'pero dentro del terreno. Comprende las viviendas particulares '
    #                                                    'para las que se captaron las características de la vivienda, '
    #                                                    'clasificadas como casa independiente, departamento en edificio, '
    #                                                    'vivienda o cuarto en vecindad y vivienda o cuarto en azotea y '
    #                                                    'a las que no especificaron clase de vivienda.')
    # VPH_AGUAFV = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Viviendas particulares habitadas que no disponen de agua entubada en el ámbito de la vivienda',
    #                                          help_text='Viviendas particulares habitadas que tienen disponibilidad de '
    #                                                    'agua de una llave pública o hidrante, de otra vivienda, de pipa, '
    #                                                    'de pozo, río, arroyo, lago u otro. Comprende las viviendas particulares '
    #                                                    'para las que se captaron las características de la vivienda, '
    #                                                    'clasificadas como casa independiente, departamento en edificio, '
    #                                                    'vivienda o cuarto en vecindad y vivienda o cuarto en azotea y '
    #                                                    'a las que no especificaron clase de vivienda.')
    # VPH_EXCSA = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Viviendas particulares habitadas que disponen de excusado o sanitario',
    #                                         help_text='Viviendas particulares habitadas que tienen excusado, retrete, '
    #                                                   'sanitario, letrina u hoyo negro. Excluye la estimación del '
    #                                                   'número de personas y de viviendas particulares sin información de ocupantes.')
    # VPH_DRENAJ = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Viviendas particulares habitadas que disponen de drenaje',
    #                                          help_text='Viviendas particulares habitadas que tienen drenaje conectado '
    #                                                    'a la red pública, fosa séptica, barranca, grieta, río, lago o mar. '
    #                                                    'Comprende las viviendas particulares para las que se captaron '
    #                                                    'las características de la vivienda, clasificadas como casa '
    #                                                    'independiente, departamento en edificio, vivienda o cuarto en '
    #                                                    'vecindad y vivienda o cuarto en azotea y a las que no '
    #                                                    'especificaron clase de vivienda.')
    # VPH_NODREN = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Viviendas particulares habitadas que no disponen de drenaje',
    #                                          help_text='Viviendas particulares habitadas que no tienen drenaje. '
    #                                                    'Comprende las viviendas particulares para las que se '
    #                                                    'captaron las características de la vivienda, clasificadas '
    #                                                    'como casa independiente, departamento en edificio, vivienda '
    #                                                    'o cuarto en vecindad y vivienda o cuarto en azotea y a las '
    #                                                    'que no especificaron clase de vivienda.')
    # VPH_C_SERV = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Viviendas particulares habitadas que disponen de luz eléctrica, agua entubada de la red pública y drenaje',
    #                                          help_text='Viviendas particulares habitadas que tienen luz eléctrica, '
    #                                                    'agua entubada dentro o fuera de la vivienda, pero dentro del '
    #                                                    'terreno, así como drenaje. Comprende las viviendas particulares '
    #                                                    'para las que se captaron las características de la vivienda, '
    #                                                    'clasificadas como casa independiente, departamento en edificio, '
    #                                                    'vivienda o cuarto en vecindad y vivienda o cuarto en azotea y '
    #                                                    'a las que no especificaron clase de vivienda.')
    # VPH_SNBIEN = models.PositiveIntegerField(null=True,
    #                                          blank=True,
    #                                          verbose_name='Viviendas particulares habitadas sin ningún bien',
    #                                          help_text='Viviendas particulares habitadas que no disponen de radio, '
    #                                                    'televisión, refrigerador, lavadora, automóvil, computadora, '
    #                                                    'teléfono fijo, celular ni internet. Comprende las viviendas '
    #                                                    'particulares para las que se captaron las características de '
    #                                                    'la vivienda, clasificadas como casa independiente, departamento '
    #                                                    'en edificio, vivienda o cuarto en vecindad y vivienda o cuarto '
    #                                                    'en azotea y a las que no especificaron clase de vivienda.')
    # VPH_RADIO = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Viviendas particulares habitadas que disponen de radio',
    #                                         help_text='Viviendas particulares habitadas que tienen radio. '
    #                                                   'Comprende las viviendas particulares para las que se '
    #                                                   'captaron las características de la vivienda, clasificadas '
    #                                                   'como casa independiente, departamento en edificio, vivienda '
    #                                                   'o cuarto en vecindad y vivienda o cuarto en azotea y a  '
    #                                                   ' que no especificaron clase de vivienda.')
    # VPH_TV = models.PositiveIntegerField(null=True,
    #                                      blank=True,
    #                                      verbose_name='Viviendas particulares habitadas que disponen de televisor',
    #                                      help_text='Viviendas particulares habitadas que tienen televisor. '
    #                                                'Comprende las viviendas particulares para las que se '
    #                                                'captaron las características de la vivienda, clasificadas '
    #                                                'como casa independiente, departamento en edificio, vivienda '
    #                                                'o cuarto en vecindad y vivienda o cuarto en azotea y '
    #                                                'a las que no especificaron clase de vivienda.')
    # VPH_REFRI = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Viviendas particulares habitadas que disponen de refrigerador',
    #                                         help_text='Viviendas particulares habitadas que tienen refrigerador. '
    #                                                   'Comprende las viviendas particulares para las que se '
    #                                                   'captaron las características de la vivienda, clasificadas '
    #                                                   'como casa independiente, departamento en edificio, vivienda o '
    #                                                   'cuarto en vecindad y vivienda o cuarto en azotea y a las '
    #                                                   'que no especificaron clase de vivienda.')
    # VPH_LAVAD = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Viviendas particulares habitadas que disponen de lavadora',
    #                                         help_text='Viviendas particulares habitadas que tienen lavadora. '
    #                                                   'Comprende las viviendas particulares para las que se '
    #                                                   'captaron las características de la vivienda, clasificadas '
    #                                                   'como casa independiente, departamento en edificio, vivienda o '
    #                                                   'cuarto en vecindad y vivienda o cuarto en azotea y a las '
    #                                                   'que no especificaron clase de vivienda..')
    # VPH_AUTOM = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Viviendas particulares habitadas que disponen de automóvil o camioneta',
    #                                         help_text='Viviendas particulares habitadas que tienen automóvil o camioneta. '
    #                                                   'Comprende las viviendas particulares para las que se '
    #                                                   'captaron las características de la vivienda, clasificadas '
    #                                                   'como casa independiente, departamento en edificio, vivienda o '
    #                                                   'cuarto en vecindad y vivienda o cuarto en azotea y a las '
    #                                                   'que no especificaron clase de vivienda.')
    # VPH_PC = models.PositiveIntegerField(null=True,
    #                                      blank=True,
    #                                      verbose_name='Viviendas particulares habitadas que disponen de computadora',
    #                                      help_text='Viviendas particulares habitadas que tienen computadora. '
    #                                                'Comprende las viviendas particulares para las que se '
    #                                                'captaron las características de la vivienda, clasificadas '
    #                                                'como casa independiente, departamento en edificio, vivienda o '
    #                                                'cuarto en vecindad y vivienda o cuarto en azotea y a las '
    #                                                'que no especificaron clase de vivienda.')
    # VPH_TELEF = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Viviendas particulares habitadas que disponen de línea telefónica fija',
    #                                         help_text='Viviendas particulares habitadas que tienen línea telefónica fija. '
    #                                                   'Comprende las viviendas particulares para las que se '
    #                                                   'captaron las características de la vivienda, clasificadas '
    #                                                   'como casa independiente, departamento en edificio, vivienda o '
    #                                                   'cuarto en vecindad y vivienda o cuarto en azotea y a las '
    #                                                   'que no especificaron clase de vivienda.')
    # VPH_CEL = models.PositiveIntegerField(null=True,
    #                                       blank=True,
    #                                       verbose_name='Viviendas particulares habitadas que disponen de teléfono celular',
    #                                       help_text='Viviendas particulares habitadas que tienen teléfono celular. '
    #                                                 'Comprende las viviendas particulares para las que se '
    #                                                 'captaron las características de la vivienda, clasificadas '
    #                                                 'como casa independiente, departamento en edificio, vivienda o '
    #                                                 'cuarto en vecindad y vivienda o cuarto en azotea y a las '
    #                                                 'que no especificaron clase de vivienda.')
    # VPH_INTER = models.PositiveIntegerField(null=True,
    #                                         blank=True,
    #                                         verbose_name='Viviendas particulares habitadas que disponen de internet',
    #                                         help_text='Viviendas particulares habitadas que tienen servicio de internet. '
    #                                                   'Comprende ''las viviendas particulares para las que se '
    #                                                   'captaron las características de la vivienda, clasificadas '
    #                                                   'como casa independiente, departamento en edificio, vivienda o '
    #                                                   'cuarto en vecindad y vivienda o cuarto en azotea y a las '
    #                                                   'que no especificaron clase de vivienda.')
    class Meta:
        abstract = True


class Entidad(DivisionGeografica):
    cvegeo = models.CharField(max_length=2, primary_key=True)
    nomgeo = models.CharField(max_length=80)

    @property
    def contenido(self):
        return f'<p><strong>Nombre: </strong> {self.nomgeo} ' \
               f'</p><p><strong>Población total:</strong> {self.POBTOT} ' \
               f'</p><p><strong>Población masculina:</strong> {self.POBMAS} ' \
               f'</p> <p><strong>Población femenina:</strong> {self.POBFEM} </p>'

    def __str__(self):
        return self.nomgeo

    class Meta:
        ordering = ['nomgeo']


class Municipio(DivisionGeografica):
    cvegeo = models.CharField(max_length=5, primary_key=True)
    nomgeo = models.CharField(max_length=80)
    cve_mun = models.CharField(max_length=3)
    entidad = models.ForeignKey(Entidad, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nomgeo

    @property
    def contenido(self):
        return f'<p><strong>Nombre: </strong> {self.nomgeo} ' \
               f'<p><strong>Entidad: </strong> {str(self.entidad)} ' \
               f'</p><p><strong>Población total:</strong> {self.POBTOT} ' \
               f'</p><p><strong>Población masculina:</strong> {self.POBMAS} ' \
               f'</p> <p><strong>Población femenina:</strong> {self.POBFEM} </p>'

    def relaciona(self, created=False):
        if created:
            ent = Entidad.objects.get(cve_ent=self.cve_ent)
            ent.municipio_set.add(self)

    def save(self, *args, **kwargs):
        created = self.pk is None
        super(Municipio, self).save(*args, **kwargs)
        self.relaciona(created)

    class Meta:
        ordering = ['nomgeo']


class Localidad(DivisionGeografica):
    AMBITO_TIPO = (
        (0, 'No Aplica'),
        (1, 'Urbana'),
        (2, 'Rural')
        )
    cvegeo = models.CharField(max_length=9, primary_key=True)
    nomgeo = models.CharField(max_length=120)
    cve_mun = models.CharField(max_length=3)
    cve_loc = models.CharField(max_length=4)
    cve_ageb = models.CharField(max_length=4, null=True)
    ambito = models.PositiveSmallIntegerField(choices=AMBITO_TIPO, null=True)
    entidad = models.ForeignKey(Entidad,
                                on_delete=models.SET_NULL,
                                null=True)
    municipio = models.ForeignKey(Municipio,
                                  on_delete=models.SET_NULL,
                                  null=True)

    # ageb = models.ForeignKey('Ageb',
    #                          on_delete=models.SET_NULL,
    #                          null=True, related_name='loc_rurales')

    def __str__(self):
        return self.nomgeo

    @property
    def contenido(self):
        return f'<p><strong>Nombre: </strong> {self.nomgeo} ' \
               f'<p><strong>Entidad: </strong> {str(self.entidad)} ' \
               f'<p><strong>Municipio: </strong> {str(self.municipio)} ' \
               f'</p><p><strong>Población total:</strong> {self.POBTOT} ' \
               f'</p><p><strong>Población masculina:</strong> {self.POBMAS} ' \
               f'</p> <p><strong>Población femenina:</strong> {self.POBFEM} </p>'

    def relaciona(self, created=False):
        if created:
            ent = Entidad.objects.get(cve_ent=self.cve_ent)
            mun = ent.municipio_set.get(cve_mun=self.cve_mun)
            ent.localidad_set.add(self)
            mun.localidad_set.add(self)
            if self.cve_ageb:
                ageb = mun.ageb_set.get(cve_ageb=self.cve_ageb)
                ageb.manzana_set.add(self)

    def save(self, *args, **kwargs):
        created = self.pk is None
        # self.nomgeo = self.nomgeo.encode("latin-1").decode("utf-8")
        super(Localidad, self).save(*args, **kwargs)
        self.relaciona(created)

    class Meta:
        ordering = ['nomgeo']


# Ageb urbano Agebu
class Ageb(DivisionGeografica):
    AMBITO_TIPO = (
        (0, 'No Aplica'),
        (1, 'Urbana'),
        (2, 'Rural')
        )
    ambito = models.PositiveSmallIntegerField(blank=True,
                                              null=True,
                                              choices=AMBITO_TIPO)
    cvegeo = models.CharField(max_length=13, primary_key=True)
    cve_mun = models.CharField(max_length=3)
    cve_loc = models.CharField(max_length=4, null=True)
    cve_ageb = models.CharField(max_length=4)
    entidad = models.ForeignKey(Entidad,
                                on_delete=models.SET_NULL,
                                null=True)
    municipio = models.ForeignKey(Municipio,
                                  on_delete=models.SET_NULL,
                                  null=True)
    localidad = models.ForeignKey(Localidad,
                                  on_delete=models.SET_NULL,
                                  null=True, related_name="agebs")

    def __str__(self):
        return self.cve_ageb

    @property
    def contenido(self):
        return f'<p><strong>Nombre: </strong> {self.cve_ageb} ' \
               f'<p><strong>Tipo: </strong> Urbano ' \
               f'<p><strong>Entidad: </strong> {str(self.entidad)} ' \
               f'<p><strong>Municipio: </strong> {str(self.municipio)} ' \
               f'<p><strong>Localidad: </strong> {str(self.localidad)} ' \
               f'</p><p><strong>Población total:</strong> {self.POBTOT} ' \
               f'</p><p><strong>Población masculina:</strong> {self.POBMAS} ' \
               f'</p> <p><strong>Población femenina:</strong> {self.POBFEM} </p>'

    def relaciona(self, created=False):
        if created:
            ent = Entidad.objects.get(cve_ent=self.cve_ent)
            mun = ent.municipio_set.get(cve_mun=self.cve_mun)
            ent.ageb_set.add(self)
            mun.ageb_set.add(self)
            if self.cve_loc:
                loc = mun.localidad_set.get(cve_loc=self.cve_loc)
                loc.agebs.add(self)

    def save(self, *args, **kwargs):
        created = self.pk is None
        super(Ageb, self).save(*args, **kwargs)
        self.relaciona(created)


# Los ageb rurales no tienen localidad omg!
# class Agebr(DivisionGeografica):
#     cvegeo = models.CharField(max_length=9)
#     cve_mun = models.CharField(max_length=3)
#     cve_ageb = models.CharField(max_length=4)
#     entidad = models.ForeignKey(Entidad,
#                                 on_delete=models.SET_NULL,
#                                 null=True)
#     municipio = models.ForeignKey(Municipio,
#                                   on_delete=models.SET_NULL,
#                                   null=True)
#
#     def __str__(self):
#         return self.cve_ageb
#
#     @property
#     def contenido(self):
#         return f'<p><strong>Nombre: </strong> {self.cve_ageb} ' \
#             f'<p><strong>Tipo: </strong> Rural ' \
#             f'<p><strong>Entidad: </strong> {str(self.entidad)} ' \
#             f'<p><strong>Municipio: </strong> {str(self.municipio)} ' \
#             f'</p><p><strong>Población total:</strong> {self.POBTOT} ' \
#             f'</p><p><strong>Población masculina:</strong> {self.POBMAS} ' \
#             f'</p> <p><strong>Población femenina:</strong> {self.POBFEM} </p>'
#
#     def relaciona(self, created=False):
#         if created:
#             ent = Entidad.objects.get(cve_ent=self.cve_ent)
#             mun = ent.municipio_set.get(cve_mun=self.cve_mun)
#             ent.agebr_set.add(self)
#             mun.agebr_set.add(self)
#
#     def save(self, *args, **kwargs):
#         created = self.pk is None
#         super(Agebr, self).save(*args, **kwargs)
#         self.relaciona(created)
class LocalidadRural(DivisionGeografica):
    PLANO_TIPO = (
        (0, 'No'),
        (1, 'Si'),
        (2, 'Croquis')
        )
    geom = models.PointField(srid=4326)
    cvegeo = models.CharField(max_length=9, primary_key=True)
    nomgeo = models.CharField(max_length=120)
    cve_mun = models.CharField(max_length=3)
    cve_loc = models.CharField(max_length=4)
    cve_ageb = models.CharField(max_length=4, null=True)
    cve_mza = models.CharField(max_length=3, null=True)
    plano = models.PositiveSmallIntegerField(choices=PLANO_TIPO, null=True)
    entidad = models.ForeignKey(Entidad,
                                on_delete=models.SET_NULL,
                                null=True)
    municipio = models.ForeignKey(Municipio,
                                  on_delete=models.SET_NULL,
                                  null=True)
    ageb = models.ForeignKey(Ageb, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nomgeo

    @property
    def contenido(self):
        return f'<p><strong>Nombre: </strong> {self.nomgeo} ' \
               f'<p><strong>Entidad: </strong> {str(self.entidad)} ' \
               f'<p><strong>Municipio: </strong> {str(self.municipio)} ' \
               f'</p><p><strong>Población total:</strong> {self.POBTOT} ' \
               f'</p><p><strong>Población masculina:</strong> {self.POBMAS} ' \
               f'</p> <p><strong>Población femenina:</strong> {self.POBFEM} </p>'

    def relaciona(self, created=False):
        if created:
            ent = Entidad.objects.get(cve_ent=self.cve_ent)
            mun = ent.municipio_set.get(cve_mun=self.cve_mun)
            ageb = mun.ageb_set.get(cve_ageb=self.cve_ageb)
            ent.localidad_set.add(self)
            mun.localidad_set.add(self)
            ageb.localidadrural_set.add(self)

    def save(self, *args, **kwargs):
        created = self.pk is None
        # self.nomgeo = self.nomgeo.encode("latin-1").decode("utf-8")
        super(LocalidadRural, self).save(*args, **kwargs)
        self.relaciona(created)

    class Meta:
        ordering = ['nomgeo']


class Manzana(DivisionGeografica):
    # Definicion de elementos para campo de eleccion
    AMBITO_TIPO = (
        (0, 'No Aplica'),
        (1, 'Urbana'),
        (2, 'Rural')
        )

    MANZANA_TIPO = (
        (0, 'No Aplica'),
        (1, 'Típica'),
        (2, 'Atípica'),
        (3, 'Contenedora'),
        (4, 'Contenida'),
        (5, 'Económica'),
        (6, 'Edificio-Manzana'),
        (7, 'Glorieta'),
        (8, 'Parque o Jardín'),
        (9, 'Camellón'),
        (10, 'Bajo Puente')
        )
    # Definicion de elementos para campo de eleccion

    CONJHAB_TIPO = (
        (1, 'Conjunto habitacional'),
        (3, 'Manzana típica'),
        (9, 'Manzana no especificada')
        )

    RECUCALL_TIPO = (
        (1, 'Todas las vialidades'),
        (2, 'Alguna vialidad'),
        (3, 'Ninguna vialidad'),
        (4, 'No especificado'),
        (5, 'Conjunto habitacional')
        )

    BANQUETA_TIPO = (
        (1, 'Todas las vialidades'),
        (2, 'Alguna vialidad'),
        (3, 'Ninguna vialidad'),
        (4, 'No especificado'),
        (5, 'Conjunto habitacional')
        )

    GUARNICI_TIPO = (
        (1, 'Todas las vialidades'),
        (2, 'Alguna vialidad'),
        (3, 'Ninguna vialidad'),
        (4, 'No especificado'),
        (5, 'Conjunto habitacional')
        )

    ARBOLES_TIPO = (
        (1, 'Todas las vialidades'),
        (2, 'Alguna vialidad'),
        (3, 'Ninguna vialidad'),
        (4, 'No especificado'),
        (5, 'Conjunto habitacional')
        )

    RAMPAS_TIPO = (
        (1, 'Todas las vialidades'),
        (2, 'Alguna vialidad'),
        (3, 'Ninguna vialidad'),
        (4, 'No especificado'),
        (5, 'Conjunto habitacional')
        )

    ALUMPUB_TIPO = (
        (1, 'Todas las vialidades'),
        (2, 'Alguna vialidad'),
        (3, 'Ninguna vialidad'),
        (4, 'No especificado'),
        )

    SENALIZA_TIPO = (
        (1, 'Todas las vialidades'),
        (2, 'Alguna vialidad'),
        (3, 'Ninguna vialidad'),
        (4, 'No especificado'),
        (5, 'Conjunto habitacional')
        )

    TELPUB_TIPO = (
        (1, 'Todas las vialidades'),
        (2, 'Alguna vialidad'),
        (3, 'Ninguna vialidad'),
        (4, 'No especificado'),
        (5, 'Conjunto habitacional')
        )

    DRENAJEP_TIPO = (
        (1, 'Todas las vialidades'),
        (2, 'Alguna vialidad'),
        (3, 'Ninguna vialidad'),
        (4, 'No especificado'),
        (5, 'Conjunto habitacional')
        )

    TRANSCOL_TIPO = (
        (1, 'Todas las vialidades'),
        (2, 'Alguna vialidad'),
        (3, 'Ninguna vialidad'),
        (4, 'No especificado'),
        (5, 'Conjunto habitacional')
        )

    ACESOPER_TIPO = (
        (1, 'Libre en todas las vialidades'),
        (2, 'Restringido en alguna vialidad'),
        (3, 'Restringido en todas las vialidades'),
        (4, 'No especificado'),
        (5, 'Conjunto habitacional')
        )

    ACESOAUT_TIPO = (
        (1, 'Libre en todas las vialidades'),
        (2, 'Restringido en alguna vialidad'),
        (3, 'Restringido en todas las vialidades'),
        (4, 'No especificado'),
        (5, 'Conjunto habitacional')
        )

    PUESSEMI_TIPO = (
        (1, 'Todas las vialidades'),
        (2, 'Alguna vialidad'),
        (3, 'Ninguna vialidad'),
        (4, 'No especificado'),
        (5, 'Conjunto habitacional')
        )

    PUESAMBU_TIPO = (
        (1, 'Todas las vialidades'),
        (2, 'Alguna vialidad'),
        (3, 'Ninguna vialidad'),
        (4, 'No especificado'),
        (5, 'Conjunto habitacional')
        )

    CONJHAB = models.PositiveSmallIntegerField(blank=True,
                                               null=True,
                                               verbose_name='Tipo de manzana',
                                               help_text='Distinción de la '
                                                         'manzana según se '
                                                         'trate de un '
                                                         'edificio de un '
                                                         'conjunto '
                                                         'habitacional o de '
                                                         'una manzana típica',
                                               choices=CONJHAB_TIPO)
    RECUCALL = models.PositiveSmallIntegerField(blank=True,
                                                null=True,
                                                verbose_name='Disponibilidad '
                                                             'de pavimento',
                                                help_text='Categoría de la '
                                                          'manzana '
                                                          'según a '
                                                          'disponibilidad '
                                                          'de pavimento '
                                                          'en sus vialidades',
                                                choices=RECUCALL_TIPO)
    BANQUETA = models.PositiveSmallIntegerField(blank=True,
                                                null=True,
                                                verbose_name='Disponibilidad de '
                                                             'banqueta',
                                                help_text='categoría de la '
                                                          'manzana según se '
                                                          'la disponibilidad '
                                                          'de  '
                                                          'banqueta en sus '
                                                          'vialidades',
                                                choices=BANQUETA_TIPO)
    GUARNICI = models.PositiveSmallIntegerField(blank=True,
                                                null=True,
                                                verbose_name='Disponibilidad '
                                                             'de '
                                                             'guarnición',
                                                help_text='Categoría de la '
                                                          'manzana según la '
                                                          'disponibilidad de '
                                                          'guarnición'
                                                          'en sus vialidades',
                                                choices=GUARNICI_TIPO)
    ARBOLES = models.PositiveSmallIntegerField(blank=True,
                                               null=True,
                                               verbose_name='Disponibilidad de '
                                                            'planta de ornato',
                                               help_text='Categoría de la '
                                                         'manzana según la '
                                                         'diponibilidad de '
                                                         'árboles o plantas '
                                                         'de ornato en sus '
                                                         'vialidades',
                                               choices=ARBOLES_TIPO)
    RAMPAS = models.PositiveSmallIntegerField(blank=True,
                                              null=True,
                                              verbose_name='Disponibilidad de rampa para silla de ruedas',
                                              help_text='Categoría de la '
                                                        'manzana según la '
                                                        'diponibilidad de '
                                                        'rampa para silla de ruedas '
                                                        'en sus vialidades',
                                              choices=RAMPAS_TIPO)
    ALUMPUB = models.PositiveSmallIntegerField(blank=True,
                                               null=True,
                                               verbose_name='Disponibilidad de alumbrado público',
                                               help_text='Categoría de la '
                                                         'manzana según la '
                                                         'diponibilidad de '
                                                         'alumbrado público '
                                                         'en sus vialidades',
                                               choices=ALUMPUB_TIPO)
    SENALIZA = models.PositiveSmallIntegerField(blank=True,
                                                null=True,
                                                verbose_name='Disponibilidad de letrero con nombre de la calle',
                                                help_text='Categoría de la '
                                                          'manzana según la '
                                                          'diponibilidad de '
                                                          'letrero con nombre de la calle '
                                                          'en sus vialidades',
                                                choices=SENALIZA_TIPO)
    TELPUB = models.PositiveSmallIntegerField(blank=True,
                                              null=True,
                                              verbose_name='Disponibilidad de teléfono público',
                                              help_text='Categoría de la '
                                                        'manzana según la '
                                                        'diponibilidad de '
                                                        'teléfono público '
                                                        'en sus vialidades',
                                              choices=TELPUB_TIPO)
    DRENAJEP = models.PositiveSmallIntegerField(blank=True,
                                                null=True,
                                                verbose_name='Disponibilidad de drenaje pluvial',
                                                help_text='Categoría de la '
                                                          'manzana según la '
                                                          'diponibilidad de '
                                                          'drenaje pluvial '
                                                          'en sus vialidades',
                                                choices=DRENAJEP_TIPO)
    TRANSCOL = models.PositiveSmallIntegerField(blank=True,
                                                null=True,
                                                verbose_name='Disponibilidad de transporte colectivo',
                                                help_text='Categoría de la '
                                                          'manzana según la '
                                                          'presencia de '
                                                          'transporte colectivo '
                                                          'en sus vialidades',
                                                choices=TRANSCOL_TIPO)
    ACESOPER = models.PositiveSmallIntegerField(blank=True,
                                                null=True,
                                                verbose_name='Acceso de peatones',
                                                help_text='Categoría de la '
                                                          'manzana según el '
                                                          'acceso de peatones '
                                                          'en sus vialidades',
                                                choices=ACESOPER_TIPO)
    ACESOAUT = models.PositiveSmallIntegerField(blank=True,
                                                null=True,
                                                verbose_name='Acceso de automóviles',
                                                help_text='Categoría de la '
                                                          'manzana según el '
                                                          'acceso de automóviles '
                                                          'en sus vialidades',
                                                choices=ACESOAUT_TIPO)
    PUESSEMI = models.PositiveSmallIntegerField(blank=True,
                                                null=True,
                                                verbose_name='Presencia de comercio semifijo',
                                                help_text='Categoría de la '
                                                          'manzana según la '
                                                          'presencia de '
                                                          'comercio semifijo '
                                                          'en sus vialidades',
                                                choices=PUESSEMI_TIPO)
    PUESAMBU = models.PositiveSmallIntegerField(blank=True,
                                                null=True,
                                                verbose_name='Presencia de comercio ambulante',
                                                help_text='Categoría de la '
                                                          'manzana según la '
                                                          'presencia de '
                                                          'comercio ambulante '
                                                          'en sus vialidades',
                                                choices=PUESAMBU_TIPO)
    VIVTOT = models.PositiveSmallIntegerField(blank=True,
                                              null=True,
                                              verbose_name='Total de viviendas',
                                              help_text='Viviendas particulares habitadas, '
                                                        'deshabitadas, de uso temporal '
                                                        'y colectivas. Incluye a las viviendas '
                                                        'particulares sin información de '
                                                        'sus ocupantes')
    TVIVHAB = models.PositiveSmallIntegerField(blank=True,
                                               null=True,
                                               verbose_name='Total de viviendas habitadas',
                                               help_text='Viviendas particulares y colectivas habitadas, '
                                                         'deshabitadas, de uso temporal '
                                                         'y colectivas. Incluye a las viviendas '
                                                         'particulares sin información de '
                                                         'sus ocupantes')
    TVIVPARHAB = models.PositiveSmallIntegerField(blank=True,
                                                  null=True,
                                                  verbose_name='Total de viviendas particulares habitadas',
                                                  help_text='Viviendas particulares habitadas, '
                                                            'deshabitadas, de uso temporal '
                                                            'y colectivas. Incluye a las viviendas '
                                                            'particulares sin información de '
                                                            'sus ocupantes')
    VPH_DEPTO = models.PositiveSmallIntegerField(blank=True,
                                                 null=True,
                                                 verbose_name='Viviendas particulares en departamento en edificio',
                                                 help_text='Viviendas particulares '
                                                           'habitadas cuya clase es'
                                                           'departamento en edificio.')
    cvegeo = models.CharField(max_length=16, primary_key=True)
    cve_mun = models.CharField(max_length=3)
    cve_loc = models.CharField(max_length=4)
    cve_ageb = models.CharField(max_length=4)
    cve_mza = models.CharField(max_length=3)
    ambito = models.PositiveSmallIntegerField(choices=AMBITO_TIPO)
    tipomza = models.PositiveSmallIntegerField(choices=MANZANA_TIPO)
    entidad = models.ForeignKey(Entidad,
                                on_delete=models.SET_NULL,
                                null=True)
    municipio = models.ForeignKey(Municipio,
                                  on_delete=models.SET_NULL,
                                  null=True)
    localidad = models.ForeignKey(Localidad, on_delete=models.SET_NULL,
                                  null=True)
    ageb = models.ForeignKey(Ageb, on_delete=models.SET_NULL, null=True)

    # agebr = models.ForeignKey(Agebr, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.cve_mza

    @property
    def contenido(self):
        return f'<p><strong>Nombre: </strong> {self.cve_mza} ' \
               f'<p><strong>Tipo: </strong> {self.tipomza} ' \
               f'<p><strong>Entidad: </strong> {str(self.entidad)} ' \
               f'<p><strong>Municipio: </strong> {str(self.municipio)} ' \
               f'<p><strong>Localidad: </strong> {str(self.localidad)} ' \
               f'<p><strong>AGEB urbana: </strong> {str(self.agebu)} ' \
               f'<p><strong>AGEB rural: </strong> {str(self.agebr)} ' \
               f'</p><p><strong>Población total:</strong> {self.POBTOT} ' \
               f'</p><p><strong>Población masculina:</strong> {self.POBMAS} ' \
               f'</p> <p><strong>Población femenina:</strong> {self.POBFEM} </p>'

    def relaciona(self, created=False):
        if created:
            ent = Entidad.objects.get(cve_ent=self.cve_ent)
            mun = ent.municipio_set.get(cve_mun=self.cve_mun)
            loc = mun.localidad_set.get(cve_loc=self.cve_loc)
            ent.manzana_set.add(self)
            mun.manzana_set.add(self)
            loc.manzana_set.add(self)
            ageb = mun.ageb_set.get(cve_ageb=self.cve_ageb)
            ageb.manzana_set.add(self)

    def save(self, *args, **kwargs):
        created = self.pk is None
        super(Manzana, self).save(*args, **kwargs)
        self.relaciona(created)

# class Servicio(models.Model):
#
#     GEOGRAFICO_TIPO = (
#         (0, "Aeródromo Civil"),
#         (1, "Camellón"),
#         (2, "Cementerio"),
#         (3, "Centro Comercial"),
#         (4, "Centro de Asistencia Médica"),
#         (5, "Corriente de Agua"),
#         (6, "Cuerpo de Agua"),
#         (7, "Escuela"),
#         (8, "Estación de Transporte Terrestre"),
#         (9, "Infraestructura Urbana"),
#         (10, "Instalación Deportiva o Recreativa"),
#         (11, "Instalación Diversa"),
#         (12, "Instalación Gubernamental"),
#         (13, "Instalación Industrial"),
#         (14, "Instalación Portuaria"),
#         (15, "Instalación de Comunicación"),
#         (16, "Instalación de Servicios"),
#         (17, "Mercado"),
#         (18, "Pista de Aviación"),
#         (19, "Plaza"),
#         (20, "Pozo"),
#         (21, "Restricción de Paso a Peatones y/o Automóviles"),
#         (22, "Subestación Eléctrica"),
#         (23, "Tanque de Agua"),
#         (24, "Templo"),
#         (25, "Zona Arqueológica"),
#         )
#
#     CONDICION_TIPO = (
#         (0, "No Aplica"),
#         (1, "En Construcción"),
#         (2, "En Operación"),
#         (3, "Fuera de Uso"),
#         (4, "Intermitente"),
#         (5, "Perenne"),
#         )
#
#     AMBITO_TIPO = (
#         (0, 'No Aplica'),
#         (1, 'Urbana'),
#         (2, 'Rural')
#         )
#     SERVICIO_TIPO = (
#         (0, "No Aplica"),
#         (1, "Acuario"),
#         (2, "Aduana"),
#         (3, "Agua"),
#         (4, "Alberca Olímpica"),
#         (5, "Alumbrado Público"),
#         (6, "Antena de Microondas de Telefonía"),
#         (7, "Antena de Radio"),
#         (8, "Antena de Televisión"),
#         (9, "Área Deportiva o Recreativa"),
#         (10, "Áreas Verdes"),
#         (11, "Arroyo"),
#         (12, "Aserradero"),
#         (13, "Autódromo"),
#         (14, "Ayudantía"),
#         (15, "Balneario"),
#         (16, "Bordo"),
#         (17, "Caja de Agua"),
#         (18, "Camellón"),
#         (19, "Campo de Golf"),
#         (20, "Campo de Tiro"),
#         (21, "Cancha"),
#         (22, "Caseta"),
#         (23, "Cenote"),
#         (24, "Central de Autobuses"),
#         (25, "Central de Bomberos"),
#         (26, "Central de Policía"),
#         (27, "Centro de Abastos"),
#         (28, "Centro de Asistencia Social"),
#         (29, "Centro de Espectáculos"),
#         (30, "Centro de Investigación"),
#         (31, "Centro de Rehabilitación"),
#         (32, "Centro de Salud"),
#         (33, "Cine"),
#         (34, "Edificación Cultural"),
#         (35, "Estación de  Ferrocarril"),    # Hay un espacio medio raro aqui
#         (36, "Estación de Bomberos"),
#         (37, "Estación de Gas"),
#         (38, "Estación de Metrobus"),
#         (39, "Estación de Transporte Foráneo"),
#         (40, "Estación de Tren Ligero"),
#         (41, "Estación de Tren Metropolitano (Metro)"),
#         (42, "Estadio"),
#         (43, "Estanque"),
#         (44, "Faro"),
#         (45, "Galgódromo"),
#         (46, "Gas"),
#         (47, "Gasolinera"),
#         (48, "Glorieta"),
#         (49, "Hipódromo"),
#         (50, "Hospital"),
#         (51, "Instalación Terrestre de Telecomunicación"),
#         (52, "Internacional"),
#         (53, "Jardín"),
#         (54, "Lago"),
#         (55, "Laguna"),
#         (56, "Lienzo Charro"),
#         (57, "Malecón"),
#         (58, "Medio Superior"),
#         (59, "Mixto"),
#         (60, "Monumento Histórico"),
#         (61, "Monumento u Obelisco"),
#         (62, "Museo"),
#         (63, "Nacional"),
#         (64, "Observatorio Astronómico"),  # 'Observataorio Astronómico',
#         (65, "Palacio Municipal"),
#         (66, "Palacio de Gobierno"),
#         (67, "Parque"),
#         (68, "Pavimentada"),
#         (69, "Petróleo"),
#         (70, "Pirámide"),
#         (71, "Planta Automotriz"),
#         (72, "Planta Cementera"),
#         (73, "Planta Petroquímica"),
#         (74, "Planta de Tratamiento de Agua"),
#         (75, "Plaza de Toros"),
#         (76, "Preescolar"),
#         (77, "Presa"),
#         (78, "Primaria"),
#         (79, "Radiofaro o VOR (Very High Frecuency Omnidirectional Range)"),
#         (80, "Rampa para Silla de Ruedas"),
#         (81, "Reclusorio"),
#         (82, "Refinería"),
#         (83, "Relleno Sanitario"),
#         (84, "Rompeolas o Escollera"),
#         (85, "Río"),
#         (86, "Secundaria"),
#         (87, "Silo"),
#         (88, "Superior"),
#         (89, "Tanque Elevado"),
#         (90, "Teatro"),
#         (91, "Teléfono Público"),
#         (92, "Terracería"),
#         (93, "Torre de Microondas"),
#         (94, "Unidad Deportiva"),
#         (95, "Velódromo"),
#         (96, "Zoológico")
#         )
#
#     cvegeo = models.CharField(max_length=16)
#     cve_ent = models.CharField(max_length=2)
#     cve_mun = models.CharField(max_length=3)
#     cve_loc = models.CharField(max_length=4)
#     cve_ageb = models.CharField(max_length=4)
#     cve_mza = models.CharField(max_length=3)
#     condicion = models.PositiveSmallIntegerField(blank=True,
#                                                  null=True,
#                                                  choices=CONDICION_TIPO)
#     geografico = models.PositiveSmallIntegerField(blank=True,
#                                                   null=True,
#                                                   choices=GEOGRAFICO_TIPO)
#     nomserv = models.CharField(max_length=110)
#     area = models.CharField(max_length=255, blank=True, null=True)
#     tipo = models.PositiveSmallIntegerField(blank=True,
#                                             null=True,
#                                             choices=SERVICIO_TIPO)
#     cve_serv = models.PositiveSmallIntegerField(blank=True,
#                                                 null=True)
#     ambito = models.PositiveSmallIntegerField(blank=True,
#                                               null=True,
#                                               choices=AMBITO_TIPO)
#     geom = models.MultiPointField(srid=4326)
#
#     entidad = models.ForeignKey(Entidad,
#                                 on_delete=models.SET_NULL,
#                                 null=True)
#     municipio = models.ForeignKey(Municipio,
#                                   on_delete=models.SET_NULL,
#                                   null=True)
#     localidad = models.ForeignKey(Localidad, on_delete=models.SET_NULL,
#                                   null=True)
#     ageb = models. ForeignKey(Ageb, on_delete=models.SET_NULL, null=True)
#     manzana = models.ForeignKey(Manzana, on_delete=models.SET_NULL, null=True)
#
#     def relaciona(self, created=False):
#         if created:
#             ent = Entidad.objects.get(cve_ent=self.cve_ent)
#             mun = ent.municipio_set.get(cve_mun=self.cve_mun)
#             loc = mun.localidad_set.get(cve_loc=self.cve_loc)
#             ent.servicio_set.add(self)
#             mun.servicio_set.add(self)
#             loc.servicio_set.add(self)
#             if self.area:
#                 try:
#                     ageb = Ageb.objects.filter(geom__contained=self.geom)[0]
#                     ageb.servicio_set.add(self)
#                 except Ageb.DoesNotExist:
#                     pass
#             else:
#                 ageb = mun.ageb_set.get(cve_ageb=self.cve_ageb)
#                 mza = ageb.manzana_set.get(cve_mza=self.cve_mza)
#                 mza.servicio_set.add(self)
#
#     def save(self, *args, **kwargs):
#         created = self.pk is None
#         super(Servicio, self).save(*args, **kwargs)
#         self.relaciona(created)
