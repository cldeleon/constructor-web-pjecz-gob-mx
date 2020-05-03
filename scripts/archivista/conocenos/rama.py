from comun.base import Base
from comun.seccion import Seccion


class Rama(Base):
    """ Coordina una Rama """

    def __init__(self, creador, directorio):
        super().__init__(
            insumos_ruta = directorio.path,
            secciones_comienzan_con = directorio.name,
            )
        self.plantillas_env = creador.plantillas_env
        self.titulo = directorio.name
        self.identificador = 'conocenos-????-????'
        self.resumen = '.'
        self.etiquetas = creador.etiquetas
        self.url = 'conocenos/????/????/'
        self.guardar_como = 'conocenos/????/????/index.html'
        self.creado = creador.creado
        self.modificado = creador.modificado
        self.secciones = []

    def alimentar(self):
        super().alimentar()

    def contenido(self):
        super().contenido()
        plantilla = self.plantillas_env.get_template('conocenos.md.jinja2')
        return(plantilla.render(
            title = self.titulo,
            slug = self.identificador,
            summary = self.resumen,
            tags = self.etiquetas,
            url = self.url,
            save_as = self.guardar_como,
            date = self.creado,
            modified = self.modificado,
            secciones = self.secciones,
            ))

    def __repr__(self):
        super().__repr__()
        return(f'<Rama> "{self.titulo}"')
