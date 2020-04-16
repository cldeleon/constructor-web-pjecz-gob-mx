import os
from transparencia.seccion import Seccion


class Base(object):
    """ Base contiene código para Transparencia, Artículo y Fracción """

    def __init__(self, insumos_ruta, secciones_comienzan_con):
        self.insumos_ruta = insumos_ruta
        self.secciones_comienzan_con = secciones_comienzan_con
        self.insumos = []
        self.secciones = []
        self.alimentado = False
        self.contenido_intro = ''
        self.contenido_final = ''

    def alimentar(self):
        if self.alimentado == False:
            # Alimentar insumos
            if os.path.exists(self.insumos_ruta):
                with os.scandir(self.insumos_ruta) as scan:
                    for item in scan:
                        if not item.name.startswith('.') and item.is_file():
                            self.insumos.append(item.name)
            self.insumos.sort()
            # Alimentar secciones cuyo archivo comienza con
            for insumo in self.insumos:
                if insumo.endswith('.md') and insumo.startswith(self.secciones_comienzan_con):
                    seccion = Seccion()
                    seccion.cargar(self.insumos_ruta, insumo)
                    self.secciones.append(seccion)
            # Alimentar secciones cuyo archivo NO comienza con
            for insumo in self.insumos:
                if insumo.endswith('.md') and not insumo.startswith(self.secciones_comienzan_con):
                    seccion = Seccion()
                    seccion.cargar(self.insumos_ruta, insumo)
                    self.secciones.append(seccion)

    def contenido(self):
        if self.alimentado == False:
            self.alimentar()
        if len(self.secciones) == 0:
            self.secciones.append(Seccion(encabezado='No hay archivos markdown'))
