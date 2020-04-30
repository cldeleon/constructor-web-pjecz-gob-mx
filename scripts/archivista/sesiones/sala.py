import csv
from comun.base import Base
from comun.seccion import Seccion
from sesiones.celebracion import Celebracion


class Sala(Base):
    """ Coordina una rama de una Sala, que tiene varias Celebraciones """

    def __init__(self, sesiones, rama, pagina, titulo, resumen, etiquetas, creado, modificado, oculto):
        super().__init__(
            insumos_ruta = f'{sesiones.insumos_ruta}/{titulo}',
            secciones_comienzan_con = titulo,
            )
        self.sesiones = sesiones
        self.rama = rama
        self.pagina = pagina
        self.titulo = titulo
        self.resumen = resumen
        self.etiquetas = etiquetas
        self.creado = creado
        self.modificado = modificado
        self.oculto = oculto
        self.destino = f'sesiones/{self.rama}/{self.rama}.md'
        self.celebraciones = []

    def alimentar(self):
        super().alimentar()
        if self.alimentado == False:
            # Alimentar celebraciones
            with open(self.sesiones.metadatos_csv) as puntero:
                lector = csv.DictReader(puntero)
                for renglon in lector:
                    if renglon['rama'] == self.rama and int(renglon['ordinal']) > 0:
                        celebracion = Celebracion(
                            sala = self,
                            rama = renglon['rama'],
                            ordinal = renglon['ordinal'],
                            pagina = renglon['pagina'],
                            titulo = renglon['titulo'],
                            resumen = renglon['resumen'],
                            etiquetas = renglon['etiquetas'],
                            creado = renglon['creado'],
                            modificado = renglon['modificado'],
                            oculto = renglon['oculto'],
                            )
                        celebracion.alimentar()
                        self.celebraciones.append(celebracion)
            # Agregar Seccion con el listado de vínculos a las celebraciones
            if len(self.celebraciones) > 0:
                lineas = []
                for celebracion in self.celebraciones:
                    lineas.append(f'{celebracion.ordinal}. [{celebracion.titulo}]({celebracion.pagina}/)')
                self.secciones_intermedias.append(Seccion('Sesiones', '\n'.join(lineas)))
            # Juntar Secciones
            self.secciones = self.secciones_iniciales + self.secciones_intermedias + self.secciones_finales
            # Levantar bandera
            self.alimentado = True

    def contenido(self):
        super().contenido()
        plantilla = self.sesiones.plantillas_env.get_template('sesiones.md.jinja2')
        return(plantilla.render(
            title = self.titulo,
            slug = f'sesiones-{self.rama}',
            summary = self.resumen,
            tags = self.etiquetas,
            url = f'sesiones/{self.rama}/',
            save_as = f'sesiones/{self.rama}/index.html',
            date = self.creado,
            modified = self.modificado,
            secciones = self.secciones,
            oculto = self.oculto,
            ))

    def __repr__(self):
        super().__repr__()
        if len(self.secciones) > 0:
            salidas = []
            for seccion in self.secciones:
                descargas_en_renglones = str(seccion).replace(' [', '\n      [')
                salidas.append('    ' + descargas_en_renglones)
            for celebracion in self.celebraciones:
                salidas.append('    ' + str(celebracion))
            return(f'<Sala> "{self.titulo}"\n' + '\n'.join(salidas))
        else:
            return(f'<Sala> "{self.titulo}" SIN SECCIONES')
