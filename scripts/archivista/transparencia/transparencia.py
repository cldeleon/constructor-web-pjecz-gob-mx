import csv
import os
from datetime import datetime
from transparencia.articulo import Articulo
from transparencia.seccion import Seccion


class Transparencia(object):

    def __init__(self, insumos_ruta, salida_ruta, metadatos_csv, plantillas_env):
        self.insumos_ruta = insumos_ruta
        self.salida_ruta = salida_ruta
        self.metadatos_csv = metadatos_csv
        self.plantillas_env = plantillas_env
        self.titulo = 'Transparencia'
        self.resumen = 'Pendiente'
        self.etiquetas = 'Transparencia'
        self.creado = self.modificado = datetime.today().isoformat(sep=' ', timespec='minutes')
        self.secciones_comienzan_con = 'Transparencia'
        self.destino = 'transparencia/transparencia.md'
        self.insumos = []
        self.secciones = []
        self.articulos = []
        self.alimentado = False

    def alimentar(self):
        if self.alimentado == False:
            # Alimentar insumos
            with os.scandir(self.insumos_ruta) as scan:
                for item in scan:
                    if not item.name.startswith('.') and item.is_file():
                        self.insumos.append(item.name)
            self.insumos.sort()
            # Alimentar secciones
            for insumo in self.insumos:
                if insumo.endswith('.md') and insumo.startswith(self.secciones_comienzan_con):
                    self.secciones.append(Seccion(self.insumos_ruta, insumo))
            # Alimentar articulos
            alimentados = []
            with open(self.metadatos_csv) as puntero:
                lector = csv.DictReader(puntero)
                for renglon in lector:
                    if renglon['rama'] not in alimentados:
                        articulo = Articulo(
                            transparencia = self,
                            rama = renglon['rama'],
                            pagina = renglon['pagina'],
                            titulo = renglon['titulo'],
                            resumen = renglon['resumen'],
                            etiquetas = renglon['etiquetas'],
                            )
                        articulo.alimentar()
                        if len(articulo.secciones) > 0:
                            self.articulos.append(articulo)
                        alimentados.append(renglon['rama'])
            # Levantar bandera
            self.alimentado = True

    def contenido(self):
        if self.alimentado == False:
            self.alimentar()
        if len(self.secciones) > 0:
            introducciones = []
            for seccion in self.secciones:
                introducciones.append(seccion.contenido())
            introduccion = '\n'.join(introducciones)
        else:
            introduccion = '### Sin introducción'
        final = '### Sin final'
        plantilla = self.plantillas_env.get_template('transparencia.md.jinja2')
        return(plantilla.render(
            title = self.titulo,
            slug = 'transparencia',
            summary = self.resumen,
            tags = self.etiquetas,
            url = 'transparencia/',
            save_as = 'transparencia/index.html',
            date = self.creado,
            modified = self.modificado,
            introduccion = introduccion,
            articulos = self.articulos,
            final = final,
            ))

    def __repr__(self):
        if self.alimentado == False:
            self.alimentar()
        yo_mismo = []
        yo_mismo.append(f'  {self.titulo}:')
        if len(self.secciones) > 0:
            s = []
            for seccion in self.secciones:
                s.append(seccion.archivo_md)
            yo_mismo.append(', '.join(s))
        if len(self.insumos) > 0:
            yo_mismo.append('+' * len(self.insumos))
        salida = [' '.join(yo_mismo)]
        for articulo in self.articulos:
            if str(articulo) != '':
                salida.append(str(articulo))
        return('\n'.join(salida))
