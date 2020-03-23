
class Seccion(object):
    """ Sección de una página """

    def __init__(self, insumos_ruta, archivo_md):
        self.insumos_ruta = insumos_ruta
        self.archivo_md = archivo_md
        self.markdown = ''
        self.procesado = False

    def procesar(self):
        with open(f'{self.insumos_ruta}/{self.archivo_md}', 'r') as f:
            self.markdown = f.read()
        self.procesado = True

    def contenido(self):
        if self.procesado == False:
            self.procesar()
        return(self.markdown)

    def __repr__(self):
        if self.procesado == False:
            self.procesar()
        return(f'<Sección> {self.archivo_md}')
