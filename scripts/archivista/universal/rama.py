from comun.base import Base
from comun.funciones import cambiar_a_identificador, cambiar_a_ruta_segura
from comun.seccion import Seccion


class Rama(Base):
    """ Coordina una rama """

    def __init__(self, creador, directorio):
        super().__init__(
            insumos_ruta = directorio.path,
            secciones_comienzan_con = directorio.name,
            )
        self.plantillas_env = creador.plantillas_env
        self.titulo = directorio.name
        self.resumen = '.'
        self.etiquetas = creador.etiquetas
        self.creado = creador.creado
        self.modificado = creador.modificado
        # Definir las rutas
        rama_relativa = cambiar_a_ruta_segura(self.insumos_ruta[len(creador.insumos_ruta) + 1:])
        self.url = creador.url + rama_relativa + '/'
        self.guardar_como = self.url + 'index.html'
        # Definir el identificador
        self.identificador = cambiar_a_identificador(creador.identificador + ' ' + rama_relativa)
        # Definir el destino al archivo markdown a escribir
        self.destino_ruta = creador.destino_ruta + '/' + rama_relativa
        self.destino_md_ruta = self.destino_ruta + '/' + cambiar_a_identificador(directorio.name) + '.md'
        # Permitir tomar descargas
        self.alimentar_insumos_en_subdirectorios = True

    def alimentar(self):
        super().alimentar()
        if self.alimentado == False:
            # Juntar Secciones
            self.secciones = self.secciones_iniciales + self.secciones_intermedias + self.secciones_finales
            # Levantar bandera
            self.alimentado = True

    def contenido(self):
        super().contenido()
        plantilla = self.plantillas_env.get_template('universal.md.jinja2')
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
        if len(self.secciones) > 0:
            salidas = []
            for seccion in self.secciones:
                salidas.append('    ' + str(seccion))
            return(f'<Rama> "{self.titulo}"\n' + '\n'.join(salidas))
        else:
            return(f'<Rama> "{self.titulo}" SIN SECCIONES')
