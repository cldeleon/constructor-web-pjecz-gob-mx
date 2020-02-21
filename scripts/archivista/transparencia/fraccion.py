import os
from datetime import datetime
from transparencia.plantillas import env


class Fraccion(object):

    def __init__(self, articulo, numero, fraccion, title, summary, tags):
        self.articulo = articulo
        self.numero = numero
        self.fraccion = fraccion
        self.title = title
        self.slug = f'transparencia-{articulo}-{fraccion}'
        self.summary = summary
        self.tags = tags
        self.date = self.modified = datetime.today().isoformat(sep=' ', timespec='minutes')

    def destino(self):
        return(f'transparencia/{self.articulo}/{self.fraccion}/{self.fraccion}.md')

    def url(self):
        return(f'transparencia/{self.articulo}/{self.fraccion}/')

    def save_as(self):
        return(f'transparencia/{self.articulo}/{self.fraccion}/index.html')

    def obtener_descargables(self):
        ruta = self.url()
        if os.path.exists(os.path.dirname(ruta)):
            archivos = [f for f in os.listdir(ruta) if os.path.isfile(os.path.join(ruta, f))]
            descargables = list()
            for archivo in archivos:
                nombre, extension = os.path.splitext(archivo)
                if extension in [ '.doc', '.docx', '.pdf', '.ppt', '.pptx', '.xls', '.xlsx', '.zip' ]:
                    descargables.append(archivo)
            return(descargables)
        else:
            return([])

    def contenido(self, descargables=[]):
        plantilla = env.get_template('fraccion.md.jinja2')
        contenido = plantilla.render(
            title=self.title,
            slug=self.slug,
            summary=self.summary,
            tags=self.tags,
            url=self.url(),
            save_as=self.save_as(),
            date=self.date,
            modified=self.modified,
            descargables=self.obtener_descargables(),
            )
        return(contenido)

    def __repr__(self):
        return(self.slug)
