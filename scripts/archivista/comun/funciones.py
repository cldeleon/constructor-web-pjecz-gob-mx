import os
import re
import shutil
import unicodedata


def cambiar_acentos(text):
    """ Cambia los caracteres acentuados a caracteres sin acentos """
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return(str(text))

def cambiar_a_ruta_segura(text):
    """ Crea una ruta segura en minúsculas, espacios a guiones y sin caracteres acentuados, pero mantiene diagonales """
    text = cambiar_acentos(text.lower())
    text = re.sub('[ ]+', '-', text)
    text = re.sub('[^0-9a-zA-Z_/-]', '', text)
    return(text)

def cambiar_a_identificador(text):
    """ Crea un identificador en minúsculas, guiones y sin caracteres acentuados """
    text = cambiar_acentos(text.lower())
    text = re.sub('[/]+', '-', text)
    text = re.sub('[ ]+', '-', text)
    text = re.sub('[^0-9a-zA-Z_-]', '', text)
    return(text)

def sobreescribir_archivo(destino, contenido):
    """ Sobreescribir un archivo """
    if not os.path.exists(os.path.dirname(destino)):
        os.makedirs(os.path.dirname(destino))
    with open(destino, 'w') as file:
        file.write(contenido)
    return(' Sobreescribir ' + os.path.basename(destino))

def copiar_archivo(archivo_ruta, directorio_ruta):
    """ Copiar un archivo """
    if os.path.exists(archivo_ruta) and os.path.isfile(archivo_ruta) and os.path.exists(directorio_ruta) and os.path.isdir(directorio_ruta):
        nombre = os.path.basename(archivo_ruta)
        shutil.copyfile(archivo_ruta, f'{directorio_ruta}/{nombre}')
        return(f' Copiar {nombre}')
    else:
        return(f' FALLÓ copiar {archivo_ruta}')
