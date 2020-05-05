import csv
import os


class Metadatos(object):
    """ Metadatos """

    def __init__(self, metadatos_csv):
        self.metadatos_csv = metadatos_csv
        self.metadatos = {}
        self.cargado = False

    def cargar(self):
        if os.path.exists(self.metadatos_csv):
            with open(self.metadatos_csv) as puntero:
                lector = csv.DictReader(puntero)
                for renglon in lector:
                    self.metadatos[renglon['identificador']] = {
                        'titulo': renglon['titulo'],
                        'resumen': renglon['resumen'],
                        'etiquetas': renglon['etiquetas'],
                        'creado': renglon['creado'],
                        'modificado': renglon['modificado'],
                        'oculto': renglon['oculto'],
                        }
            self.cargado = True

    def consultar(self, identificador):
        if self.cargado == False:
            self.cargar()
        if identificador in self.metadatos:
            return(self.metadatos[identificador])
        else:
            return(None)

    def __repr__(self):
        return('<Metadatos>')
