import csv
import os
from datetime import datetime
from transparencia.base import Base
from transparencia.fraccion import Fraccion
from transparencia.seccion import Seccion


class Articulo(Base):
    """ Coordina una rama de Artículo, que tiene varias Fracciones """

    def __init__(self, transparencia, rama, pagina, titulo, resumen, etiquetas):
        self.transparencia = transparencia
        self.titulo = titulo
        secciones_comienzan_con = self.titulo
        insumos_ruta = f'{self.transparencia.insumos_ruta}/{secciones_comienzan_con}'
        super().__init__(insumos_ruta, secciones_comienzan_con)
        self.rama = rama
        self.pagina = pagina
        self.resumen = resumen
        self.etiquetas = etiquetas
        self.creado = self.modificado = datetime.today().isoformat(sep=' ', timespec='minutes')
        self.destino = f'transparencia/{self.rama}/{self.rama}.md'
        self.fracciones = []

    def alimentar(self):
        super().alimentar()
        if self.alimentado == False:
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
        super().contenido()
        # Agregar el listado de vínculos a las fracciones
        lineas = []
        for fraccion in self.fracciones:
            lineas.append(f'{fraccion.ordinal}. [{fraccion.titulo}]({fraccion.pagina}/)')
        self.secciones.append(Seccion('Fracciones', '\n'.join(lineas)))
        # Entregar contenido
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
            secciones = self.secciones,
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
