import os
from transparencia.seccion import Seccion


class Base(object):
    """ Base contiene código para Transparencia, Artículo y Fracción """

    def __init__(self, insumos_ruta, secciones_comienzan_con):
        self.insumos_ruta = insumos_ruta
        self.secciones_comienzan_con = secciones_comienzan_con
        self.secciones = []
        self.secciones_iniciales = []
        self.secciones_intermedias = []
        self.secciones_finales = []
        self.alimentado = False
        self.contenido_intro = ''
        self.contenido_final = ''
        self.alimentar_insumos_en_subdirectorios = False

    def obtener_archivos_markdown_iniciales(self, ruta):
        archivos_markdown = []
        if os.path.exists(ruta):
            with os.scandir(ruta) as scan:
                for item in scan:
                    if not item.name.startswith('.') and item.is_file():
                        if item.name.endswith('.md') and item.name.startswith(self.secciones_comienzan_con):
                            archivos_markdown.append(item.path)
                archivos_markdown.sort()
        return(archivos_markdown)

    def obtener_archivos_descargables(self, ruta):
        archivos_descargables = []
        if os.path.exists(ruta):
            with os.scandir(ruta) as scan:
                for item in scan:
                    if not item.name.startswith('.') and item.is_file():
                        if item.name.endswith('.pdf') or item.name.endswith('.ppt') or item.name.endswith('.pptx') or item.name.endswith('.xls') or item.name.endswith('.xlsx'):
                            archivos_descargables.append(item.path)
                archivos_descargables.sort()
        return(archivos_descargables)

    def obtener_directorios(self, ruta):
        directorios = []
        if os.path.exists(ruta):
            with os.scandir(ruta) as scan:
                for item in scan:
                    if not item.name.startswith('.') and item.is_dir():
                        directorios.append(item.path)
                directorios.sort()
        return(directorios)

    def obtener_archivos_markdown_finales(self, ruta):
        archivos_markdown = []
        if os.path.exists(ruta):
            with os.scandir(ruta) as scan:
                for item in scan:
                    if not item.name.startswith('.') and item.is_file():
                        if item.name.endswith('.md') and not item.name.startswith(self.secciones_comienzan_con):
                            archivos_markdown.append(item.path)
                archivos_markdown.sort()
        return(archivos_markdown)

    def alimentar(self):
        if self.alimentado == False:
            # Secciones iniciales: archivos makdown cuyo nombre secciones_comienzan_con
            for archivo_markdown in self.obtener_archivos_markdown_iniciales(self.insumos_ruta):
                seccion = Seccion()
                seccion.cargar(archivo_markdown)
                if seccion.cargado:
                    self.secciones_iniciales.append(seccion)
            # Secciones intermedias: descargables
            seccion = Seccion(encabezado='Descargar')
            for archivo_descargable in self.obtener_archivos_descargables(self.insumos_ruta):
                seccion.agregar_descargable(archivo_descargable)
            if seccion.cargado:
                self.secciones_intermedias.append(seccion)
            # Secciones intermedias: obtener descargables en subdirectorios
            if self.alimentar_insumos_en_subdirectorios:
                for subdirectorio in self.obtener_directorios(self.insumos_ruta):
                    seccion = Seccion(encabezado=os.path.basename(subdirectorio))
                    for archivo_descargable in self.obtener_archivos_descargables(subdirectorio):
                        seccion.agregar_descargable(archivo_descargable)
                    if seccion.cargado:
                        self.secciones_intermedias.append(seccion)
            # Secciones finales: archivos makdown cuyo nombre NO secciones_comienzan_con
            for archivo_markdown in self.obtener_archivos_markdown_finales(self.insumos_ruta):
                seccion = Seccion()
                seccion.cargar(archivo_markdown)
                if seccion.cargado:
                    self.secciones_finales.append(seccion)

    def contenido(self):
        if self.alimentado == False:
            self.alimentar()

    def __repr__(self):
        if self.alimentado == False:
            self.alimentar()
        return('<Base>')
