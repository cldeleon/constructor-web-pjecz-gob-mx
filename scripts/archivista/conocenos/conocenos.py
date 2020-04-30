import csv
from datetime import datetime
from comun.base import Base
from comun.seccion import Seccion


class Conocenos(Base):
    """ Coordina la rama de Conócenos """

    def __init__(self, arg):
        super().__init__(
            insumos_ruta = insumos_ruta,
            secciones_comienzan_con = 'Conócenos',
            )
        self.arg = arg

    def alimentar(self):
        super().alimentar()

    def contenido(self):
        super().contenido()

    def __repr__(self):
        super().__repr__()
