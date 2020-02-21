import csv
from datetime import datetime
from transparencia.plantillas import env
from transparencia.fraccion import Fraccion


class Articulo(object):

    def __init__(self):
        self.articulo = 'articulo-21'
        self.title = 'Transparencia - Artículo 21'
        self.slug = f'transparencia-{self.articulo}'
        self.summary = 'Pendiente'
        self.tags = 'Transparencia'
        self.date = self.modified = datetime.today().isoformat(sep=' ', timespec='minutes')
        self.fracciones = list()

    def alimentar(self, transparencia_csv):
        with open(transparencia_csv) as puntero:
            lector = csv.DictReader(puntero)
            for renglon in lector:
                self.fracciones.append(Fraccion(
                    articulo=renglon['articulo'],
                    numero=int(renglon['numero']),
                    fraccion=renglon['fraccion'],
                    title=renglon['title'],
                    summary=renglon['summary'],
                    tags=renglon['tags'],
                    ))

    def destino(self):
        return(f'transparencia/{self.articulo}/{self.articulo}.md')

    def contenido(self):
        plantilla = env.get_template('articulo.md.jinja2')
        contenido = plantilla.render(
            title=self.title,
            slug=self.slug,
            summary=self.summary,
            tags=self.tags,
            url=f'transparencia/{self.articulo}/',
            save_as=f'transparencia/{self.articulo}/index.html',
            date=self.date,
            modified=self.modified,
            fracciones=self.fracciones,
            )
        return(contenido)

    def __repr__(self):
        output = list()
        for fraccion in self.fracciones:
            output.append(fraccion.destino())
        return('\n'.join(output))
