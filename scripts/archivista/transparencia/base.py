import os
from transparencia.seccion import Seccion


def scantree(path):
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path)
        else:
            yield entry


class Base(object):
    """ Base contiene código para Transparencia, Artículo y Fracción """

    def __init__(self, insumos_ruta, secciones_comienzan_con):
        self.insumos_ruta = insumos_ruta
        self.secciones_comienzan_con = secciones_comienzan_con
        self.insumos = []
        self.secciones = []
        self.secciones_iniciales = []
        self.secciones_intermedias = []
        self.secciones_finales = []
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
            # Seccones iniciales: archivos makdown cuyo nombre secciones_comienzan_con
            for insumo in self.insumos:
                if insumo.endswith('.md') and insumo.startswith(self.secciones_comienzan_con):
                    seccion = Seccion()
                    seccion.cargar(self.insumos_ruta, insumo)
                    self.secciones_iniciales.append(seccion)
            # Secciones intermedias: descargables
            descargas = Seccion()
            for insumo in self.insumos:
                # Es archivo
                if insumo.endswith('.pdf') or insumo.endswith('.ppt') or insumo.endswith('.pptx') or insumo.endswith('.xls') or insumo.endswith('.xlsx'):
                    descargas.agregar_descargable(insumo)
                # Es directorio
                if False:
                    pass
            if descargas.cargado:
                self.secciones_intermedias.append(descargas)
            # Secciones finales: archivos makdown cuyo nombre NO secciones_comienzan_con
            for insumo in self.insumos:
                if insumo.endswith('.md') and not insumo.startswith(self.secciones_comienzan_con):
                    seccion = Seccion()
                    seccion.cargar(self.insumos_ruta, insumo)
                    self.secciones_finales.append(seccion)

    def contenido(self):
        if self.alimentado == False:
            self.alimentar()

    def __repr__(self):
        if self.alimentado == False:
            self.alimentar()
        return('<Base>')
