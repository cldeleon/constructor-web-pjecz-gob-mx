from comun.base import Base


class Fraccion(Base):
    """ Coordina una rama de Fracción """

    def __init__(self, articulo, rama, ordinal, pagina, titulo, resumen, etiquetas, creado, modificado, oculto):
        super().__init__(
            insumos_ruta=f'{articulo.insumos_ruta}/F{ordinal.zfill(2)} {titulo}',
            secciones_comienzan_con=f'F{ordinal.zfill(2)} {titulo}',
        )
        self.articulo = articulo
        self.rama = rama
        self.ordinal = ordinal
        self.pagina = pagina
        self.titulo = titulo
        self.resumen = resumen
        self.etiquetas = etiquetas
        self.creado = creado
        self.modificado = modificado
        self.oculto = oculto
        self.destino = f'transparencia-tca/{self.rama}/{self.pagina}/{self.pagina}.md'
        self.alimentar_insumos_en_subdirectorios = True

    def alimentar(self):
        super().alimentar()
        if self.alimentado is False:
            # Juntar Secciones
            self.secciones = self.secciones_iniciales + self.secciones_intermedias + self.secciones_finales
            # Levantar bandera
            self.alimentado = True

    def contenido(self):
        super().contenido()
        plantilla = self.articulo.transparencia.plantillas_env.get_template('fraccion.md.jinja2')
        return(plantilla.render(
            title=self.titulo,
            slug=f'transparencia-tca-{self.rama}-{self.pagina}',
            summary=self.resumen,
            tags=self.etiquetas,
            url=f'transparencia-tca/{self.rama}/{self.pagina}/',
            save_as=f'transparencia-tca/{self.rama}/{self.pagina}/index.html',
            date=self.creado,
            modified=self.modificado,
            secciones=self.secciones,
        ))

    def __repr__(self):
        super().__repr__()
        if len(self.secciones) > 0:
            salidas = []
            for seccion in self.secciones:
                descargas_en_renglones = str(seccion).replace(' [', '\n        [')
                salidas.append('      ' + descargas_en_renglones)
            return(f'<Fraccion> "{self.titulo}"\n' + '\n'.join(salidas))
        else:
            return(f'<Fraccion> "{self.titulo}" SIN SECCIONES')
