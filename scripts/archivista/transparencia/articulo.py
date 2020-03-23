import csv
import os
from datetime import datetime
from transparencia.fraccion import Fraccion
from transparencia.seccion import Seccion


class Articulo(object):

    def __init__(self, transparencia, rama, pagina, titulo, resumen, etiquetas):
        self.transparencia = transparencia
        self.rama = rama
        self.pagina = pagina
        self.titulo = titulo
        self.resumen = resumen
        self.etiquetas = etiquetas
        self.creado = self.modificado = datetime.today().isoformat(sep=' ', timespec='minutes')
        self.secciones_comienzan_con = self.titulo
        self.insumos_ruta = f'{self.transparencia.insumos_ruta}/{self.secciones_comienzan_con}'
        self.destino = f'transparencia/{self.rama}/{self.rama}.md'
        self.insumos = []
        self.secciones = []
        self.fracciones = []
        self.alimentado = False

    def alimentar(self):
        if self.alimentado == False:
            # Alimentar insumos
            if os.path.exists(self.insumos_ruta):
                with os.scandir(self.insumos_ruta) as scan:
                    for item in scan:
                        if not item.name.startswith('.') and item.is_file():
                            self.insumos.append(item.name)
            self.insumos.sort()
            # Alimentar secciones
            for insumo in self.insumos:
                if insumo.endswith('.md') and insumo.startswith(self.secciones_comienzan_con):
                    self.secciones.append(Seccion(self.insumos_ruta, insumo))
            # Alimentar fracciones
            with open(self.transparencia.metadatos_csv) as puntero:
                lector = csv.DictReader(puntero)
                for renglon in lector:
                    if renglon['rama'] == self.rama and int(renglon['ordinal']) > 0:
                        fraccion = Fraccion(
                            articulo = self,
                            rama = renglon['rama'],
                            ordinal = renglon['ordinal'],
                            pagina = renglon['pagina'],
                            titulo = renglon['titulo'],
                            resumen = renglon['resumen'],
                            etiquetas = renglon['etiquetas'],
                            )
                        fraccion.alimentar()
                        if len(fraccion.secciones) > 0:
                            self.fracciones.append(fraccion)
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
        plantilla = self.transparencia.plantillas_env.get_template('articulo.md.jinja2')
        return(plantilla.render(
            title = self.titulo,
            slug = f'transparencia-{self.rama}',
            summary = self.resumen,
            tags = self.etiquetas,
            url = f'transparencia/{self.rama}/',
            save_as = f'transparencia/{self.rama}/index.html',
            date = self.creado,
            modified = self.modificado,
            introduccion = introduccion,
            fracciones = self.fracciones,
            final = final,
            ))

    def __repr__(self):
        if self.alimentado == False:
            self.alimentar()
        if len(self.secciones) == 0 and len(self.insumos) == 0 and len(self.fracciones) == 0:
            return('')
        yo_mismo = []
        yo_mismo.append(f'    {self.titulo}:')
        if len(self.secciones) > 0:
            s = []
            for seccion in self.secciones:
                s.append(seccion.archivo_md)
            yo_mismo.append(', '.join(s))
        if len(self.insumos) > 0:
            yo_mismo.append('+' * len(self.insumos))
        salida = [' '.join(yo_mismo)]
        for fraccion in self.fracciones:
            if str(fraccion) != '':
                salida.append(str(fraccion))
        return('\n'.join(salida))
