from datetime import datetime
from comun.base import Base
from comun.seccion import Seccion


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
        super().__repr__()
        if len(self.secciones) > 0:
            salidas = []
            for seccion in self.secciones:
                descargas_en_renglones = str(seccion).replace(' (', '\n        (')
                salidas.append('      ' + descargas_en_renglones)
            return(f'<Fraccion> "{self.titulo}"\n' + '\n'.join(salidas))
        else:
            return(f'<Fraccion> "{self.titulo}" SIN SECCIONES')
