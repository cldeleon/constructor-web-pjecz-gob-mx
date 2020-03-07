import csv
import os
from datetime import datetime
from transparencia.articulo import Articulo


class Transparencia(object):

    def __init__(self, input_path, output_path, metadatos_csv, plantillas_env):
        self.input_path = input_path
        self.output_path = output_path
        self.metadatos_csv = metadatos_csv
        self.plantillas_env = plantillas_env
        self.titulo = 'Transparencia'
        self.resumen = 'Pendiente'
        self.etiquetas = 'Transparencia'
        self.creado = self.modificado = datetime.today().isoformat(sep=' ', timespec='minutes')
        # Listar archivos con los contenidos y descargables
        self.insumos = []
        with os.scandir(self.input_path) as scan:
            for item in scan:
                if not item.name.startswith('.') and item.is_file():
                    self.insumos.append(item.name)
        self.insumos.sort()
        # Alimentar articulos
        self.articulos = []
        alimentados = []
        with open(self.metadatos_csv) as puntero:
            lector = csv.DictReader(puntero)
            for renglon in lector:
                if renglon['rama'] not in alimentados:
                    self.articulos.append(Articulo(
                        transparencia = self,
                        rama = renglon['rama'],
                        pagina = renglon['pagina'],
                        titulo = renglon['titulo'],
                        resumen = renglon['resumen'],
                        etiquetas = renglon['etiquetas'],
                        ))
                    alimentados.append(renglon['rama'])

    def destino(self):
        return('transparencia/transparencia.md')

    def contenido(self):
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
            articulos = self.articulos,
            ))

    def __repr__(self):
        if len(self.insumos) > 0:
            salida = []
            salida.append('{}: {}'.format(self.titulo, ', '.join(self.insumos)))
            for articulo in self.articulos:
                if str(articulo) != '':
                    salida.append(str(articulo))
            return('\n'.join(salida))
        else:
            return('')
