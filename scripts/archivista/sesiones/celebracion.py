from datetime import datetime
from comun.base import Base
from comun.seccion import Seccion


class Celebracion(Base):
    """ Coordina una rama de Sesión """

    def __init__(self, sala, rama, ordinal, pagina, titulo, resumen, etiquetas, creado, modificado, oculto):
        super().__init__(
            insumos_ruta = f'{sala.insumos_ruta}/{titulo}',
            secciones_comienzan_con = titulo,
            )
        self.sala = sala
        self.rama = rama
        self.ordinal = ordinal
        self.pagina = pagina
        self.titulo = titulo[11:] # Quitar YYYY-MM-DD
        self.resumen = resumen
        self.etiquetas = etiquetas
        self.creado = creado
        self.modificado = modificado # datetime.today().isoformat(sep=' ', timespec='minutes')
        self.oculto = oculto
        self.destino = f'sesiones/{self.rama}/{self.pagina}/{self.pagina}.md'
        self.alimentar_insumos_en_subdirectorios = True

    def alimentar(self):
        super().alimentar()
        if self.alimentado == False:
            # Juntar Secciones
            self.secciones = self.secciones_iniciales + self.secciones_intermedias + self.secciones_finales
            # Levantar bandera
            self.alimentado = True

    def contenido(self):
        super().contenido()
        plantilla = self.sala.sesiones.plantillas_env.get_template('sesiones.md.jinja2')
        return(plantilla.render(
            title = self.titulo,
            slug = f'sesiones-{self.rama}-{self.pagina}',
            summary = self.resumen,
            tags = self.etiquetas,
            url = f'sesiones/{self.rama}/{self.pagina}/',
            save_as = f'sesiones/{self.rama}/{self.pagina}/index.html',
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
                descargas_en_renglones = str(seccion).replace(' (', '\n        (')
                salidas.append('      ' + descargas_en_renglones)
            return(f'<Celebracion> "{self.titulo}"\n' + '\n'.join(salidas))
        else:
            return(f'<Celebracion> "{self.titulo}" SIN SECCIONES')
