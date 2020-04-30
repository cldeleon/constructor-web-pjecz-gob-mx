import csv
from datetime import datetime
from comun.base import Base
from comun.seccion import Seccion
from transparenciatca.articulo import Articulo


class TransparenciaTCA(Base):
    """ Coordina la rama de Transparencia TCA """

    def __init__(self, insumos_ruta, salida_ruta, metadatos_csv, plantillas_env):
        super().__init__(
            insumos_ruta = insumos_ruta,
            secciones_comienzan_con = 'Transparencia TCA',
            )
        self.salida_ruta = salida_ruta
        self.metadatos_csv = metadatos_csv
        self.plantillas_env = plantillas_env
        self.titulo = 'Transparencia Tribunal de Conciliación y Arbitraje'
        self.resumen = 'Pendiente'
        self.etiquetas = 'Transparencia TCA'
        self.creado = self.modificado = datetime.today().isoformat(sep=' ', timespec='minutes')
        self.destino = 'transparencia-tca/transparencia-tca.md'
        self.articulos = []

    def alimentar(self):
        super().alimentar()
        if self.alimentado == False:
            # Alimentar articulos
            alimentados = []
            with open(self.metadatos_csv) as puntero:
                lector = csv.DictReader(puntero)
                for renglon in lector:
                    if renglon['rama'] not in alimentados:
                        articulo = Articulo(
                            transparencia = self,
                            rama = renglon['rama'],
                            pagina = renglon['pagina'],
                            titulo = renglon['titulo'],
                            resumen = renglon['resumen'],
                            etiquetas = renglon['etiquetas'],
                            )
                        articulo.alimentar()
                        self.articulos.append(articulo)
                        alimentados.append(renglon['rama'])
            # Agregar Seccion con listado de articulos
            if len(self.articulos) > 0:
                lineas = []
                for articulo in self.articulos:
                    lineas.append(f'* [{articulo.titulo}]({articulo.pagina}/)')
                self.secciones_intermedias.append(Seccion('Artículos', '\n'.join(lineas)))
            # Juntar Secciones
            self.secciones = self.secciones_iniciales + self.secciones_intermedias + self.secciones_finales
            # Levantar bandera
            self.alimentado = True

    def contenido(self):
        super().contenido()
        plantilla = self.plantillas_env.get_template('transparencia.md.jinja2')
        return(plantilla.render(
            title = self.titulo,
            slug = 'transparencia-tca',
            summary = self.resumen,
            tags = self.etiquetas,
            url = 'transparencia-tca/',
            save_as = 'transparencia-tca/index.html',
            date = self.creado,
            modified = self.modificado,
            secciones = self.secciones,
            ))

    def __repr__(self):
        super().__repr__()
        if len(self.secciones) > 0:
            salidas = []
            for seccion in self.secciones:
                salidas.append('  ' + str(seccion))
            for articulo in self.articulos:
                salidas.append('  ' + str(articulo))
            return(f'<Transparencia> "{self.titulo}"\n' + '\n'.join(salidas))
        else:
            return(f'<Transparencia> "{self.titulo}" SIN SECCIONES')
