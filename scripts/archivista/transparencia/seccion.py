import os


class Seccion(object):
    """ Sección de una página """

    def __init__(self, encabezado='', markdown=''):
        self.encabezado = encabezado
        self.archivo_md = None
        self.markdown = markdown
        self.cargado = False

    def cargar(self, insumos_ruta, archivo_md):
        self.archivo_md = archivo_md
        archivo = f'{insumos_ruta}/{self.archivo_md}'
        if os.path.exists(archivo):
            with open(archivo, 'r') as f:
                self.markdown = f.read()
        self.cargado = True

    def contenido(self):
        if self.markdown == '' and self.cargado == False:
            return('### Sin contenido')
        elif self.encabezado != '':
            return(f'### {self.encabezado}\n\n{self.markdown}\n')
        else:
            return(self.markdown)

    def __repr__(self):
        if self.markdown == '' and self.cargado == False:
            return('<Sección> sin contenido')
        else:
            return(f'<Sección> {self.archivo_md}')
