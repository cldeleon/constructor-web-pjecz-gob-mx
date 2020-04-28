import os
from pathlib import Path


class Descargable(object):
    """ Descargable """

    def __init__(self, ruta):
        self.ruta = ruta
        self.hash = None
        self.subido = False
        self.almacen_frio = 'https://storage.googleapis.com/pjecz-gob-mx'

    def nombre(self):
        """ Entregar nombre.ext """
        return(os.path.basename(self.ruta))

    def vinculo(self):
        """ Entregar el vínculo de este descargable en Google Cloud """
        # Determinar la ruta base a nextcloud_ruta
        home_ruta = str(Path.home())
        nextcloud_ruta = f'{home_ruta}/Nextcloud/Sitios Web/pjecz.gob.mx'
        # Recorte
        if self.ruta[:len(nextcloud_ruta)] != nextcloud_ruta:
            return('')
        # Determinar la rama
        rama_ruta = self.ruta[len(nextcloud_ruta):]
        vinculo_ruta = self.almacen_frio + rama_ruta
        return(vinculo_ruta)

    def __repr__(self):
        return(f'<Descargable> {self.vinculo()}')
