import csv
from datetime import datetime
from comun.base import Base
from comun.seccion import Seccion
from sesiones.sala import Sala


class Sesiones(Base):
    """ Coordina la rama de Sesiones """

    def __init__(self, insumos_ruta, salida_ruta, metadatos_csv, plantillas_env):
        super().__init__(
            insumos_ruta = insumos_ruta,
            secciones_comienzan_con = 'Sesiones',
            )
        self.salida_ruta = salida_ruta
        self.metadatos_csv = metadatos_csv
        self.plantillas_env = plantillas_env
        self.titulo = 'Sesiones'
        self.resumen = '.'
        self.etiquetas = 'Sesiones'
        self.creado = self.modificado = '2020-01-01 15:00:00' # datetime.today().isoformat(sep=' ', timespec='minutes')
        self.destino = 'sesiones/sesiones.md'
        self.salas = []

    def alimentar(self):
        super().alimentar()
        if self.alimentado == False:
            # Alimentar salas
            alimentados = []
            with open(self.metadatos_csv) as puntero:
                lector = csv.DictReader(puntero)
                for renglon in lector:
                    if renglon['rama'] not in alimentados:
                        sala = Sala(
                            sesiones = self,
                            rama = renglon['rama'],
                            pagina = renglon['pagina'],
                            titulo = renglon['titulo'],
                            resumen = renglon['resumen'],
                            etiquetas = renglon['etiquetas'],
                            creado = renglon['creado'],
                            modificado = renglon['modificado'],
                            oculto = renglon['oculto'],
                            )
                        sala.alimentar()
                        self.salas.append(sala)
                        alimentados.append(renglon['rama'])
            # Agregar Seccion con listado de salas
            if len(self.salas) > 0:
                lineas = []
                for sala in self.salas:
                    lineas.append(f'* [{sala.titulo}]({sala.pagina}/)')
                self.secciones_intermedias.append(Seccion('Salas', '\n'.join(lineas)))
            # Juntar Secciones
            self.secciones = self.secciones_iniciales + self.secciones_intermedias + self.secciones_finales
            # Levantar bandera
            self.alimentado = True

    def contenido(self):
        super().contenido()
        plantilla = self.plantillas_env.get_template('sesiones.md.jinja2')
        return(plantilla.render(
            title = self.titulo,
            slug = 'sesiones',
            summary = self.resumen,
            tags = self.etiquetas,
            url = 'sesiones/',
            save_as = 'sesiones/index.html',
            date = self.creado,
            modified = self.modificado,
            secciones = self.secciones,
            oculto = '1',
            ))

    def __repr__(self):
        super().__repr__()
        if len(self.secciones) > 0:
            salidas = []
            for seccion in self.secciones:
                salidas.append('  ' + str(seccion))
            for sala in self.salas:
                salidas.append('  ' + str(sala))
            return(f'<Sesiones> "{self.titulo}"\n' + '\n'.join(salidas))
        else:
            return(f'<Sesiones> "{self.titulo}" SIN SECCIONES')
