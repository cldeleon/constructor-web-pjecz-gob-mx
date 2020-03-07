import csv
import os
from datetime import datetime


class Fraccion(object):

    def __init__(self, articulo, rama, ordinal, pagina, titulo, resumen, etiquetas):
        self.articulo = articulo
        self.rama = rama
        self.ordinal = int(ordinal)
        self.pagina = pagina
        self.titulo = titulo
        self.resumen = resumen
        self.etiquetas = etiquetas
        # Listar archivos con los contenidos y descargables
        self.insumos = []
        self.input_path = '{}/F{} {}'.format(self.articulo.input_path, ordinal.zfill(2), self.titulo)
        if os.path.exists(self.input_path):
            with os.scandir(self.input_path) as scan:
                for item in scan:
                    if not item.name.startswith('.') and item.is_file():
                        self.insumos.append(item.name)
        self.insumos.sort()

    def destino(self):
        return(f'transparencia/{self.rama}/{self.pagina}/{self.pagina}.md')

    def contenido(self):
        plantilla = self.articulo.transparencia.plantillas_env.get_template('fraccion.md.jinja2')
        return(plantilla.render(
            title = self.titulo,
            slug = f'transparencia-{self.rama}-{self.pagina}',
            summary = self.resumen,
            tags = self.etiquetas,
            url = f'transparencia/{self.rama}/{self.pagina}/',
            save_as = f'transparencia/{self.rama}/{self.pagina}/index.html',
            date = self.creado,
            modified = self.modificado,
            descargables = [],
            ))

    def __repr__(self):
        if len(self.insumos) > 0:
            return('    {}: {}'.format(self.titulo, ', '.join(self.insumos)))
        else:
            return('')
