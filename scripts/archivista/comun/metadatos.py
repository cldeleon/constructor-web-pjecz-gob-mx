import csv
import os


class Metadatos(object):
    """ Cargar los metadatos y ofrecer consultas de los mismos """

    def __init__(self, metadatos_csv):
        self.metadatos_csv = metadatos_csv
        self.metadatos = {}
        self.cargado = False

    def cargar(self):
        """ Cargar el archivo metadatos_csv """
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
        """ Consultar por identificador """
        if self.cargado is False:
            self.cargar()
        if identificador in self.metadatos:
            return(self.metadatos[identificador])
        else:
            return(None)

    def __repr__(self):
        return('<Metadatos>')
