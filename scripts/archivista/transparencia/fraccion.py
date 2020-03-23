import csv
import os
from datetime import datetime
from transparencia.seccion import Seccion


def scantree(path):
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path)
        else:
            yield entry


class Fraccion(object):

    def __init__(self, articulo, rama, ordinal, pagina, titulo, resumen, etiquetas):
        self.articulo = articulo
        self.rama = rama
        self.ordinal = ordinal
        self.pagina = pagina
        self.titulo = titulo
        self.resumen = resumen
        self.etiquetas = etiquetas
        self.creado = self.modificado = datetime.today().isoformat(sep=' ', timespec='minutes')
        self.secciones_comienzan_con = 'F{} {}'.format(self.ordinal.zfill(2), self.titulo)
        self.insumos_ruta = f'{self.articulo.insumos_ruta}/{self.secciones_comienzan_con}'
        self.destino = f'transparencia/{self.rama}/{self.pagina}/{self.pagina}.md'
        self.insumos = []
        self.secciones = []
        self.alimentado = False

    def alimentar(self):
        if self.alimentado == False:
            # Alimentar insumos
            if os.path.exists(self.insumos_ruta):
                for entry in scantree(self.insumos_ruta):
                    self.insumos.append(entry.name)
            self.insumos.sort()
            # Alimentar secciones
            for insumo in self.insumos:
                if insumo.endswith('.md') and insumo.startswith(self.secciones_comienzan_con):
                    self.secciones.append(Seccion(self.insumos_ruta, insumo))
            # Levantar bandera
            self.alimentado = True

    def contenido(self):
        if self.alimentado == False:
            self.alimentar()
        if len(self.secciones) > 0:
            introducciones = []
            for seccion in self.secciones:
                introducciones.append(seccion.contenido())
            introduccion = '\n'.join(introducciones)
        else:
            introduccion = '### Sin introducción'
        final = '### Sin final'
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
            introduccion = introduccion,
            descargables = [],
            final = final,
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
