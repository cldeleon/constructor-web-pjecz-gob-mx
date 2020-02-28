import os
from datetime import datetime
from transparencia.plantillas import env


class Fraccion(object):

    def __init__(self, rama, ordinal, pagina, titulo, resumen, etiquetas):
        self.rama = rama
        self.ordinal = ordinal
        self.pagina = pagina
        self.titulo = titulo
        self.resumen = resumen
        self.etiquetas = etiquetas
        self.creado = self.modificado = datetime.today().isoformat(sep=' ', timespec='minutes')

    def destino(self):
        return(f'transparencia/{self.rama}/{self.pagina}/{self.pagina}.md')

    def contenido(self, descargables=[]):
        descargables = []
        ruta = f'transparencia/{self.rama}/{self.pagina}/'
        if os.path.exists(os.path.dirname(ruta)):
            archivos = [f for f in os.listdir(ruta) if os.path.isfile(os.path.join(ruta, f))]
            for archivo in archivos:
                nombre, extension = os.path.splitext(archivo)
                if extension in [ '.doc', '.docx', '.pdf', '.ppt', '.pptx', '.xls', '.xlsx', '.zip' ]:
                    descargables.append(archivo)
        plantilla = env.get_template('fraccion.md.jinja2')
        return(plantilla.render(
            title = self.titulo,
            slug = f'transparencia-{self.rama}-{self.pagina}',
            summary = self.resumen,
            tags = self.etiquetas,
            url = f'transparencia/{self.rama}/{self.pagina}/',
            save_as = f'transparencia/{self.rama}/{self.pagina}/index.html',
            date = self.creado,
            modified = self.modificado,
            descargables = descargables,
            ))

    def __repr__(self):
        return(f'{self.destino()}, {self.titulo}')
