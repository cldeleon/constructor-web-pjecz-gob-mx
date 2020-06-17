import os
from comun.seccion import Seccion


class Base(object):
    """ Base contiene código para Transparencia, Artículo y Fracción """

    def __init__(self, insumos_ruta, secciones_comienzan_con):
        self.insumos_ruta = insumos_ruta
        self.secciones_comienzan_con = secciones_comienzan_con
        self.secciones = []
        self.secciones_iniciales = []
        self.secciones_intermedias = []
        self.secciones_finales = []
        self.imagenes = []
        self.alimentado = False
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
                        if item.name.endswith('.doc') or item.name.endswith('.docx') or item.name.endswith('.pdf') or item.name.endswith('.ppt') or item.name.endswith('.pptx') or item.name.endswith('.xls') or item.name.endswith('.xlsx') or item.name.endswith('.zip'):
                            archivos_descargables.append(item.path)
                archivos_descargables.sort()
        return(archivos_descargables)

    def obtener_archivos_imagenes(self, ruta):
        archivos_imagenes = []
        if os.path.exists(ruta):
            with os.scandir(ruta) as scan:
                for item in scan:
                    if not item.name.startswith('.') and item.is_file():
                        if item.name.endswith('.gif') or item.name.endswith('.jpg') or item.name.endswith('.jpeg') or item.name.endswith('.png') or item.name.endswith('.svg'):
                            archivos_imagenes.append(item.path)
                archivos_imagenes.sort()
        return(archivos_imagenes)

    def obtener_directorios(self, ruta):
        directorios = []
        if os.path.exists(ruta):
            with os.scandir(ruta) as scan:
                for item in scan:
                    if not item.name.startswith('.') and item.is_dir():
                        # Si tiene dentro un archivo nombre-directorio.md se omite
                        posible_md_archivo = os.path.basename(item.path) + '.md'
                        posible_md_ruta = f'{item.path}/{posible_md_archivo}'
                        if not os.path.exists(posible_md_ruta):
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
        if self.alimentado is False:
            # Secciones iniciales: archivos makdown cuyo nombre secciones_comienzan_con
            for archivo_markdown in self.obtener_archivos_markdown_iniciales(self.insumos_ruta):
                seccion = Seccion()
                seccion.cargar(archivo_markdown)
                if seccion.cargado:
                    self.secciones_iniciales.append(seccion)
            # Secciones intermedias: descargables
            seccion = Seccion()
            for archivo_descargable in self.obtener_archivos_descargables(self.insumos_ruta):
                seccion.agregar_descargable(archivo_descargable)
            if seccion.cargado:
                self.secciones_intermedias.append(seccion)
            # Secciones intermedias: obtener descargables en subdirectorios
            if self.alimentar_insumos_en_subdirectorios:
                # Nivel 3 tres gatos
                for subdirectorio3 in self.obtener_directorios(self.insumos_ruta):
                    seccion3 = Seccion(encabezado=os.path.basename(subdirectorio3), nivel=3)
                    for archivo_descargable in self.obtener_archivos_descargables(subdirectorio3):
                        seccion3.agregar_descargable(archivo_descargable)
                    self.secciones_intermedias.append(seccion3)
                    # Nivel 4 cuatro gatos
                    for subdirectorio4 in self.obtener_directorios(subdirectorio3):
                        seccion4 = Seccion(encabezado=os.path.basename(subdirectorio4), nivel=4)
                        for archivo_descargable in self.obtener_archivos_descargables(subdirectorio4):
                            seccion4.agregar_descargable(archivo_descargable)
                        self.secciones_intermedias.append(seccion4)
                        # Nivel 5 cinco gatos
                        for subdirectorio5 in self.obtener_directorios(subdirectorio4):
                            seccion5 = Seccion(encabezado=os.path.basename(subdirectorio5), nivel=5)
                            for archivo_descargable in self.obtener_archivos_descargables(subdirectorio5):
                                seccion5.agregar_descargable(archivo_descargable)
                            self.secciones_intermedias.append(seccion5)
            # Secciones finales: archivos makdown cuyo nombre NO secciones_comienzan_con
            for archivo_markdown in self.obtener_archivos_markdown_finales(self.insumos_ruta):
                seccion = Seccion()
                seccion.cargar(archivo_markdown)
                if seccion.cargado:
                    self.secciones_finales.append(seccion)
            # Imágenes
            self.imagenes = self.obtener_archivos_imagenes(self.insumos_ruta)

    def contenido(self):
        if self.alimentado is False:
            self.alimentar()

    def __repr__(self):
        if self.alimentado is False:
            self.alimentar()
        return('<Base>')
