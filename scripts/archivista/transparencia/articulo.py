import csv
from datetime import datetime
from comun.base import Base
from comun.seccion import Seccion
from transparencia.fraccion import Fraccion


class Articulo(Base):
    """ Coordina una rama de Artículo, que tiene varias Fracciones """

    def __init__(self, transparencia, rama, pagina, titulo, resumen, etiquetas):
        super().__init__(
            insumos_ruta = f'{transparencia.insumos_ruta}/{titulo}',
            secciones_comienzan_con = titulo,
            )
        self.transparencia = transparencia
        self.rama = rama
        self.pagina = pagina
        self.titulo = titulo
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
                        self.fracciones.append(fraccion)
            # Agregar Seccion con el listado de vínculos a las fracciones
            if len(self.fracciones) > 0:
                lineas = []
                for fraccion in self.fracciones:
                    lineas.append(f'{fraccion.ordinal}. [{fraccion.titulo}]({fraccion.pagina}/)')
                self.secciones_intermedias.append(Seccion('Fracciones', '\n'.join(lineas)))
            # Juntar Secciones
            self.secciones = self.secciones_iniciales + self.secciones_intermedias + self.secciones_finales
            # Levantar bandera
            self.alimentado = True

    def contenido(self):
        super().contenido()
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
        super().__repr__()
        if len(self.secciones) > 0:
            salidas = []
            for seccion in self.secciones:
                descargas_en_renglones = str(seccion).replace(' (', '\n      (')
                salidas.append('    ' + descargas_en_renglones)
            for fraccion in self.fracciones:
                salidas.append('    ' + str(fraccion))
            return(f'<Articulo> "{self.titulo}"\n' + '\n'.join(salidas))
        else:
            return(f'<Articulo> "{self.titulo}" SIN SECCIONES')
