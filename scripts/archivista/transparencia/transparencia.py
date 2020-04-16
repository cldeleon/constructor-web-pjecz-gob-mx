import csv
import os
from datetime import datetime
from transparencia.articulo import Articulo
from transparencia.base import Base
from transparencia.seccion import Seccion


class Transparencia(Base):
    """ Coordina la rama de Transparencia, que tiene varios Artículos """

    def __init__(self, insumos_ruta, salida_ruta, metadatos_csv, plantillas_env):
        super().__init__(insumos_ruta, 'Transparencia')
        self.salida_ruta = salida_ruta
        self.metadatos_csv = metadatos_csv
        self.plantillas_env = plantillas_env
        self.titulo = 'Transparencia'
        self.resumen = 'Pendiente'
        self.etiquetas = 'Transparencia'
        self.creado = self.modificado = datetime.today().isoformat(sep=' ', timespec='minutes')
        self.destino = 'transparencia/transparencia.md'
        self.articulos = []

    def alimentar(self):
        super().alimentar()
        if self.alimentado == False:
            # Alimentar articulos
            alimentados = []
            with open(self.metadatos_csv) as puntero:
                lector = csv.DictReader(puntero)
                for renglon in lector:
                    if renglon['rama'] not in alimentados:
                        articulo = Articulo(
                            transparencia = self,
                            rama = renglon['rama'],
                            pagina = renglon['pagina'],
                            titulo = renglon['titulo'],
                            resumen = renglon['resumen'],
                            etiquetas = renglon['etiquetas'],
                            )
                        articulo.alimentar()
                        if len(articulo.secciones) > 0:
                            self.articulos.append(articulo)
                        alimentados.append(renglon['rama'])
            # Levantar bandera
            self.alimentado = True

    def contenido(self):
        super().contenido()
        # Agregar el listado de vínculos a los artículos
        lineas = []
        for articulo in self.articulos:
            lineas.append(f'* [{articulo.titulo}]({articulo.pagina}/)')
        self.secciones.append(Seccion('Artículos', '\n'.join(lineas)))
        # Entregar contenido
        plantilla = self.plantillas_env.get_template('transparencia.md.jinja2')
        return(plantilla.render(
            title = self.titulo,
            slug = 'transparencia',
            summary = self.resumen,
            tags = self.etiquetas,
            url = 'transparencia/',
            save_as = 'transparencia/index.html',
            date = self.creado,
            modified = self.modificado,
            secciones = self.secciones,
            ))

    def __repr__(self):
        if self.alimentado == False:
            self.alimentar()
        yo_mismo = []
        yo_mismo.append(f'  {self.titulo}:')
        if len(self.secciones) > 0:
            s = []
            for seccion in self.secciones:
                s.append(seccion.archivo_md)
            yo_mismo.append(', '.join(s))
        if len(self.insumos) > 0:
            yo_mismo.append('+' * len(self.insumos))
        salida = [' '.join(yo_mismo)]
        for articulo in self.articulos:
            if str(articulo) != '':
                salida.append(str(articulo))
        return('\n'.join(salida))
