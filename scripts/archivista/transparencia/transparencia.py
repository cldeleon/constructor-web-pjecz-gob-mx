from datetime import datetime
from transparencia.plantillas import env
from transparencia.articulo import Articulo


class Transparencia(object):

    def __init__(self):
        self.title = 'Transparencia'
        self.slug = 'transparencia'
        self.summary = 'Pendiente'
        self.tags = 'Transparencia'
        self.date = self.modified = datetime.today().isoformat(sep=' ', timespec='minutes')
        self.articulos = list()

    def alimentar(self, transparencia_csv):
        articulo = Articulo()
        articulo.alimentar(transparencia_csv)
        self.articulos.append(articulo)

    def destino(self):
        return('transparencia/transparencia.md')

    def contenido(self):
        plantilla = env.get_template('transparencia.md.jinja2')
        contenido = plantilla.render(
            title=self.title,
            slug=self.slug,
            summary=self.summary,
            tags=self.tags,
            url='transparencia/',
            save_as='transparencia/index.html',
            date=self.date,
            modified=self.modified,
            )
        return(contenido)

    def __repr__(self):
        return(self.destino())
