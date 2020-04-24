import os


class Seccion(object):
    """ Sección de una página """

    def __init__(self, encabezado='', markdown=''):
        self.encabezado = encabezado
        self.archivo_md = None
        self.markdown = markdown
        self.descargables = []
        if self.markdown == '':
            self.cargado = False
        else:
            self.cargado = True

    def agregar_descargable(self, insumo):
        self.descargables.append(insumo)
        self.cargado = True

    def cargar(self, insumos_ruta, archivo_md):
        """ Cargar el contenido de un archivo markdown """
        self.archivo_md = archivo_md
        archivo = f'{insumos_ruta}/{self.archivo_md}'
        if os.path.exists(archivo):
            with open(archivo, 'r') as f:
                self.markdown = f.read()
        self.cargado = True

    def contenido(self):
        """ Entregar el contenido markdown de esta sección """
        salida = []
        if self.cargado:
            if self.encabezado != '':
                salida.append(f'### {self.encabezado}\n\n')
            if self.markdown != '':
                salida.append(f'{self.markdown}\n\n')
            if len(self.descargables) > 0:
                listado = []
                for descargable in self.descargables:
                    listado.append(f'* [{descargable}]({descargable})')
                #salida.append(f'### Descargar\n')
                salida.append('\n'.join(listado))
                salida.append('\n')
            return('\n'.join(salida))
        else:
            return('### Sin contenido')

    def __repr__(self):
        if self.cargado:
            mensajes = []
            if self.archivo_md:
                mensajes.append(self.archivo_md)
            elif self.markdown != '':
                mensajes.append('+md+')
            if len(self.descargables) > 0:
                mensajes.append('(' + ') ('.join(self.descargables) + ')')
            if self.encabezado != '':
                return(f'<Seccion> "{self.encabezado}" ' + ', '.join(mensajes))
            else:
                return('<Seccion> ' + ', '.join(mensajes))
        else:
            return('<Seccion> No cargada')
