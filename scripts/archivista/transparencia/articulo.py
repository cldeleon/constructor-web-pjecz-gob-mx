import csv
from datetime import datetime
from transparencia.plantillas import env
from transparencia.fraccion import Fraccion


class Articulo(object):

    def __init__(self, entrada_csv, rama, pagina, titulo, resumen, etiquetas):
        self.rama = rama
        self.pagina = pagina
        self.titulo = titulo
        self.resumen = resumen
        self.etiquetas = etiquetas
        self.creado = self.modificado = datetime.today().isoformat(sep=' ', timespec='minutes')
        self.fracciones = []
        with open(entrada_csv) as puntero:
            lector = csv.DictReader(puntero)
            for renglon in lector:
                if renglon['rama'] == self.rama and int(renglon['ordinal']) > 0:
                    self.fracciones.append(Fraccion(
                        rama = renglon['rama'],
                        ordinal = int(renglon['ordinal']),
                        pagina = renglon['pagina'],
                        titulo = renglon['titulo'],
                        resumen = renglon['resumen'],
                        etiquetas = renglon['etiquetas'],
                        ))

    def destino(self):
        return(f'transparencia/{self.rama}/{self.rama}.md')

    def contenido(self):
        plantilla = env.get_template('articulo.md.jinja2')
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
        salida = []
        salida.append(f'{self.destino()}, {self.titulo}')
        for fraccion in self.fracciones:
            salida.append(str(fraccion))
        return('\n'.join(salida))
