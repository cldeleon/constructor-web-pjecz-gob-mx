import os
from comun.base import Base
from comun.funciones import cambiar_a_identificador, cambiar_a_ruta_segura, obtener_metadatos_del_nombre


class Rama(Base):
    """ Coordina una rama (dentro de un tronco) del sitio web """

    def __init__(self, creador, directorio):
        super().__init__(
            insumos_ruta=directorio.path,
            secciones_comienzan_con=directorio.name,
        )
        self.plantillas_env = creador.plantillas_env
        # Definir URL y guardar_como
        rama_relativa = cambiar_a_ruta_segura(self.insumos_ruta[len(creador.insumos_ruta) + 1:])
        self.url = creador.url + rama_relativa + '/'
        self.guardar_como = self.url + 'index.html'
        # Definir el identificador
        self.identificador = cambiar_a_identificador(creador.identificador + ' ' + rama_relativa)
        # Obtener metadatos
        meta = creador.metadatos.consultar(self.identificador)
        if meta is None:
            fecha_hora, titulo = obtener_metadatos_del_nombre(directorio.name, creador.creado)
            self.titulo = titulo
            self.creado = fecha_hora
            self.modificado = fecha_hora
            self.resumen = '.'
            self.etiquetas = creador.etiquetas
            self.oculto = '0'
        else:
            self.titulo = meta['titulo']
            self.resumen = meta['resumen']
            self.etiquetas = meta['etiquetas']
            self.creado = meta['creado']
            self.modificado = meta['modificado']
            self.oculto = meta['oculto']
        # Definir el destino al archivo markdown a escribir
        self.destino_ruta = creador.destino_ruta + '/' + rama_relativa
        self.destino_md_ruta = self.destino_ruta + '/' + cambiar_a_identificador(directorio.name) + '.md'
        # Permitir tomar descargas
        self.alimentar_insumos_en_subdirectorios = True

    def alimentar(self):
        super().alimentar()
        if not self.alimentado:
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
        if len(self.secciones) > 0:
            salidas = []
            for seccion in self.secciones:
                salidas.append('    ' + str(seccion))
            for imagen in self.imagenes:
                salidas.append('    (' + os.path.basename(imagen) + ')')
            if self.oculto == '1':
                oculto = 'OCULTO'
            else:
                oculto = ''
            return(f'<Rama> {self.creado} {oculto} "{self.titulo}"\n' + '\n'.join(salidas))
        else:
            return(f'<Rama> {self.creado} "{self.titulo}" SIN SECCIONES')
