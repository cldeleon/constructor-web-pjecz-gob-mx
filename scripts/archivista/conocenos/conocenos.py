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
        self.titulo = 'Conócenos'
        self.resumen = '.'
        self.etiquetas = 'Conócenos'
        self.creado = self.modificado = '2020-01-01 15:00:00'
        self.destino = 'conocenos/conocenos.md'
        self.ramas = []

    def rastrear_directorios(self, ruta):
        for item in os.scandir(ruta):
            if item.is_dir(follow_symlinks=False):
                yield item
                yield from self.rastrear_directorios(item.path)

    def alimentar(self):
        super().alimentar()
        for directorio in self.rastrear_directorios(self.insumos_ruta):
            self.ramas.append(Rama(self, directorio))

    def contenido(self):
        super().contenido()

    def __repr__(self):
        super().__repr__()
        if len(self.ramas) > 0:
            salidas = []
            for rama in self.ramas:
                salidas.append('  ' + str(rama))
            return(f'<Conocenos> "{self.titulo}"\n' + '\n'.join(salidas))
        else:
            return(f'<Conocenos> "{self.titulo}" SIN SECCIONES')
