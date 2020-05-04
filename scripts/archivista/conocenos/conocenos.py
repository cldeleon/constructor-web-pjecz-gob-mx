import click
import os
from comun.base import Base
from conocenos.rama import Rama


class Conocenos(Base):
    """ Coordina la rama de Conócenos """

    def __init__(self, insumos_ruta, salida_ruta, metadatos_csv, plantillas_env):
        super().__init__(
            insumos_ruta = insumos_ruta,
            secciones_comienzan_con = 'Conócenos',
            )
        self.insumos_ruta = insumos_ruta
        self.salida_ruta = salida_ruta
        self.metadatos_csv = metadatos_csv
        self.plantillas_env = plantillas_env
        # Definir lo que necesita contenido
        self.titulo = 'Conócenos'
        self.identificador = 'conocenos'
        self.resumen = '.'
        self.etiquetas = 'Conócenos'
        self.url = 'conocenos/'
        self.guardar_como = self.url + 'index.html'
        self.creado = self.modificado = '2020-05-01 15:00:00'
        # Definir el destino al archivo markdown a escribir
        self.destino_ruta = f'{self.salida_ruta}/conocenos'
        self.destino_md_ruta = f'{self.destino_ruta}/conocenos.md'
        # Listado de ramas
        self.ramas = []

    def rastrear_directorios(self, ruta):
        for item in os.scandir(ruta):
            if item.is_dir(follow_symlinks=False):
                yield item
                yield from self.rastrear_directorios(item.path)

    def alimentar(self):
        super().alimentar()
        if self.alimentado == False:
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
        plantilla = self.plantillas_env.get_template('conocenos.md.jinja2')
        return(plantilla.render(
            title = self.titulo,
            slug = self.identificador,
            summary = self.resumen,
            tags = self.etiquetas,
            url = self.url,
            save_as = self.guardar_como,
            date = self.creado,
            modified = self.modificado,
            secciones = self.secciones,
            ))

    def __repr__(self):
        super().__repr__()
        if len(self.ramas) > 0:
            salidas = []
            for rama in self.ramas:
                salidas.append('  ' + str(rama))
            return(f'<Conocenos> "{self.titulo}"\n' + '\n'.join(salidas))
        else:
            return(f'<Conocenos> "{self.titulo}" SIN SECCIONES')
