import os
from comun.base import Base
from comun.funciones import cambiar_a_identificador
from universal.rama import Rama


class Universal(Base):
    """ Coordina tronco del sitio web """

    def __init__(self, insumos_ruta, salida_ruta, metadatos, plantillas_env, titulo, resumen, etiquetas, creado, modificado):
        super().__init__(
            insumos_ruta=insumos_ruta,
            secciones_comienzan_con=titulo,
        )
        self.insumos_ruta = insumos_ruta
        self.salida_ruta = salida_ruta
        self.metadatos = metadatos
        self.plantillas_env = plantillas_env
        # Definir el identificador
        self.identificador = cambiar_a_identificador(titulo)
        # Obtener metadatos
        meta = self.metadatos.consultar(self.identificador)
        if meta is None:
            self.titulo = titulo
            self.resumen = resumen
            self.etiquetas = etiquetas
            self.creado = creado
            self.modificado = modificado
            self.oculto = '0'
        else:
            self.titulo = meta['titulo']
            self.resumen = meta['resumen']
            self.etiquetas = meta['etiquetas']
            self.creado = meta['creado']
            self.modificado = meta['modificado']
            self.oculto = meta['oculto']
        # Definir URL y guardar_como
        self.url = self.identificador + '/'
        self.guardar_como = self.url + 'index.html'
        # Definir el destino al archivo markdown a escribir
        self.destino_ruta = self.salida_ruta + '/' + self.identificador
        self.destino_md_ruta = self.destino_ruta + '/' + self.identificador + '.md'
        # Listado de ramas
        self.ramas = []

    def rastrear_directorios(self, ruta):
        for item in os.scandir(ruta):
            if item.is_dir(follow_symlinks=False):
                yield item
                yield from self.rastrear_directorios(item.path)

    def alimentar(self):
        super().alimentar()
        if self.alimentado is False:
            # Rastrear los directorios y acumular ramas
            for directorio in self.rastrear_directorios(self.insumos_ruta):
                posible_md_nombre = os.path.basename(directorio.path)
                posible_md_ruta = f'{directorio.path}/{posible_md_nombre}.md'
                if os.path.exists(posible_md_ruta):
                    self.ramas.append(Rama(self, directorio))
            # Juntar Secciones
            self.secciones = self.secciones_iniciales + self.secciones_intermedias + self.secciones_finales
            # Levantar bandera
            self.alimentado = True

    def contenido(self):
        super().contenido()
        plantilla = self.plantillas_env.get_template('universal.md.jinja2')
        return(plantilla.render(
            title=self.titulo,
            slug=self.identificador,
            summary=self.resumen,
            tags=self.etiquetas,
            url=self.url,
            save_as=self.guardar_como,
            date=self.creado,
            modified=self.modificado,
            secciones=self.secciones,
            oculto=self.oculto,
        ))

    def __repr__(self):
        super().__repr__()
        if len(self.ramas) > 0:
            salidas = []
            for rama in self.ramas:
                salidas.append('  ' + str(rama))
            for imagen in self.imagenes:
                salidas.append('  (' + os.path.basename(imagen) + ')')
            return(f'<Universal> {self.creado} "{self.titulo}"\n' + '\n'.join(salidas))
        else:
            return(f'<Universal> {self.creado} "{self.titulo}" SIN SECCIONES')
