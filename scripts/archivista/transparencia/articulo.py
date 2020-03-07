import csv
import os
from datetime import datetime
from transparencia.fraccion import Fraccion


class Articulo(object):

    def __init__(self, transparencia, rama, pagina, titulo, resumen, etiquetas):
        self.transparencia = transparencia
        self.rama = rama
        self.pagina = pagina
        self.titulo = titulo
        self.resumen = resumen
        self.etiquetas = etiquetas
        self.creado = self.modificado = datetime.today().isoformat(sep=' ', timespec='minutes')
        # Listar archivos con los contenidos y descargables
        self.insumos = []
        self.input_path = f'{self.transparencia.input_path}/{self.titulo}'
        if os.path.exists(self.input_path):
            with os.scandir(self.input_path) as scan:
                for item in scan:
                    if not item.name.startswith('.') and item.is_file():
                        self.insumos.append(item.name)
        self.insumos.sort()
        # Alimentar fracciones
        self.fracciones = []
        with open(transparencia.metadatos_csv) as puntero:
            lector = csv.DictReader(puntero)
            for renglon in lector:
                if renglon['rama'] == self.rama and int(renglon['ordinal']) > 0:
                    self.fracciones.append(Fraccion(
                        articulo = self,
                        rama = renglon['rama'],
                        ordinal = renglon['ordinal'],
                        pagina = renglon['pagina'],
                        titulo = renglon['titulo'],
                        resumen = renglon['resumen'],
                        etiquetas = renglon['etiquetas'],
                        ))

    def destino(self):
        return(f'transparencia/{self.rama}/{self.rama}.md')

    def contenido(self):
        plantilla = self.transparencia.plantillas_env.get_template('articulo.md.jinja2')
        return(plantilla.render(
            title = self.titulo,
            slug = f'transparencia-{self.rama}',
            summary = self.resumen,
            tags = self.etiquetas,
            url = f'transparencia/{self.rama}/',
            save_as = f'transparencia/{self.rama}/index.html',
            date = self.creado,
            modified = self.modificado,
            fracciones = self.fracciones,
            ))

    def __repr__(self):
        if len(self.insumos) > 0:
            salida = []
            salida.append('  {}: {}'.format(self.titulo, ', '.join(self.insumos)))
            for fraccion in self.fracciones:
                if str(fraccion) != '':
                    salida.append(str(fraccion))
            return('\n'.join(salida))
        else:
            return('')
