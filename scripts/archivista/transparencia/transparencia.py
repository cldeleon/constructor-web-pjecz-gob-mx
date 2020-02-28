import csv
from datetime import datetime
from transparencia.plantillas import env
from transparencia.articulo import Articulo


class Transparencia(object):

    def __init__(self, entrada_csv):
        self.titulo = 'Transparencia'
        self.resumen = 'Pendiente'
        self.etiquetas = 'Transparencia'
        self.creado = self.modificado = datetime.today().isoformat(sep=' ', timespec='minutes')
        self.articulos = []
        alimentados = []
        with open(entrada_csv) as puntero:
            lector = csv.DictReader(puntero)
            for renglon in lector:
                if renglon['rama'] not in alimentados:
                    self.articulos.append(Articulo(
                        entrada_csv = entrada_csv,
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
        plantilla = env.get_template('transparencia.md.jinja2')
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
        salida = []
        salida.append(f'{self.destino()}, {self.titulo}')
        for articulo in self.articulos:
            salida.append(str(articulo))
        return('\n'.join(salida))
