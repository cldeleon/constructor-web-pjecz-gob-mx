import os
from comun.descargable import Descargable


class Seccion(object):
    """ Sección de una página """

    def __init__(self, encabezado='', markdown='', nivel=2):
        self.encabezado = encabezado
        self.markdown = markdown
        self.nivel = nivel
        self.archivo_markdown_ruta = None
        self.descargables = []
        if self.markdown == '':
            self.cargado = False
        else:
            self.cargado = True

    def gatos(self):
        if self.nivel >=1 and self.nivel <= 6:
            return('#' * self.nivel)
        else:
            return('##')

    def agregar_descargable(self, archivo_ruta):
        """ Agregar la ruta a un archivo descargable """
        if os.path.exists(archivo_ruta) and os.path.isfile(archivo_ruta):
            self.descargables.append(Descargable(archivo_ruta))
            self.cargado = True
            if self.encabezado == '':
                self.encabezado = 'Descargar'

    def cargar(self, archivo_markdown_ruta):
        """ Cargar el contenido de un archivo markdown """
        self.archivo_markdown_ruta = archivo_markdown_ruta
        if os.path.exists(self.archivo_markdown_ruta) and os.path.isfile(self.archivo_markdown_ruta):
            with open(self.archivo_markdown_ruta, 'r') as f:
                self.markdown = f.read()
        self.cargado = True

    def contenido(self):
        """ Entregar el contenido markdown de esta sección """
        salida = []
        if self.encabezado != '':
            salida.append(f'{self.gatos()} {self.encabezado}\n\n')
        if self.cargado:
            if self.markdown != '':
                salida.append(f'{self.markdown}\n\n')
            if len(self.descargables) > 0:
                listado = []
                for descargable in self.descargables:
                    nombre = descargable.nombre()
                    vinculo = descargable.vinculo()
                    listado.append(f'* [{nombre}]({vinculo})')
                salida.append('\n'.join(listado))
                salida.append('\n')
        if len(salida) > 0:
            return('\n'.join(salida))
        else:
            return('\nSección sin contenido.\n')

    def __repr__(self):
        if self.cargado:
            mensajes = []
            if self.archivo_markdown_ruta != None:
                mensajes.append(os.path.basename(self.archivo_markdown_ruta))
            elif self.markdown != '':
                mensajes.append('+md+')
            if len(self.descargables) > 0:
                #vinculos = []
                #for descargable in self.descargables:
                #    vinculos.append(descargable.vinculo())
                nombres = []
                for descargable in self.descargables:
                    nombres.append(descargable.nombre())
                mensajes.append('(' + ') ('.join(nombres) + ')')
            if self.encabezado != '':
                return(f'<Seccion> {self.gatos()} {self.encabezado} ' + ', '.join(mensajes))
            else:
                return('<Seccion> ' + ', '.join(mensajes))
        else:
            if self.encabezado != '':
                return(f'<Seccion> {self.gatos()} {self.encabezado} ')
            else:
                return('<Seccion> SIN CONTENIDO')
