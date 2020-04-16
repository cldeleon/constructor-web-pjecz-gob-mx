import csv
import os
from datetime import datetime
from transparencia.base import Base
from transparencia.seccion import Seccion


def scantree(path):
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path)
        else:
            yield entry


class Fraccion(Base):
    """ Coordina una rama de Fracción """

    def __init__(self, articulo, rama, ordinal, pagina, titulo, resumen, etiquetas):
        self.articulo = articulo
        self.ordinal = ordinal
        self.titulo = titulo
        secciones_comienzan_con = 'F{} {}'.format(self.ordinal.zfill(2), self.titulo)
        insumos_ruta = f'{self.articulo.insumos_ruta}/{secciones_comienzan_con}'
        super().__init__(insumos_ruta, secciones_comienzan_con)
        self.rama = rama
        self.pagina = pagina
        self.resumen = resumen
        self.etiquetas = etiquetas
        self.creado = self.modificado = datetime.today().isoformat(sep=' ', timespec='minutes')
        self.destino = f'transparencia/{self.rama}/{self.pagina}/{self.pagina}.md'

    def alimentar(self):
        super().alimentar()
        if self.alimentado == False:
            # Levantar bandera
            self.alimentado = True

    def contenido(self):
        super().contenido()
        # Agregar el listado de vínculos a las descargas
        lineas = []
        lineas.append(f'* [Prueba 1](#)')
        lineas.append(f'* [Prueba 2](#)')
        lineas.append(f'* [Prueba 3](#)')
        self.secciones.append(Seccion('Descargas', '\n'.join(lineas)))
        # Entregar contenido
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
            secciones = self.secciones,
            ))

    def __repr__(self):
        if self.alimentado == False:
            self.alimentar()
        if len(self.secciones) == 0 or len(self.insumos) == 0:
            return('')
        yo_mismo = []
        yo_mismo.append(f'      {self.titulo}:')
        if len(self.secciones) > 0:
            s = []
            for seccion in self.secciones:
                s.append(seccion.archivo_md)
            yo_mismo.append(', '.join(s))
        if len(self.insumos) > 0:
            yo_mismo.append('+' * len(self.insumos))
        return(' '.join(yo_mismo))
