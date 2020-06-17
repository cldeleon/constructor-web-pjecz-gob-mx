import csv
from comun.base import Base
from comun.seccion import Seccion
from transparenciatca.fraccion import Fraccion


class Articulo(Base):
    """ Coordina una rama de Artículo, que tiene varias Fracciones """

    def __init__(self, transparencia, rama, pagina, titulo, resumen, etiquetas, creado, modificado, oculto):
        super().__init__(
            insumos_ruta=f'{transparencia.insumos_ruta}/{titulo}',
            secciones_comienzan_con=titulo,
        )
        self.transparencia = transparencia
        self.rama = rama
        self.pagina = pagina
        self.titulo = titulo
        self.resumen = resumen
        self.etiquetas = etiquetas
        self.creado = creado
        self.modificado = modificado
        self.oculto = oculto
        self.destino = f'transparencia-tca/{self.rama}/{self.rama}.md'
        self.fracciones = []

    def alimentar(self):
        super().alimentar()
        if self.alimentado is False:
            # Alimentar fracciones
            with open(self.transparencia.metadatos_csv) as puntero:
                lector = csv.DictReader(puntero)
                for renglon in lector:
                    if renglon['rama'] == self.rama and int(renglon['ordinal']) > 0:
                        fraccion = Fraccion(
                            articulo=self,
                            rama=renglon['rama'],
                            ordinal=renglon['ordinal'],
                            pagina=renglon['pagina'],
                            titulo=renglon['titulo'],
                            resumen=renglon['resumen'],
                            etiquetas=renglon['etiquetas'],
                            creado=renglon['creado'],
                            modificado=renglon['modificado'],
                            oculto=renglon['oculto'],
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
            title=self.titulo,
            slug=f'transparencia-tca-{self.rama}',
            summary=self.resumen,
            tags=self.etiquetas,
            url=f'transparencia-tca/{self.rama}/',
            save_as=f'transparencia-tca/{self.rama}/index.html',
            date=self.creado,
            modified=self.modificado,
            secciones=self.secciones,
        ))

    def __repr__(self):
        super().__repr__()
        if len(self.secciones) > 0:
            salidas = []
            for seccion in self.secciones:
                descargas_en_renglones = str(seccion).replace(' [', '\n      [')
                salidas.append('    ' + descargas_en_renglones)
            for fraccion in self.fracciones:
                salidas.append('    ' + str(fraccion))
            return(f'<Articulo> "{self.titulo}"\n' + '\n'.join(salidas))
        else:
            return(f'<Articulo> "{self.titulo}" SIN SECCIONES')
